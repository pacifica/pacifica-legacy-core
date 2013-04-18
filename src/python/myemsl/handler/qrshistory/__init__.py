from mod_python import apache
from mod_python import util

from myemsl.service import qrshistory

def handler(req):
	req.content_type = "text/xml"
	number = req.path_info.split('/', 3)[2]
	type = req.path_info.split('/', 3)[3]
	qrshistory.qrshistory(req.user, number, type, req)
	return apache.OK

