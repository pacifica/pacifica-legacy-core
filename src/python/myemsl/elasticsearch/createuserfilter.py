#!/usr/bin/python

import sys
import pycurl
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
	curl.setopt(curl.POSTFIELDS, filter)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	return code

if __name__ == "__main__":
	code = create_user_filter(sys.argv[1], int(sys.argv[2]))
	if code != 200:
		print code
		sys.exit(code)
