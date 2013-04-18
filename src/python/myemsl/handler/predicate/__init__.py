from mod_python import apache
from mod_python import util

from myemsl.service import predicate

import sys

def handler(req):
	pi = req.path_info.split('/', 2)
	if len(pi) < 2:
		path = ""
	else:
		path = pi[1]
	predicate.predicate(req.user, path, req.method, req, req)
	return apache.OK

