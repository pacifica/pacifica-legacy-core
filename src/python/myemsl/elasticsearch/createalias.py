#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()


def create_alias(index, alias, server=None, config=config):
##FIXME delete alias if it already exists
	alias_cmd = """
{
	"actions": [{
		"add": {
			"index": "%s",
			"alias": "%s"
		}
	}]
}""" %(index, alias)
	if server == None:
		server = config.get('elasticsearch', 'server')
	writebody = ""
	url = server
	if url[-1:] != '/':
		url += '/'
	url += "_aliases"
	try:
		writebody = call_curl(url, method="POST", idata=alias_cmd)
	except CurlException, ex:
		return ex.http_code
	return 200

if __name__ == "__main__":
	code = create_alias(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
