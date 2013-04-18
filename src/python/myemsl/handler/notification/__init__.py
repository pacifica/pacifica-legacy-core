# Author: Brock Erwin
# Description: Apache python module that handles notification requests
#              from a client.  To be more specific, there are two modes
#              of operation.
#              GET: Server will return a list of proposals and their
#                   respective notification preferences per proposal
#              POST: Client can set per proposal notification prefe-
#                    rences.
from mod_python import apache
from cgi import parse_qs, escape
import sys,traceback
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.service import notification
from myemsl.logging import getLogger
logger = getLogger(__name__)

def handler(req):
#	req.write('user is: %s \n' % req.user)
	# Generic try-catch block to prevent server from crashing
	try:
		logger.debug( 'handler:notification' )
		if req.method == "GET":
			notification.getnotifications(req.user, req)
		elif req.method == "POST":
				notification.setnotifications(req.user, parse_qs(req.read()))
		else:
			return apache.HTTP_NOT_IMPLEMENTED
		return apache.OK
	except Exception, e:
		req.write(str(e))
		logger.debug(str(traceback.format_exc()))
		return apache.HTTP_INTERNAL_SERVER_ERROR
