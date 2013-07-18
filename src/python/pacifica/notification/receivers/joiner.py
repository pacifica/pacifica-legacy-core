#!/usr/bin/python

import time
import pacifica.metadata.joiner
from optparse import OptionParser
from pacifica.notification import *
from pacifica.notification.receiver import *
from pymongo import Connection

class JoinerReceiver(Receiver):
	def __init__(self, host, port, db, notification_name, process_name):
       		super(JoinerReceiver, self).__init__(host, port, db, notification_name, process_name)
#FIXME make metadata collection usable with different mongodb host/database.
		client = Connection(host, port)
		db = client[db]
		self.metadata_fmds_collection = pymongo.collection.Collection(db, "fmds_collection", create=False)
		self.metadata_jmds_collection = pymongo.collection.Collection(db, "jmds_collection", create=False)
		self.wsw = writer_socket_writer(writer_socket_get("jmds"))
	def discovered(self, tag, item_id, version):
#FIXME get instance uuid from somewhere...
		pacifica.metadata.joiner.process_item(item_id, self.metadata_fmds_collection, self.joiner_cb)
	def joiner_cb(self, doc):
		while True:
			try:
				id = doc['_id']
				doc['pver'] = doc['ver']
				del doc['_id']
				del doc['ver']
				del doc['nver']
				doc = self.metadata_jmds_collection.find_and_modify(query={'_id': id}, update={'$setOnInsert': {'nver':0}, '$inc': {'ver': 1}, '$set': doc}, upsert=True, new=True)
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
	r = JoinerReceiver(parser.values.host, parser.values.port, parser.values.db, parser.values.channel, parser.values.module)
	sys.exit(r.run())
	pass

if __name__ == '__main__':
	main()
