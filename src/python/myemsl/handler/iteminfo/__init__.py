from mod_python import apache

from myemsl.service import iteminfo

def handler(req):
	bits = req.path_info.split('/', 3)
	item_id = bits[2]
	type = None
	if len(bits) > 3:
		type = bits[3]
		req.content_type = "text/xml"
	else:
		req.content_type = "text/html"
	iteminfo.iteminfo(req.user, item_id, type, req)
	return apache.OK

