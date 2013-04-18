#!/usr/bin/env python
from mod_python import apache
from mod_python import util
from mod_python import Cookie
import os
import grp
import errno
import urllib
import myemsl.service.auth

from myemsl.getconfig import getconfig
config = getconfig()

from myemsl.logging import getLogger

logger = getLogger(__name__)

def cookie_and_redirect(req, session_id, url):
	cookie = Cookie.Cookie(config.get('session', 'cookie_name'), session_id)
	cookie.path = '/'
	if config.get('session', 'cookie_host') != '':
		cookie.domain = config.get('session', 'cookie_host')
	Cookie.add_cookie(req, cookie)
	util.redirect(req, "%s" %(urllib.unquote(url)))

def handler(req):
	res = {}
	try:
		session_id = myemsl.service.auth.session_add(req.user)
	except:
		logger.error("Failed to add session for some reason")
		return apache.HTTP_UNAUTHORIZED
	get = {}
	for item in req.subprocess_env['QUERY_STRING'].split('&'):
		try:
			t = item.split('=', 1)
			get[t[0]] = t[1]
		except:
			pass
	cookie_and_redirect(req, session_id, "%s" %(urllib.unquote(get.get("url", "/myemsl/files"))))
	return apache.HTTP_FORBIDDEN
