#!/usr/bin/python

import urllib
import pycurl
import re

class AHandler:
	def __init__(self):
		self.data = ""
	def body(self, buf):
		self.data += buf

def eus_auth(encusername, password):
	
	foo = AHandler()
	data = urllib.urlencode({'encodedUserId':encusername, 'password':password})
	c = pycurl.Curl()
#	c.setopt(pycurl.PROXY, "localhost:10000")
#	c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
	c.setopt(pycurl.URL, "https://eus.emsl.pnl.gov/Portal/portal/portal_login_external_action.jsp")
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, data)
	c.setopt(pycurl.COOKIEJAR, 'mycookies.txt')
	c.setopt(pycurl.WRITEFUNCTION, foo.body)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.setopt(pycurl.MAXREDIRS, 5)
	c.perform()
	c.setopt(pycurl.POST, 0)
	c.setopt(pycurl.POSTFIELDS, '')
	c.setopt(pycurl.URL, "https://eus.emsl.pnl.gov/Portal/portal/portal_banner.jsp")
	foo.data = ''
	c.perform()
	m = re.search('<span id="welcomeText">Welcome, <span id="name"></span>.</span>', foo.data)
	if not m:
		login = True
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, 'target=content')
		c.setopt(pycurl.URL, "https://eus.emsl.pnl.gov/Portal/portal/portal_logout_action.jsp")
		foo.data = ''
		c.perform()
	else:
		login = False
	return login

if __name__ == '__main__':
	import sys
	import base64
	import getpass
	user = sys.argv[1]
	password = getpass.getpass()
	login = eus_auth(base64.b64encode(user), password)
	if login:
		print "User %s good." %(user)
	else:
		print "User %s bad." %(user)
