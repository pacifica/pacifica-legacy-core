from mod_python import apache, util
import urllib
from myemsl.service import queryengine

def handler(req):
	req.content_type = "text/xml"
	try:
		url = urllib.unquote_plus(req.path_info).split('/', 2)[2]
	except:
		url = ''
	url = "%s/%s" %(req.user, url)
	request_data = util.FieldStorage(req, keep_blank_values=True)
	auth_add = request_data.getfirst("auth")
	if auth_add == "":
		auth_add = True
	else:
		auth_add = False
	op = request_data.getfirst("op")
	if op == "" or op == None:
		op = 'readdir'
	queryengine.base_query(url, op, auth_add, req)
	return apache.OK

