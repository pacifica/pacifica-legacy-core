#!/usr/bin/env python

import sys
from myemsl.callcurl import call_curl, CurlException
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
		url = "%s%s/%s" %(config.get('getuser', 'prefix'), config.get('getuser', map), urllib.quote(username))
		writebody = call_curl(url, capath='/etc/pki/tls/certs/ca-bundle.crt')
		logger.info(writebody)
		dom = xml.dom.minidom.parseString(writebody)
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
