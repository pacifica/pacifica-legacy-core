#!/usr/bin/env python

from mod_python import apache
from mod_python import util
from myemsl.getuserremote import *

def authzhandler(req):
	"""This handles authorization"""
	try:
		user = get_user_remote(req.user)
		if user:
			req.user = user
			return apache.OK
		else:
			util.redirect(req, "/myemsl/error/nopersonid")
			return apache.UNAUTHORIZED
	except Exception, e:
		pass
	return apache.HTTP_INTERNAL_SERVER_ERROR
