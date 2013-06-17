#!/usr/bin/python
from mod_python import apache

from myemsl.service import reprocess

def handler(req):
	req.content_type = "text/xml"
	req.write(reprocess.reprocess(req.user, req.path_info.split('/')[2], req.method, req.read()))
	return apache.OK

