#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def delete_index(index_name, server=None, config=config):
	if server == None:
		server = config.get('elasticsearch', 'server')
	writebody = ""
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index_name
	try:
		writebody = call_curl(url, method="DELETE")
	except CurlException, ex:
		return ex.http_code
	return code

if __name__ == "__main__":
	code = delete_index(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
