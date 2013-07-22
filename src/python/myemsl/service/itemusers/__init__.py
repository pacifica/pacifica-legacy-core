#!/usr/bin/python

import os
import sys
import errno
import urllib
import simplejson as json
from pymongo import Connection as mongoconnection
from myemsl.getconfig import getconfig_notification
config = getconfig_notification('jmds')

from myemsl.logging import getLogger

logger = getLogger(__name__)

def itemusers(item_id, req, retries=1):
	client = mongoconnection(config.notification.hostname, config.notification.port)
	collection = client['pacifica_db']['jmds_collection']
	code = 404
	item_id = int(item_id)
	f = collection.find({"_id":item_id})
	for doc in f:
		req.write(json.dumps(doc))
		req.write("\n")
		list = []
		if 'agd' not in doc or doc['agd'] != False:
			if 'submitter' in doc:
				list.append(doc['submitter'])
			req.write(json.dumps(list))
			req.write("\n")
		code = 200
		break
	return code

if __name__ == '__main__':
	res = itemusers(sys.argv[1], sys.stdout)
	print res
	sys.exit(res)

