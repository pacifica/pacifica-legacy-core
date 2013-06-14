#!/usr/bin/python

from optparse import OptionParser
from pacifica.notification import *
from pacifica.notification.receiver import *
from pymongo import Connection

class VersionClearerReceiver(Receiver):
	def __init__(self, host, port, db, notification_name, process_name, collection):
       		super(VersionClearerReceiver, self).__init__(host, port, db, notification_name, process_name)
#FIXME make metadata collection usable with different mongodb host/database.
		client = Connection(host, port)
		db = client[db]
		self.metadata_collection = pymongo.collection.Collection(db, "%s_collection" %(collection), create=False)
	def recover(self, db, collection, min_cur_id):
		self.last_id = collection.find().sort('$natural', 1).limit(1).next()['ts']
		print "Just using the oldest id: %s" %(self.last_id)
		return 0
	def discovered(self, tag, item_id, version):
		self.metadata_collection.update({'_id':int(item_id), 'ver':version}, {'$set': {'nver': version}})

def main():
	parser = OptionParser()
        add_usage(parser)
        add_options(parser)
	parser.add_option('-o', '--collection', type='string', action='store', dest='collection', default='', help="MongoDB collection metadata is stored in", metavar='C')
        parser.parse_args()
        check_options(parser)
	if parser.values.collection == "":
		parser.values.collection = parser.values.channel
	r = VersionClearerReceiver(parser.values.host, parser.values.port, parser.values.db, parser.values.channel, parser.values.module, parser.values.collection)
	sys.exit(r.run())
	pass

if __name__ == '__main__':
	main()
