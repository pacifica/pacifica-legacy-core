from mod_python import Cookie, apache, util

import time
import urllib

from myemsl.getconfig import getconfig
config = getconfig()

def cookie_and_redirect(req, session_id, url):
	cookie = Cookie.Cookie(config.get('session', 'cookie_name'), session_id)
	cookie.path = '/'
	cookie.domain = config.get('session', 'cookie_host')
	Cookie.add_cookie(req, cookie)
	util.redirect(req, "%s" %(urllib.unquote(url)))

def handler(req):
	req.content_type = "text/html"
	try:
		session_id = req.path_info.split('/', 2)[2]
	except:
		return apache.HTTP_FORBIDDEN
	get = {}
	for item in req.subprocess_env['QUERY_STRING'].split('&'):
		try:
			t = item.split('=', 1)
			get[t[0]] = t[1]
		except:
			pass
	cookie_and_redirect(req, session_id, "%s" %(urllib.unquote(get.get("url", "/myemsl/files"))))
	return apache.OK
