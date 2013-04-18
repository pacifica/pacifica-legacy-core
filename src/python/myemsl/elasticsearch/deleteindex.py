#!/usr/bin/python

import sys
import pycurl

from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()

def delete_index(index_name, server=None, config=config):
	if server == None:
		server = config.get('elasticsearch', 'server')
	curl = pycurl.Curl()
	curl.setopt(pycurl.FOLLOWLOCATION, 1)
	curl.setopt(pycurl.MAXREDIRS, 5)
	curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
	curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
	curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
	writebody = StringIO()
	url = server
	if url[-1:] != '/':
		url += '/'
	url += index_name
	curl.setopt(curl.URL, url)
	curl.setopt(curl.WRITEFUNCTION, writebody.write)
	curl.perform()
	code = curl.getinfo(pycurl.HTTP_CODE)
	curl.close()
	return code

if __name__ == "__main__":
	code = delete_index(sys.argv[1], sys.argv[2])
	if code != 200:
		print code
		sys.exit(code)
