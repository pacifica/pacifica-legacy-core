from mod_python import apache

from myemsl.service import itemauth

def handler(req):
	item_id = req.path_info[1:]
	type = None
	req.content_type = "plain/text"
	code = itemauth.itemauth(req.user, item_id, req)
	if code == 200:
		return apache.OK
	return code

