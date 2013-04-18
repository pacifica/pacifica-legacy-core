from mod_python import apache
import urllib
from myemsl.service.sstp.preallocate import preallocate_req, Preallocate_Error

subdir_root = '../myemsl/staging'

def handler(req):
	req.content_type = "text/plain"
	preallocate_req(req)
	return apache.OK
