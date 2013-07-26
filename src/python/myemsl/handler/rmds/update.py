from mod_python import apache, util
import urllib
import simplejson as json

from myemsl.service.rmds import update

from myemsl.logging import getLogger
logger = getLogger(__name__)

def handler(req):
	req.content_type = "application/json; charset=UTF-8"
	bits = req.path_info.split('/', 7)
	bits = [x for x in bits if x != '']
	logger.debug("FOO! %s" %len(bits))
	if len(bits) != 5:
		return apache.HTTP_BAD_REQUEST
	if req.method == "POST":
		code = update.update(bits[1], bits[2], bits[3], bits[4], req)
	else:
		return apache.HTTP_NOT_IMPLEMENTED
	if code == 200:
		return apache.OK
	if code == 401:
		return apache.UNAUTHORIZED
	if code == 401:
		return apache.FORBIDDEN
	return code
