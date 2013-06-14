#!/usr/bin/python

import os
import sys
import time
import errno
import fcntl
import struct
import pymongo
from optparse import OptionParser
from pymongo import Connection
from myemsl.util import try_mkdir
from pacifica.notification import *
from myemsl.getconfig import getconfig_notification

#http://linux.die.net/man/7/pipe PIPE_BUF atomic

def add_options(parser):
	parser.add_option('-d', '--db', type='string', action='store', dest='db', default='pacifica_db', help="MongoDB database to use", metavar='D')
	parser.add_option('-n', '--host', type='string', action='store', dest='host', default='', help="MongoDB hostname to use", metavar='H')
	parser.add_option('-p', '--port', type='int', action='store', dest='port', default=-1, help="MongoDB port number to use", metavar='P')
	parser.add_option('-c', '--channel', type='string', action='store', dest='channel', default='', help="Channel to listen on", metavar='C')
	parser.add_option('-s', '--socket', type='string', action='store', dest='socket', default='', help="Socket file to listen on", metavar='S')

def add_usage(parser):
	"""
	Adds a custom usage description string for this module to an OptionParser
	"""
	parser.set_usage("usage: %prog [options] -h host -c channel")

def check_options(parser):
	if parser.values.channel == "":
		sys.stderr.write("You must specify a channel with -c\n")
		sys.exit(-1)
	config = getconfig_notification(parser.values.channel)
	if parser.values.host == "":
		try:
			parser.values.host = config.notification.hostname
		except Exception, e:
			raise e
			sys.stderr.write("You must specify a MongoDB host with -n\n")
			sys.exit(-1)
	if parser.values.port == -1:
		parser.values.port = config.notification.port
	if parser.values.socket == "":
		parser.values.socket = writer_socket_get(parser.values.channel)
		try_mkdir(os.path.dirname(parser.values.socket))

def main():
	parser = OptionParser()
        add_usage(parser)
        add_options(parser)
        parser.parse_args()
        check_options(parser)
	try:
    		os.mkfifo(parser.values.socket)
	except OSError, e:
		if e.errno != errno.EEXIST:
			raise
	socket = os.open(parser.values.socket, os.O_RDONLY | os.O_NONBLOCK)
	socket_write = os.open(parser.values.socket, os.O_WRONLY | os.O_NONBLOCK)
	fl = fcntl.fcntl(socket, fcntl.F_GETFL)
	fcntl.fcntl(socket, fcntl.F_SETFL, fl & (~os.O_NONBLOCK))

	print "|%s|%s|" %(parser.values.host, parser.values.port)
	while True:
		try:
			client = Connection(parser.values.host, parser.values.port)
			db = client[parser.values.db]
			collection_name = collection_name_get(db, parser.values.channel)
			collection = pymongo.collection.Collection(db, collection_name, create=False)
			last_id = collection.find().sort('$natural', -1).limit(1).next()['ts']
			print "Collection: %s" %(collection_name)
			print "Last ID: %s" %(last_id)
#512 atomic read is min garanteed by posix. This number is provided by select.PIPE_BUF only in python >= 2.7. :(
			PIPE_BUF = 512
			while(True):
				data = os.read(socket, PIPE_BUF)
				if len(data) % 16 != 0:
					sys.stderr.write("Bad read from pipe. Size is not right! %s\n" %(len(data)))
					return -1
				f = "<%sq" %(len(data) / 8)
				unpacked = struct.unpack(f, data)
				s = [(unpacked[i*2], unpacked[i*2+1]) for i in range(0, len(unpacked)/2)]
				for (i, v) in s:
					next_id = last_id + 1
					try:
						collection.insert({'_id':next_id, 'id':i, 'ts':next_id, 'ver':v})
						last_id = next_id
					except Exception, e:
						print e
		except pymongo.errors.AutoReconnect, e:
			print "Mongo disconnect. %s. Trying again in 10 seconds..." %(e)
			time.sleep(10)

if __name__ == '__main__':
	sys.exit(main())
