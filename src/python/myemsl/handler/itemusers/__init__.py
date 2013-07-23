from mod_python import apache

from myemsl.service import itemusers

def handler(req):
	bits = req.path_info.split('/', 2)
	item_id = bits[1]
	type = None
	req.content_type = "plain/json"
	code = itemusers.itemusers(item_id, req)
	if code == 200:
		return apache.OK
	return code

