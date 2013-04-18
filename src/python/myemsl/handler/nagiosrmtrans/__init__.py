from mod_python import apache

from myemsl.service import nagiosrmtrans

def handler(req):
	req.content_type = "text/plain"
	try:
		transaction = req.path_info.split('/', 2)[2]
		nagiosrmtrans.nagios_rm_trans(transaction, req)
	except Exception, e:
		req.write(str(e))
	return apache.OK
