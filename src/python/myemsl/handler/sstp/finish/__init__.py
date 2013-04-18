from mod_python import apache
import urllib
from myemsl.service.sstp.finish import finish_req, Finish_Error

def handler(req):
	req.content_type = "text/plain"
	(err, msg) = finish_req(req.user, req.path_info.split('/')[4:])
	if err:
		req.write(msg+"\n")
	else:
		req.write(msg+"\nAccepted\n")
	return apache.OK
