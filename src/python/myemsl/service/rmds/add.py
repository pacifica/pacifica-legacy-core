#!/usr/bin/python

import os
import sys
import struct
import simplejson as json
import pymongo
import pymongo.errors
from myemsl.service.rmds.notify import notify
from myemsl.getconfig import getconfig_notification

config = getconfig_notification('rmds')

from myemsl.logging import getLogger

logger = getLogger(__name__)

def add(user, data):
	version = 1
	j = json.load(data)
	item_id = j['_id']
#FIXME make metadata collection usable with different mongodb host/database.
	host = config.notification.hostname
	port = config.notification.port
	client = pymongo.Connection(host, port)
#FIXME make this configurable
	db = 'pacifica_db'
	db = client[db]
	rmds_collection = pymongo.collection.Collection(db, "rmds_collection", create=False)
	try:
#FIXME make w configurable for safety.
		rmds_collection.insert(j, w=1)
	except pymongo.errors.DuplicateKeyError, e:
		data.write("%s\n" %(json.dumps({'error': str(e)})))
		return 400
#FIXME for scalability, probably should make this a curl call to notification service.
	notify(user, item_id, version)
	return 200
