#!/usr/bin/python

import sys
import pycurl
import simplejson as json

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def get_alias(index='simple_items', alias=None, server=None, config=config):
	if alias == None:
		alias = "%s_%s" %(config.get('elasticsearch', "alias"), index)
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
#FIXME This grabs all aliases. should find an api that maps only the single one we need.
	url += alias + '/_aliases'
	curl.setopt(curl.URL, url)
	curl.setopt(curl.WRITEFUNCTION, writebody.write)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	if code != 200:
		return None, code
	writebody.seek(0)
	j = json.load(writebody)
	keys = j.keys()
	if len(keys) < 1:
		code = 404
		return None, code
	retval = keys[0]
	return retval, code

if __name__ == "__main__":
	retval, code = get_alias(sys.argv[1])
	if code != 200:
		print code
		sys.exit(code)
	print retval
