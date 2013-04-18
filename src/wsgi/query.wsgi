import authz
import sys

class foo:
	def __init__(self):
		self.data = ''
	def write(self, data):
		self.data = self.data + data

def application(environ, start_response):
	status = '200 OK'
	req = foo()

	path_info = environ['PATH_TRANSLATED'][len(environ['DOCUMENT_ROOT']):]
#	sys.stderr.write(path_info)
#	sys.stderr.flush()

	path_info = "/%s%s" %(environ['REMOTE_USER'], path_info)
	authz.tauth(path_info, environ['REMOTE_USER'], req)
	response_headers = [('Content-type', 'text/xml'),
	                    ('Content-Length', str(len(req.data)))]
	start_response(status, response_headers)
	return [req.data]
