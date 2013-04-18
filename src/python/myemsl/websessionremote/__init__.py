#!/usr/bin/env python

import re
import sys
import pgdb
import pycurl
import urllib
import StringIO
import ConfigParser
import tempfile
from myemsl.logging import getLogger
from myemsl.getconfig import getconfig

logger = getLogger(__name__)

class web_session_remote:
	def __init__(self):
		try:
			self.cookie_file = None
			self.cookie_jar = None
			self.data = StringIO.StringIO()
			self.curl = None
			self.init_curl()
			self.logout_url = None
			self.logout_url_re = re.compile('https?://[^/]*', re.I)
		except Exception, e:
			logger.error("%s", e)
			raise e
		return None
	def __del__(self):
		self.close()
	def init_curl(self, config=None):
		if config == None:
			config = getconfig()
		if not self.cookie_file:
			self.cookie_file = tempfile.NamedTemporaryFile()
			self.cookie_jar = self.cookie_file.name
		self.curl = pycurl.Curl()
		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 5)
		self.curl.unsetopt(pycurl.CAPATH)
		self.curl.setopt(pycurl.CAINFO, '/etc/pki/tls/certs/ca-bundle.crt')
		pycurl_httpauth = pycurl.HTTPAUTH_GSSNEGOTIATE
		self.curl.setopt(pycurl.USERPWD, ":")
		self.curl.setopt(pycurl.HTTPAUTH, pycurl_httpauth)
		self.curl.setopt(pycurl.COOKIEJAR, self.cookie_jar)
		self.curl.setopt(pycurl.COOKIEFILE, self.cookie_jar)
		self.curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		self.curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')

		return self.curl
	def get(self, url, reconnect=True):
		try:
			match = self.logout_url_re.match(url)
			if match:
				self.logout_url = "%s/myemsl/logout" %(match.group(0))
			if reconnect:
				self.init_curl()
			self.data.truncate(0)
			self.curl.setopt(pycurl.URL, url)
			self.curl.setopt(pycurl.WRITEFUNCTION, self.data.write)
			self.curl.perform()
			self.data.seek(0)
			return self.data
		except Exception, e:
			logger.error("%s", e)
			raise e
		return None
	def getstatus(self):
		return self.curl.getinfo(pycurl.HTTP_CODE)
	def close(self):
		if self.curl and self.logout_url:
			try:
				logger.debug("Logging out %s", self.logout_url)
				self.data.truncate(0)
				self.curl.setopt(pycurl.URL, self.logout_url)
				self.curl.setopt(pycurl.WRITEFUNCTION, self.data.write)
				self.curl.perform()
				self.data.seek(0)
			except Exception, e:
				logger.error("%s", e)
				raise
		self.curl = None
		self.cookie_file = None
		self.cookie_jar = None

if __name__ == '__main__':
	wsr = web_session_remote()
	data = wsr.get(sys.argv[1])
	print data.read()
	data = wsr.get(sys.argv[1])
	print data.read()
