#!/usr/bin/python

import os
import sys
import errno
import urllib
import pycurl
import time
import myemsl.elasticsearch
import myemsl.token
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

from myemsl.logging import getLogger

import myemsl.elasticsearch

logger = getLogger(__name__)

#FIXME most of this code looks just like elasticsearch service's code (Since copied from. consider generalizing that code)
def itemauth(user, item_id, req, retries=1):
	user_id = int(user)
	item_id = int(item_id)
	(code, document) = myemsl.elasticsearch.item_auth(user_id, item_id)
	if code == 200:
		token = myemsl.token.simple_items_token_gen([item_id], person_id=user_id)
		req.write(token)
	return code

if __name__ == '__main__':
	res = itemauth(sys.argv[1], sys.argv[2], sys.stdout)
	print res
	sys.exit(res)

