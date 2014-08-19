#!/usr/bin/python

import sys
from myemsl.callcurl import call_curl, CurlException
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()


def bulk_action(index, actions, server=None, config=config):
	alias_cmd = '\n'.join([json.dumps(i) for i in actions])
	alias_cmd += '\n'
	if server == None:
		server = config.get('elasticsearch', 'server')
	writebody = ""
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index + "/_bulk"
	try:
		writebody = call_curl(url, method="POST", idata=alias_cmd)
	except CurlException, ex:
		return ex.http_code
	return code

if __name__ == "__main__":
	code = bulk_action(sys.argv[1], json.loads('\n'.join(sys.stdin.readlines())))
	if code != 200:
		print code
		sys.exit(code)
