from mod_python import apache

from myemsl.service import getuser

def handler(req):
	req.content_type = "text/xml"
	try:
		url = req.path_info.split('/', 2)[2]
	except:
		url = ''
	getuser.get_user_base(url, req)
	return apache.OK

