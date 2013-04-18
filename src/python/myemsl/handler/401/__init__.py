from mod_python import apache
from myemsl.brand import brand
import urllib

def handler(req):
	req.content_type = "text/html"
        brand('header', req)
	location = "https://%s%s" %(req.hostname, req.subprocess_env['REQUEST_URI'])
	req.write("<meta http-equiv=\"refresh\" content=\"0;url=%s\">" %(location))
        brand('middle', req)
	req.write("To login, you must go <a href=\"%s\">here.</a>" %(location))
        brand('footer', req)
	return apache.DONE
