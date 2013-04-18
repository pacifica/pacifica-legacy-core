from mod_python import apache

from myemsl.service import outage

def handler(req):
	try:
		type = req.path_info.split('/', 2)[2]
	except:
		type = ''
	req.status = apache.HTTP_SERVICE_UNAVAILABLE
	req.content_type = outage.outage_mime(type)
	outage.outage(type, req)
	return apache.OK

