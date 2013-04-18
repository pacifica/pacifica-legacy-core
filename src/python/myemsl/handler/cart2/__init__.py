from mod_python import apache, util
import urllib

from myemsl.service import cart2
import myemsl.util

from myemsl.logging import getLogger
logger = getLogger(__name__)

def handler(req):
	req.content_type = "application/json; charset=UTF-8"
	bits = req.path_info.split('/', 3)
	bits = [x for x in bits if x != '']
	if req.method == "DELETE":
		if len(bits) <= 1:
			return apache.OK
		cart_id = bits[1]
		code = cart2.cartdel(req.user, req, cart_id)
	elif req.method == "POST":
		cart_id = None
		submit = False
		resubmit = False
		email_addr = ""
		if len(bits) > 1:
			cart_id = bits[1]
			logger.debug("request: %s" %(bits))
			req.add_common_vars()
			getvars = req.subprocess_env['QUERY_STRING'].split('&')
			for item in getvars:
				i = item.split('=', 1)
				if i[0] == "submit":
					submit = True
				elif i[0] == "email_addr":
					email_addr = i[1]
				elif i[0] == "resubmit":
					resubmit = True
		if resubmit:
			code = cart2.cartresubmit(req.user, req, cart_id)
		elif submit:
			code = cart2.cartsubmit(req.user, req, cart_id, email_addr)
		else:
			code = cart2.cartadd(req.user, req, cart_id)
	elif req.method == "GET":
		logger.debug("reqlen: %s %s" %(len(bits), bits))
		req.add_common_vars()
		getvars = req.subprocess_env['QUERY_STRING'].split('&')
		state = None
		for item in getvars:
			i = item.split('=', 1)
			detail = False
			if i[0] == "state":
				state = i[1]
			if i[0] == "detail":
				if len(i) > 1:
					detail = myemsl.util.string_to_bool(i[1])
				else:
					detail = True
		if state != 'admin':
			cart_id = None
			if len(bits) >= 2:
				if len(bits) >= 3:
					return apache.HTTP_NOT_IMPLEMENTED
				cart_id = bits[1]
			code = cart2.cartsget(req.user, req, cart_id=cart_id, detail=detail)
		else:
			if len(bits) >= 2:
				return apache.HTTP_NOT_IMPLEMENTED
			code = cart2.cartsadminget(req.user, req)
	else:
		return apache.HTTP_NOT_IMPLEMENTED
	if code == 200:
		return apache.OK
	if code == 401:
		return apache.UNAUTHORIZED
	if code == 401:
		return apache.FORBIDDEN
	return code
