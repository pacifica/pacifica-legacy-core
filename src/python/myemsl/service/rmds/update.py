#!/usr/bin/python

import os
import sys
import struct
import simplejson as json
import pymongo
import pymongo.errors
import myemsl.ingest
import myemsl.metadata
from myemsl.service.rmds.notify import notify
from myemsl.getconfig import getconfig_notification

config = getconfig_notification('rmds')

from myemsl.logging import getLogger

logger = getLogger(__name__)

def update(user, transaction, stime, item_id, data):
	user = int(user)
	transaction = int(transaction)
	item_id = int(item_id)
	j = json.load(data)
#FIXME make metadata collection usable with different mongodb host/database.
	host = config.notification.hostname
	port = config.notification.port
	client = pymongo.Connection(host, port)
#FIXME make this configurable
	db = 'pacifica_db'
	db = client[db]
	rmds_collection = pymongo.collection.Collection(db, "rmds_collection", create=False)
	while True:
		found = False
		cursor = rmds_collection.find({'_id':item_id})
		for doc in cursor:
			found = True
			if 'add' not in j or len(j['add']) < 1:
				return 200
			old_version = doc['ver']
			doc['ver'] = old_version + 1
			vals = {}
			for (id, kvp) in doc["vals"].iteritems():
				key = kvp[0]
				value = kvp[1]
				t = vals.get(key)
				if t == None:
					t = {}
					vals[key] = t
				tvalue = json.dumps(value, sort_keys=True)
				t[tvalue] = id
			print vals
			newvallist = []
			for (key, value) in j['add'].iteritems():
				found = False
				tvalue = json.dumps(value, sort_keys=True)
				k = vals.get(key)
				if k != None:
					tv = k.get(tvalue)
					print "FOO", tv, tvalue
					if tv != None:
						found = True
						id = int(tv)
				if not found:
					nv = id = doc['nv']
					doc['nv'] = nv + 1
					doc['vals'][str(id)] = [key, value]
					print "Not found"
					print key, value
				newvallist.append(id)
				print id, newvallist, stime
				#docs['vals'][str(id)] = []...
			doc["trans"][str(transaction)] = {'s':user, 'st':stime, 'v':newvallist}
			del doc['_id']
#FIXME make w configurable.
			info = rmds_collection.update({'_id':int(item_id), 'ver':old_version}, {'$set': doc}, w=1)
			print json.dumps(doc, indent=4), json.dumps(j, indent=4), transaction
			if info['n'] > 0:
#FIXME for scalability, probably should make this a curl call to notification service.
				notify(user, item_id, doc['ver'])
				return 200
			else:
				logging.debug("document not updated due to version bump. retrying. %s" %(doc))
		if found == False:
			return 404

def main():
	update(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.stdin)

if __name__ == '__main__':
	main()
