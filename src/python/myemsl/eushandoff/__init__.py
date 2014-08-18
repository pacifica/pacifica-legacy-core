#!/usr/bin/env python

import sys
import pgdb
import base64
import hashlib
from myemsl.callcurl import call_curl, CurlException
import random
import urllib
import tempfile
import StringIO
import xml.dom.minidom
import xml.parsers.expat
from myemsl.logging import getLogger

logger = getLogger(__name__)

from myemsl.getconfig import getconfig
config = getconfig()

def eus_user_remove(username):
	if username == None:
		raise Exception("User is None")
	isok = False
	try:
		writebody = ""
		url = "%s/%s" %(config.get('metadata', 'eus_auth'), urllib.quote(username))
		writebody = call_curl(url, method="DELETE", cainfo='/etc/pki/tls/certs/ca-bundle.crt')
		logger.info("%s", writebody)
		dom = xml.dom.minidom.parseString(writebody)
		found = False
		for x in dom.firstChild.childNodes:
			if x.nodeType == x.ELEMENT_NODE and (x.nodeName == 'status'):
				isok = (str(x.getAttribute('action')) == 'removed')
				break
	except Exception, e:
		logger.error("%s", e)
		raise
	return isok

def eus_user_add(username, results):
	if username == None:
		raise Exception("User is None")
	isok = False
	try:
		pw = str(random.getrandbits(8*32))
		m = hashlib.md5()	
		m.update(pw)
		pw = m.hexdigest()
		pdata = "%s" %(pw)
		writebody = ""
		writebody = call_curl(url, method="PUT", idata=pdata, cainfo='/etc/pki/tls/certs/ca-bundle.crt')
		logger.info("%s", writebody)
		dom = xml.dom.minidom.parseString(writebody)
		found = False
		for x in dom.firstChild.childNodes:
			if x.nodeType == x.ELEMENT_NODE and (x.nodeName == 'status'):
				isok = (str(x.getAttribute('action')) == 'added')
			if x.nodeType == x.ELEMENT_NODE and (x.nodeName == 'redirect'):
				results['proto'] = str(x.getAttribute('proto'))
				results['hostname'] = str(x.getAttribute('hostname'))
				results['path'] = str(x.getAttribute('path'))
		if isok:
			return pw
	except xml.parsers.expat.ExpatError, e:
		logger.error("%s", returned_data)
		logger.error("%s", e)
		raise
	except Exception, e:
		logger.error("%s", e)
		raise
	return None

if __name__ == '__main__':
	username = sys.argv[1]
	eus_user_remove(username)
	pw = eus_user_add(username)
	if pw:
		print "User: %s\nPassword: %s" %(username, pw)

