#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def get_alias(index='simple_items', alias=None, server=None, config=config):
	if alias == None:
		alias = "%s_%s" %(config.get('elasticsearch', "alias"), index)
	if server == None:
		server = config.get('elasticsearch', 'server')
	url = server
	if url[-1:] != '/':
		url += '/'
#FIXME This grabs all aliases. should find an api that maps only the single one we need.
	url += alias + '/_aliases'
	writebody = ""
	try:
		writebody = call_curl(url)
	except CurlException, ex:
		return None, ex.http_code
	j = json.loads(writebody)
	keys = j.keys()
	if len(keys) < 1:
		code = 404
		return None, code
	retval = keys[0]
	return retval, 200

if __name__ == "__main__":
	retval, code = get_alias(sys.argv[1])
	if code != 200:
		print code
		sys.exit(code)
	print retval
