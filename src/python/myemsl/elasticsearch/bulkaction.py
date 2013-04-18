#!/usr/bin/python

import sys
import pycurl
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()


def bulk_action(index, actions, server=None, config=config):
	alias_cmd = '\n'.join([json.dumps(i) for i in actions])
	alias_cmd += '\n'
	if server == None:
		server = config.get('elasticsearch', 'server')
	curl = pycurl.Curl()
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
	curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
	writebody = StringIO()
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index + "/_bulk"
	curl.setopt(curl.URL, url)
	curl.setopt(curl.POST, 1)
	curl.setopt(curl.WRITEFUNCTION, writebody.write)
	curl.setopt(curl.POSTFIELDS, alias_cmd)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	return code

if __name__ == "__main__":
	code = bulk_action(sys.argv[1], json.loads('\n'.join(sys.stdin.readlines())))
	if code != 200:
		print code
		sys.exit(code)
