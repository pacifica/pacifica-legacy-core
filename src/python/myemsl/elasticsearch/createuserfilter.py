#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()


def create_user_filter(index, user_id, server=None, prefix="myemsl_user", config=config):
	alias = "%s_%i" %(prefix, user_id)
	filter = """
{
	"actions": [{
		"add": {
			"index": "%s",
			"alias": "%s",
			"filter": {
				"or": [{
					"term": {"users": %i}
				}, {
					"term": {"aged": true}
				}]
			}
		}
	}]
}""" %(index, alias, user_id)
	if server == None:
		server = config.get('elasticsearch', 'server')
	writebody = ""
	url = server
	if url[-1:] != '/':
		url += '/'
	url += "_aliases"
	try:
		writebody = call_curl(url, method="POST", postfields=filter)
	except CurlException, ex:
		return ex.http_code
	return code

if __name__ == "__main__":
	code = create_user_filter(sys.argv[1], int(sys.argv[2]))
	if code != 200:
		print code
		sys.exit(code)
