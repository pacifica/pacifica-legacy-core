#!/usr/bin/env python

import sys
import pgdb
import base64
import hashlib
import pycurl
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
		foo = StringIO.StringIO()
		data = []
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "%s/%s" %(config.get('metadata', 'eus_auth'), urllib.quote(username)))
		c.setopt(pycurl.WRITEFUNCTION, foo.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
		c.unsetopt(pycurl.CAPATH)
		c.setopt(pycurl.CAINFO, '/etc/pki/tls/certs/ca-bundle.crt')
		c.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		c.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')

		c.perform()
		foo.seek(0)
		returned_data = foo.read()
		logger.info("%s", returned_data)
		dom = xml.dom.minidom.parseString(returned_data)
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
		tmpfile = tempfile.TemporaryFile()
		foo = StringIO.StringIO()
		pw = str(random.getrandbits(8*32))
		m = hashlib.md5()	
		m.update(pw)
		pw = m.hexdigest()
		pdata = "%s" %(pw)
		tmpfile.write(pdata)
		tmpfile.seek(0)
		data = []
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "%s/%s" %(config.get('metadata', 'eus_auth'), urllib.quote(username)))
		c.setopt(pycurl.WRITEFUNCTION, foo.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.setopt(pycurl.PUT, 1)
		c.unsetopt(pycurl.CAPATH)
		c.setopt(pycurl.CAINFO, '/etc/pki/tls/certs/ca-bundle.crt')
		c.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		c.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
		c.setopt(pycurl.INFILE, tmpfile)
		c.setopt(pycurl.INFILESIZE, len(pdata))

		c.perform()
		foo.seek(0)
		returned_data = foo.read()
		logger.info("%s", returned_data)
		dom = xml.dom.minidom.parseString(returned_data)
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

