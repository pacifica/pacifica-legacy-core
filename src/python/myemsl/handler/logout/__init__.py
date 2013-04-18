from mod_python import apache
from mod_python import Cookie
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

logger = getLogger(__name__)

#If you get here, you already have a valid session cookie.
def handler(req):
	req.content_type = 'text/html'
	cookies = Cookie.get_cookies(req)
        brand('header', req)
        brand('middle', req)
	session_id = cookies['myemsl_session'].value
#FIXME rename myemsl.eus_auth
	sql = "delete from myemsl.eus_auth where session_id=%(sid)s"
	try:
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		cursor.execute(sql, {'sid':session_id})
		cnx.commit()
		req.write("You have successfully logged out.")
	except Exception, e:
		logger.warning("Unknown exception %s", e)
		req.write("Unknown issue during logout")
        brand('footer', req)
	return apache.OK
