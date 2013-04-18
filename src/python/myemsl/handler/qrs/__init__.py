from mod_python import apache
from mod_python import util

from myemsl.service import qrs

def handler(req):
	type = req.path_info.split('/', 3)[2]
	id = req.path_info.split('/', 3)[3]
	qrs.qrscan(req.user, type, id, req)
	util.redirect(req, "/myemsl/iteminfo/%s" %(id))
	return apache.OK

