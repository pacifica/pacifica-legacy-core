#!/usr/bin/env python
from mod_python import apache
from mod_python import Cookie

import time
import myemsl.token

from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.logging import getLogger

logger = getLogger(__name__)

def check_for_token(req):
		token = ""
		req.add_common_vars()
		getvars = req.subprocess_env['QUERY_STRING'].split('&')
		for item in getvars:
			i = item.split('=')
			if i[0] == "token" and len(i) > 1:
				token = i[1]
				break
		return token

#PATH is /myemsl/item/storageuuid/instanceuuid/itemid
def authenhandler(req):
	logger.debug("Req: %s", req.unparsed_uri)

	token = ""
	if req.headers_in.has_key('Authorization'):
		list = req.headers_in['Authorization'].split(' ')
		if list < 2 or list[0] != 'Bearer':
			token = check_for_token(req)
			if token == '':
				return apache.HTTP_UNAUTHORIZED
		else:
			token = list[1]
	else:
		token = check_for_token(req)
		if token == '':
			return apache.HTTP_UNAUTHORIZED

	req.user = ""
	pub = None
	try:
		pub, priv = myemsl.token.token_parse(token)
	except:
		pass
	if not pub:
		time.sleep(2)
		return apache.HTTP_UNAUTHORIZED
	logger.debug("Authorization: %s", pub)
	if 'p' in pub and pub['p'] != None:
		req.user = "%s" %(pub['p'])
	valid = myemsl.token.token_validate_time(pub)
	if not valid:
		return apache.HTTP_UNAUTHORIZED
	if not pub.has_key('i'):
		return apache.HTTP_FORBIDDEN
	path = req.unparsed_uri.split('/', 6)
	if len(path) < 6:
		logger.debug("Url too short.")
		return apache.HTTP_BAD_REQUEST
	item = path[5]
#FIXME verify instance and storage uuid. path[3] and path[4]
	try:
		item = int(item)
	except Exception, e:
		logger.debug("Item validation error: %s" %(e))
		return apache.HTTP_BAD_REQUEST
	found = False
	try:
		for i in pub['i']:
			if int(i) == item:
				found = True
				break
	except:
		return apache.HTTP_FORBIDDEN
	if not found:
		logger.debug("Item %i not found in %s", item, pub['i'])
		return apache.HTTP_FORBIDDEN
	logger.debug("Item %i is authorized.", item)
	return apache.OK
	return apache.HTTP_UNAUTHORIZED
