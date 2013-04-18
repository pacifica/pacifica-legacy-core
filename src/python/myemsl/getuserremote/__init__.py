#!/usr/bin/env python

import sys
import pycurl
import urllib
import StringIO
import xml.dom.minidom

from myemsl.getconfig import getconfig
config = getconfig()

from myemsl.logging import getLogger

logger = getLogger(__name__)

def get_user_remote(username, map='web_map'):
	"""This handles authorization"""
	newuser = None
	try:
		foo = StringIO.StringIO()
		data = []
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "%s%s/%s" %(config.get('getuser', 'prefix'), config.get('getuser', map), urllib.quote(username)))
		c.setopt(pycurl.WRITEFUNCTION, foo.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.unsetopt(pycurl.CAPATH)
		c.setopt(pycurl.CAINFO, '/etc/pki/tls/certs/ca-bundle.crt')
		c.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		c.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')

		c.perform()
		foo.seek(0)
		returned_data = foo.read()
		logger.info(returned_data)
		dom = xml.dom.minidom.parseString(returned_data)
		found = False
		for x in dom.firstChild.childNodes:
			if x.nodeType == x.ELEMENT_NODE and (x.nodeName == 'user'):
				newuser = str(x.getAttribute('id'))
				break
	except Exception, e:
		logger.error("%s", e)
		raise e
	return newuser

if __name__ == '__main__':
	print get_user_remote(sys.argv[1])
