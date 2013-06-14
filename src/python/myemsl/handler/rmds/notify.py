from mod_python import apache, util
import urllib
import simplejson as json

from myemsl.service.rmds import notify

from myemsl.logging import getLogger
logger = getLogger(__name__)

def handler(req):
	req.content_type = "application/json; charset=UTF-8"
	bits = req.path_info.split('/', 3)
	bits = [x for x in bits if x != '']
	if len(bits) < 3:
		return apache.HTTP_BAD_REQUEST
	if req.method == "POST":
		code = notify.notify(req.user, bits[1], bits[2])
	else:
		return apache.HTTP_NOT_IMPLEMENTED
	if code == 200:
		return apache.OK
	if code == 401:
		return apache.UNAUTHORIZED
	if code == 401:
		return apache.FORBIDDEN
	return code
