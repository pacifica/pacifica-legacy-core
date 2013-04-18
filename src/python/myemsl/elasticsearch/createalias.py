#!/usr/bin/python

import sys
import pycurl
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
	curl = pycurl.Curl()
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
	curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
	writebody = StringIO()
	url = server
	if url[-1:] != '/':
		url += '/'
	url += "_aliases"
	curl.setopt(curl.URL, url)
	curl.setopt(curl.POST, 1)
	curl.setopt(curl.WRITEFUNCTION, writebody.write)
	curl.setopt(curl.POSTFIELDS, alias_cmd)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	return code

if __name__ == "__main__":
	code = create_alias(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
