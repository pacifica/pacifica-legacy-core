#!/usr/bin/env python

import sys
import pycurl
import urllib
import StringIO
import ConfigParser
import xml.dom.minidom
import tempfile
from myemsl import websessionremote
from myemsl.logging import getLogger

logger = getLogger(__name__)

def get_status_remote(url, web_session_remote=None):
	"""This handles authorization"""
	newuser = None
	try:
		url = "%s/xml" %(url)
		if web_session_remote == None:
			web_session_remote = websessionremote.web_session_remote()
		data = web_session_remote.get(url)
		dom = xml.dom.minidom.parseString(data.read())
		return dom
	except Exception, e:
		logger.error("%s", e)
		raise e
	return None

if __name__ == '__main__':
	print get_status_remote(sys.argv[1]).toxml()
