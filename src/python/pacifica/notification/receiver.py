#!/usr/bin/python
#http://blog.pythonisito.com/2013/04/mongodb-pubsub-with-capped-collections.html

import __main__ as tmain
import os
import sys
import time
import errno
import os.path
import pymongo
import simplejson as json
from pymongo import Connection
from optparse import OptionParser
from pymongo.cursor import _QUERY_OPTIONS
from myemsl.util import try_mkdir
from pacifica.notification import *

from myemsl.getconfig import getconfig_notification

class Receiver(object):
	def __init__(self, host, port, db, notification_name, process_name):
		self.host = host
		self.port = port
		self.db = db
		self.notification_name = notification_name
		self.process_name = process_name
		self.pid = os.getpid()
		self.last_id = None
		self.last_version = None
		self.last_tag_init()
		if self.last_version == None:
			self.last_version = notification_version_get(host, port, db, notification_name)
		self.collection_name = collection_name_get(None, notification_name, self.last_version)
		if self.last_id == None:
			self.last_id = 1 #Initied always to one.
		print "Last ID: %s" %(self.last_id)
	def last_tag_init(self):
		dir = '/var/lib/pacifica/metanotification/last'
		try_mkdir(dir)
		self.statefile = "%s/%s_%s.json" %(dir, self.notification_name, self.process_name)
		try:
			file = open(self.statefile, 'r')
			j = json.load(file)
			self.last_id = j['last_id']
			self.last_version = j['last_version']
			file.close()
		except IOError, e:
			if e.errno != errno.ENOENT:
				raise
		except Exception, e:
			raise
	def write_last_tag(self):
		file = open("%s.%s" %(self.statefile, self.pid), 'w')
		file.write("{\"last_id\":%s, \"last_version\":%s}\n" %(self.last_id, self.last_version))
		file.close()
		os.rename("%s.%s" %(self.statefile, self.pid), self.statefile)
	def recover(self, db, collection, min_cur_id):
		print "Need to recover! %s < %s" %(self.last_id, min_cur_id)
		return -1
	def discovered(self, tag, item_id, version):
		print {'tag':tag, 'item_id': item_id, 'version': version}
	def run(self):
		need_recovery = False
		min_cur_id = None
		while True:
			client = Connection(self.host, self.port)
			db = client[self.db]
			if self.collection_name not in db.collection_names():
#FIXME deal with collection versions.
				sys.stderr.write("Collection %s does not exist.\n" %(self.collection_name))
				sys.exit(-1)

			collection = db[self.collection_name]

			if need_recovery:
				res = self.recover(db, collection, notification['ts'])
				if res != 0:
					return res

			first_pass = True
			query = {}
			if self.last_id != None:
#FIXME because of this, if last_id goes backwards, you will never see updates for them until they become larger then last_id again.
				query['ts'] = {'$gt': self.last_id - 1}
			cursor = collection.find(query, await_data=True, tailable=True).hint([('$natural', 1)])
			try:
				while cursor.alive:
					try:
						notification = cursor.next()
						if first_pass:
							if self.last_id < notification['ts']:
								need_recovery = True
								min_cur_id = notification['ts']
								break
							if self.last_id == notification['ts']:
								first_pass = False
								continue #Already processed this document. None were lost.
						self.discovered(notification['ts'], notification['id'], notification['ver'])
						self.last_id = notification['ts']
					except StopIteration:
						continue
					except pymongo.errors.OperationFailure, e:
						print "Failure! Reconnecting.", e
						break
			except KeyboardInterrupt:
				print "trl-C"
				self.write_last_tag()
				return 0

class TestReceiver(Receiver):
	def last_tag_init(self):
		self.last_id = 0
	def recover(self, db, collection, min_cur_id):
		self.last_id = collection.find().sort('$natural', -1).limit(1).next()['ts']
		print "Just using most recent id: %s" %(self.last_id)
		return 0
	def write_last_id(self):
		pass

def add_options(parser):
	parser.add_option('-d', '--db', type='string', action='store', dest='db', default='pacifica_db', help="MongoDB database to use", metavar='D')
	parser.add_option('-n', '--host', type='string', action='store', dest='host', default='', help="MongoDB hostname to use", metavar='H')
	parser.add_option('-p', '--port', type='int', action='store', dest='port', default=27017, help="MongoDB port number to use", metavar='P')
	parser.add_option('-c', '--channel', type='string', action='store', dest='channel', default='', help="Notification Chanel to use", metavar='C')
	parser.add_option('-m', '--module', type='string', action='store', dest='module', default='', help="Notification Module to use", metavar='M')

def check_options(parser):
	if parser.values.channel == "":
		sys.stderr.write("You must specify a channel with -c\n")
		sys.exit(-1)
	if parser.values.host == "":
		config = getconfig_notification(parser.values.channel)
		parser.values.host = config.notification.hostname
	name = os.path.basename(tmain.__file__)
	if name.endswith('.py'):
		name[:-len('.py')]
	if parser.values.module == '':
		parser.values.module = name

def add_usage(parser):
	"""
	Adds a custom usage description string for this module to an OptionParser
	"""
	parser.set_usage("usage: %prog [options] -c channel -m module -n hostname")

def main():
	parser = OptionParser()
        add_usage(parser)
        add_options(parser)
        parser.parse_args()
        check_options(parser)
	r = Receiver(parser.values.host, parser.values.port, parser.values.db, parser.values.channel, parser.values.module)
	sys.exit(r.run())
	
if __name__ == '__main__':
	main()
