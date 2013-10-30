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
from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

import simplejson as json

logger = getLogger(__name__)

def elasticsearchquery(user, index, type, req, retries=1, auth_add=False, search_type=None, scan=None):
	req_data = req.read()
	if type != 'released_publications' and user == '':
		req.write("Forbidden")
		return 401
	user_tries = 2
	while user_tries > 0:
		if type != "simple_items" and type != "released_publications":
			req.write("Forbidden")
			return 401
		if type == "released_publications":
			index = "myemsl_current_released_publications"
			auth_add = False
		server = config.get('elasticsearch', 'server')
		writebody = StringIO()
		curl = pycurl.Curl()
		curl.setopt(curl.POST, 1)
		curl.setopt(curl.POSTFIELDS, req_data)
		curl.setopt(pycurl.FOLLOWLOCATION, 1)
		curl.setopt(pycurl.MAXREDIRS, 5)
		curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
		url = server
		if url[-1:] != '/':
			url += '/'
		if scan:
			url += '/_search/scroll?scroll=10m'
		else:
			url += "%s/%s/_search" %(index, type)
			if search_type:
				url += '?search_type=scan&scroll=10m&size=50'
		curl.setopt(curl.URL, url)
		curl.setopt(curl.WRITEFUNCTION, writebody.write)
		curl.perform()
		code = curl.getinfo(pycurl.HTTP_CODE)
		curl.close()
		if code != 404:
			writebody.seek(0)
			if auth_add:
				auth_items = []
				j = json.load(writebody)
				for i in j['hits']['hits']:
					auth_items.append(i['_id'])
				if len(auth_items) > 0:
					token = myemsl.token.simple_items_token_gen(auth_items, person_id=int(user))
					logger.debug("Requested auth. %s" %(auth_items))
					j['myemsl_auth_token'] = token
				req.write(json.dumps(j))
				return code
			else:
				req.write('\n'.join(writebody.readlines()))
				return code
		retval = ""
		alias_tries = 3
		while alias_tries > 0:
			retval, code = myemsl.elasticsearch.get_alias(index=type)
			if code == 404:
				time.sleep(1)
				alias_tries -= 1
			elif code == 200:
				break
			else:
				return code
		if alias_tries < 1:
			return 500
		if type != 'released_publications':
			user_id = int(user)
			code = myemsl.elasticsearch.create_user_filter(retval, user_id)
			if code < 200 or code > 299:
				return 404
		user_tries -= 1

if __name__ == '__main__':
	sys.exit(elasticsearchquery(sys.argv[1], "myemsl_user_%s" %(sys.argv[1]), sys.argv[2], sys.stdout))

