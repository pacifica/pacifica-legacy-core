from mod_python import apache

from myemsl.service import itemauth

def handler(req):
	bits = req.path_info.split('/', 3)
	item_id = bits[2]
	type = None
	req.content_type = "plain/text"
	code = itemauth.itemauth(req.user, item_id, req)
	if code == 200:
		return apache.OK
	return code

