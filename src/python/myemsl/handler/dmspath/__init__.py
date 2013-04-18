from mod_python import apache, util
import urllib
from myemsl.service import dmspath

def handler(req):
	req.content_type = "text/json"
	try:
		import sys
		sys.stderr.write("PI: %s\n" %(req.path_info))
		url = urllib.unquote_plus(req.path_info).split('/', 2)[1]
	except:
		url = ''
	request_data = util.FieldStorage(req, keep_blank_values=True)
	auth_add = request_data.getfirst("auth")
	if auth_add == "":
		auth_add = True
	else:
		auth_add = False
	dmspath.base_query(req.user, url, auth_add, req)
	return apache.OK

