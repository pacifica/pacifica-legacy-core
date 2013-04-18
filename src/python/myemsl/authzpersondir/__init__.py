#!/usr/bin/env python
# http://www.thoughtspark.org/node/25
# http://www.modpython.org/pipermail/mod_python/2006-April/020966.html
#curl -T /home/kfox/Desktop/ISDE.desktop -u kfox http://localhost:8080/kfox/

from mod_python import apache
from mod_python import util
import os
import grp
import errno
import myemsl.getunixuser

def general_authzhandler(req, position=4):
	"""This handles authorization"""
	list = req.uri.split('/', position + 1)
	if list == None:
		apache.log_error("URL Was unsplitable", apache.APLOG_CRIT)
		return apache.HTTP_FORBIDDEN
	if len(list) < position:
		apache.log_error("Root", apache.APLOG_DEBUG)
		return apache.HTTP_FORBIDDEN
	apache.log_error("Authzpersondirhandler %s %s %s" %(list[position - 1], req.uri, req.user), apache.APLOG_DEBUG)
	if(list[position - 1] == req.user):
		return apache.OK
	return apache.HTTP_FORBIDDEN
