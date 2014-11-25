from mod_python import apache

from myemsl.service import userinfo

def handler(req):
	bits = req.path_info.split('/', 3)
	item_id = bits[2]
	type = None
	if len(bits) > 3:
		type = bits[3]
		req.content_type = type
	else:
		req.content_type = "application/json"
	userinfo.userinfo(req.user, type, req)
	return apache.OK

