#!/usr/bin/python
from mod_python import apache

from myemsl.service import reprocess

def handler(req):
	reprocess.reprocess(req.path_info.split('/')[2], req.method, req.read())
	return apache.OK

