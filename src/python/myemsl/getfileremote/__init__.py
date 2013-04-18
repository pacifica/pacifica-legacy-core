#!/usr/bin/env python

import sys
import pycurl
import urllib
import ConfigParser
import xml.dom.minidom
import StringIO
from myemsl import websessionremote
from myemsl.logging import getLogger

logger = getLogger(__name__)

def get_file_remote(server, filename, protocol="http", web_session_remote=None):
	"""Get remote myemsl file"""
	newuser = None
	try:
		filename = urllib.quote_plus(filename, safe='/')
		array = filename.rsplit('/', 1)
		if len(array) > 1:
			dir = array[0]
			file = array[1]
		else:
			dir = '/'
			file = filename
		url = "%s://%s/myemsl/files-basic/index.php?dir=%s&file=%s" %(protocol, server, dir, file)
		if web_session_remote == None:
			web_session_remote = websessionremote.web_session_remote()
		data = web_session_remote.get(url)
		return data.read()
	except Exception, e:
		logger.error("%s", e)
		raise
	return None

if __name__ == '__main__':
	print get_file_remote(sys.argv[1], sys.argv[2])
