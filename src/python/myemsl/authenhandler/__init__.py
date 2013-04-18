#!/usr/bin/env python
from mod_python import apache
from mod_python import Cookie
import os
import re
import grp
import pgdb
import errno
import random
import urllib
import hashlib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.logging import getLogger

logger = getLogger(__name__)

def redirect(req, location):
	req.err_headers_out["Location"] = location
	req.status = apache.HTTP_MOVED_TEMPORARILY
	req.write('<p>The document has moved <a href="%s">here</a></p>' %(location))

def general_authenhandler(req, req_type):
	pw = req.get_basic_auth_pw()
	cookies = Cookie.get_cookies(req)
	if not cookies.has_key('csrftoken'):
		cookie = Cookie.Cookie('csrftoken', hashlib.md5(str(random.randrange(0, 2<<63))).hexdigest())
		cookie.path = '/'
		if config.get('session', 'cookie_host') != '':
			cookie.domain = config.get('session', 'cookie_host')
		Cookie.add_cookie(req, cookie)
	if cookies.has_key('myemsl_session'):
		sql = "select user_name from myemsl.eus_auth where session_id = %(sid)s"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		cursor.execute(sql, {'sid':cookies['myemsl_session'].value})
		rows = cursor.fetchall()
		found = False
		for row in rows:
			req.user = row[0]
			found = True
		if found:
			logger.debug("Session: %s", str(cookies['myemsl_session'].value))
			return outage_check(req, req_type)
	url = urllib.quote(req.unparsed_uri)
	redirect(req, "/myemsl/auth?url=%s" %(url))
	return apache.HTTP_UNAUTHORIZED

def outage_type(req):
	logger.debug(req.unparsed_uri)
	matchers = []
	try:
		for x in sorted(os.listdir('/usr/lib/myemsl/apache/outage.d')):
			if x[len(x)-2:] == '.d':
				type = x[:len(x)-2]
				for y in os.listdir('/usr/lib/myemsl/apache/outage.d/%s' %(x)):
					tf = open('/usr/lib/myemsl/apache/outage.d/%s/%s' %(x, y), 'r')
					for line in tf.readlines():
						line = line.strip()
						matchers.append({'regex':line, 'type':type})
	except OSError, e:
		if e.errno != errno.ENOENT:
			raise
	logger.debug(str(matchers))
	type = ''
	for x in matchers:
		logger.debug("Matching %s against %s\n" %(req.unparsed_uri, x['regex']))
		match = re.search(x['regex'], req.unparsed_uri)
		if match != None:
			type = "/%s" %(x['type'])
			break
		else:
			type = ""
	logger.debug("%s", type)
	return type

def outage_check(req, req_type):
	logger.debug("Outage check start")
	try:
		inited = False
		try:
			stat = os.stat('/dev/shm/myemsl/inited')
			if stat.st_uid == 0:
				inited = True
		except OSError, e:
			if e.errno != errno.ENOENT and e.errno != errno.EACCES:
				raise
		if not inited:
			type = outage_type(req)
			if type != '/ignore':
				req.internal_redirect("/myemsl/outage%s" %(type))
				return apache.HTTP_INTERNAL_SERVER_ERROR
		#If req_type is storage, you only care if myemsl is offline. Else, you care if either.
		try_list = ['/dev/shm/myemsl/outage/myemsl']
		if req_type != 'storage':
			try_list.append('/dev/shm/myemsl/outage/storage')
		for file in try_list:
			try:
				stat = os.stat(file)
				if stat.st_uid == 0:
					type = outage_type(req)
					if type != '/ignore':
						logger.debug("redirecting to outage type %s" %(type))
						req.internal_redirect("/myemsl/outage%s" %(type))
						return apache.HTTP_INTERNAL_SERVER_ERROR
			except OSError, e:
				if e.errno != errno.ENOENT and e.errno != errno.EACCES:
					raise
		return apache.OK
	except Exception, e:
		logger.error(str(e))
		pass
	logger.error("Internal error")
	return apache.HTTP_INTERNAL_SERVER_ERROR
