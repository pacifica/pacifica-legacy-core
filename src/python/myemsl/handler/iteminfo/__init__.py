from mod_python import apache

from myemsl.service import iteminfo

def handler(req):
	bits = req.path_info.split('/', 2)
	item_id = bits[1]
	type = None
	if len(bits) > 2:
		type = bits[2]
		req.content_type = "text/xml"
	else:
		req.content_type = "text/html"
	iteminfo.iteminfo(req.user, item_id, type, req)
	return apache.OK

