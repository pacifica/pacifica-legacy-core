#!/usr/bin/python

import os
import sys
import errno
import urllib
import pycurl
import time
import myemsl.elasticsearch
import myemsl.token
import myemsl.token.rfc3339enc as rfc3339enc
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

from myemsl.logging import getLogger

import myemsl.elasticsearch

logger = getLogger(__name__)

#FIXME this code also exists in query engine. libraryize it.
def auth_sign(items):
#FIXME read in from config.
	uuid = 'huYNwptYEeGzDAAmucepzw';
#FIXME read in from config.
	duration = 60 * 60
	js = {'s':rfc3339enc.rfc3339(time.time()), 'd':duration, 'u':uuid, 'i':items, 'o':0}
	stok = myemsl.token.token_gen(js, '')
	return stok

#FIXME most of this code looks just like elasticsearch service's code (Since copied from. consider generalizing that code)
def itemauth(user, item_id, req, retries=1):
	user_id = int(user)
	item_id = int(item_id)
	(code, document) = myemsl.elasticsearch.item_auth(user_id, item_id)
	if code == 200:
		token = auth_sign([item_id])
		req.write(token)
	return code

if __name__ == '__main__':
	res = itemauth(sys.argv[1], sys.argv[2], sys.stdout)
	print res
	sys.exit(res)

