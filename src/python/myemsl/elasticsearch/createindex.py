#!/usr/bin/python

import sys
import pycurl

import myemsl.elasticsearch.schema

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def create_index(index_name, server=None, config=config, desc=None):
	if desc == None:
		desc = myemsl.elasticsearch.schema.schema_get('simple_item')
	if server == None:
		server = config.get('elasticsearch', 'server')
	curl = pycurl.Curl()
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
	curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
	readbody = StringIO()
	writebody = StringIO()
	readbody.write(desc)
	readbody.seek(0)
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index_name
	curl.setopt(curl.URL, url)
	curl.setopt(curl.UPLOAD, 1) 
	curl.setopt(curl.PUT, 1)
	curl.setopt(curl.INFILESIZE, len(desc))
	curl.setopt(curl.WRITEFUNCTION, writebody.write)
	curl.setopt(curl.READFUNCTION, readbody.read)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	return code

if __name__ == "__main__":
	code = create_index(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
