#!/usr/bin/env python

import datetime

from mod_python import apache
from myemsl.authzpersondir import *
from myemsl.getconfig import getconfig
from pymongo import Connection
config = getconfig()

def authzhandler(req):
	res = general_authzhandler(req, position=5)
	if res == apache.OK:
		list = req.uri.split('/', 6)
		cart_id = int(list[5].split('.', 1)[0])
		logentry = {
			'd': datetime.datetime.now(),
			'c': cart_id
		}
		try:
			logentry['p'] = int(req.user)
		except:
			pass
		db_host = config.get('download_log', 'server')
		db_port = config.getint('download_log', 'port')
		db_name = config.get('download_log', 'db_name')
		collection_name = config.get('download_log', 'cart_collection')
		client = Connection(db_host, db_port)
		db = client[db_name]
		collection = pymongo.collection.Collection(db, collection_name)
		collection.insert(logentry, w=1)
	return res
