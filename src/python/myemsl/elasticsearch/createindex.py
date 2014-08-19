#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException

import myemsl.elasticsearch.schema

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def create_index(index_name, server=None, config=config, desc=None):
	if desc == None:
		desc = myemsl.elasticsearch.schema.schema_get('simple_item')
	if server == None:
		server = config.get('elasticsearch', 'server')
	writebody = ""
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index_name
	try:
		writebody = call_curl(url, method="PUT", idata=desc)
	except CurlException, ex:
		return ex.http_code
	return 200

if __name__ == "__main__":
	code = create_index(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
