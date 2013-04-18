from mod_python import apache
from mod_python import Cookie
from myemsl.service.admin import switchuser

from myemsl.getconfig import getconfig
config = getconfig()

def handler(req):
	req.content_type = "text/json"
	all_cookies = Cookie.get_cookies(req)
	session_id = all_cookies.get(config.get('session', 'cookie_name'), None)
	if req.method != "POST":
		return 400
	if session_id == None:
		return apache.HTTP_UNAUTHORIZED
	try:
		url = req.path_info.split('/', 2)[2]
	except:
		return 400
	res = switchuser.switch_user(session_id.value, url, req)
	if res == 200:
		return apache.OK
	return res

