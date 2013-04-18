from mod_python import apache

from myemsl.service import personinfo

def handler(req):
	bits = req.path_info.split('/', 2)
	type = None
	if len(bits) > 2:
		type = bits[2]
		req.content_type = "text/xml"
	else:
		req.content_type = "text/html"
	personinfo.personinfo(req.user, req.user, type, req)
	return apache.OK

