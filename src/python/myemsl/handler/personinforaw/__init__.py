from mod_python import apache

from myemsl.service import personinfo

def handler(req):
	bits = req.path_info.split('/', 3)
	person_id = bits[2]
	type = None
	if len(bits) > 3:
		type = bits[3]
		req.content_type = "text/xml"
	else:
		req.content_type = "text/html"
	personinfo.personinfo(req.user, person_id, type, req)
	return apache.OK

