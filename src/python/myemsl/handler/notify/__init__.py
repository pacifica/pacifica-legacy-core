from mod_python import apache

from myemsl.service import notify

def handler(req):
	req.content_type = "text/html"
	transaction = int(req.path_info[1:])
	notify.notify(transaction, req)
	return apache.OK

