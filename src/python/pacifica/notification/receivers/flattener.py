#!/usr/bin/python

import time
import pacifica.metadata.flattener
from optparse import OptionParser
from pacifica.notification import *
from pacifica.notification.receiver import *
from pymongo import Connection

class FlattenerReceiver(Receiver):
	def __init__(self, host, port, db, notification_name, process_name):
       		super(FlattenerReceiver, self).__init__(host, port, db, notification_name, process_name)
#FIXME make metadata collection usable with different mongodb host/database.
		client = Connection(host, port)
		db = client[db]
		self.metadata_tmds_collection = pymongo.collection.Collection(db, "tmds_collection", create=False)
		self.metadata_fmds_collection = pymongo.collection.Collection(db, "fmds_collection", create=False)
		self.wsw = writer_socket_writer(writer_socket_get("fmds"))
#FIXME get last id out of stream, query all items out of rmds and call discovered on them, then continue
#	def recover(self, db, collection, min_cur_id):
#		self.last_id = collection.find().sort('$natural', 1).limit(1).next()['ts']
#		print "Just using the oldest id: %s" %(self.last_id)
#		return 0
	def discovered(self, tag, item_id, version):
#FIXME get instance uuid from somewhere...
		instanceuuid = 'instanceuuid'
		pacifica.metadata.flattener.process_item(instanceuuid, item_id, self.metadata_tmds_collection, self.flattener_cb)
	def flattener_cb(self, doc):
		while True:
			try:
				id = doc['_id']
				del doc['_id']
				doc = self.metadata_fmds_collection.find_and_modify(query={'_id': id}, update={'$setOnInsert': {'nver':0}, '$inc': {'ver': 1}, '$set': doc}, upsert=True, new=True)
				self.wsw.entry(id, doc['ver'])
				break
			except pymongo.errors.OperationFailure, e:
				print "Mongo issue. %s." %(e)
				time.sleep(1)

def main():
	parser = OptionParser()
        add_usage(parser)
        add_options(parser)
        parser.parse_args()
        check_options(parser)
	r = FlattenerReceiver(parser.values.host, parser.values.port, parser.values.db, parser.values.chanel, parser.values.module)
	sys.exit(r.run())
	pass

if __name__ == '__main__':
	main()
