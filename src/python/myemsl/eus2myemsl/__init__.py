#!/usr/bin/env python
from mod_python import apache
from mod_python import util
from myemsl import eus2login
from myemsl import pam
from myemsl import getuserremote
import os
import grp
import errno

from myemsl.logging import getLogger

logger = getLogger(__name__)

def authenhandler(req):
	logger.info("Authentication username: %s", req.user)
	password = req.get_basic_auth_pw()
	if req.user == None:
		util.redirect(req, "/myemsl/error/nopersonid")
		return apache.HTTP_UNAUTHORIZED
	user = req.user
	if user.find('@') != -1:
#FIXME Make this fail on error better
		res = eus2login.eus2login(user, password)
		if not res.has_key('person_id') or not res['person_id']:
			return apache.HTTP_UNAUTHORIZED
		logger.info("Authentication username: %s personid: %s", req.user, res['person_id'])
#FIXME add myemsl_id mapping in when we have it
		req.user = res['person_id']
	else:
		service = 'myemsl'
		auth = pam.BasicPAMAuth(service, user, password)
		if not auth.authenticated:
			return apache.HTTP_UNAUTHORIZED
		newuser = getuserremote.get_user_remote(user, map='fs_map')
		if not newuser:
			logger.error("Failed to get user id for user %s", user)
			return apache.HTTP_UNAUTHORIZED
		req.user = newuser
	return apache.OK
