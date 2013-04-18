from myemsl import queryengine
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

	queryengine.base_query(path_info, req)
	response_headers = [('Content-type', 'text/xml'),
	                    ('Content-Length', str(len(req.data)))]
	start_response(status, response_headers)
	return [req.data]
