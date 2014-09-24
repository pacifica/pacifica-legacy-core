from mod_python import apache, util
import urllib

from myemsl.service import elasticsearch

def handler(req):
	bits = req.path_info.split('/', 3)
	type = bits[1]
	req.content_type = "application/json; charset=UTF-8"
	req.add_common_vars()
	getvars = req.subprocess_env['QUERY_STRING'].split('&')
	auth_add = False
	search_type = None
	scan = False
	for item in getvars:
		i = item.split('=', 1)
		if i[0] == "auth":
			auth_add = True
		if i[0] == "search_type":
			search_type = i[1]
		if i[0] == "scan":
			scan = True
	index = "myemsl_user_%s" %(req.user)
	code = elasticsearch.elasticsearchquery(req.user, index, type, req, auth_add=auth_add, search_type=search_type, scan=scan)
	if code == 200:
		return apache.OK
	return code
