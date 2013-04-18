from mod_python import apache
import urllib
from myemsl.service import transaction

def handler(req):
	req.content_type = "text/xml"
	user = req.path_info.split('/', 2)[2]
	transaction.transaction(user, req)
	return apache.OK
