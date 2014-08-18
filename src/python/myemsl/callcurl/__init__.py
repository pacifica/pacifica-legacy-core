#!/usr/bin/python

from myemsl.getconfig import getconfig
config = getconfig()

class CurlException(Exception):
	def __init__(self, code):
		Exception.__init__(self, "HTTP_CODE: %d" %(code))
		self.http_code = code

class _BytesRecievedCounter:
	def __init__(self, writecb, bytesrecieved):
		self.counter = 0
		self.writecb = writecb
		self.bytesrecieved = bytesrecieved
	def write(self, data):
		self.counter += len(data)
		self.bytesrecieved(self.counter)
		self.writecb(data)

def call_curl(url, **kwargs):
	"""
	Input

	url - This is the url to perform the action on.
	kwargs - a hash containing some valid optional keys.

	Optional

	method - One of POST/PUT/GET/DELETE/HEAD/DOWNLOAD
	idata - Input string to send to the url valid only for PUT/POST
	content_type - Content Type for the content being sent
	accept - accept mimetype in header
	username/password - only valid together
	auth - one of negotiate, bearer, or anything else for basic
	filename - If method=DOWNLOAD, this specifies what file to download to.
	bytesrecieved - If method=DOWNLOAD, this specifies a callback getting the value of how many bytes have been downloaded.
	token - If auth=bearer, this is the token to use.
	headers - A function or dict that receives the response headers.
	getread - A function that gets called as data arives.

	insecure_peer - if defined it will use that value for SSL_VERIFYPEER. If not defined, it uses the settings from general.ini
	insecure_host - if defined it will use that value for SSL_VERIFYHOST. If not defined, it uses the settings from general.ini
	capath - if None unset otherwise set it
	cainfo - if None unset otherwise set it
	sslcert - if None unset otherwise set it
	sslcerttype - if None unset otherwise set it
        postfields - String passed to postfields if set

	This is a simple interface to curl basically you give it a string
	for input to a url and then you recieve the output string.
	"""
	import StringIO
	import pycurl
	odata = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	getread = None

	if not 'method' in kwargs or kwargs['method'] != 'DOWNLOAD':
		if 'method' in kwargs and kwargs['method'] == 'GET' and 'getread' in kwargs:
			getread = kwargs['getread']
			c.setopt(pycurl.WRITEFUNCTION, getread)
		else:
			c.setopt(pycurl.WRITEFUNCTION, odata.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.setopt(pycurl.MAXREDIRS, 5)

	map = {
		'capath':pycurl.CAPATH,
		'cainfo':pycurl.CAINFO,
		'sslcert':pycurl.SSLCERT,
		'sslcerttype':pycurl.SSLCERTTYPE
	}
	for opt in map:
		if opt in kwargs:
			if kwargs[opt] == None:
				c.unsetopt( map[opt] )
			else:
				c.setopt( map[opt], kwargs[opt] )

	for ssltype in ['peer', 'host']:
		if 'insecure_'+ssltype in kwargs:
			c.setopt( eval "pycurl.SSL_VERIFY"+ssltype.upper(), kwargs['insecure_'+ssltype )
		else:
			c.setopt( eval "pycurl.SSL_VERIFY"+ssltype.upper(), 2 if config.getboolean('webservice', 'ssl_verify_'+ssltype) else 0 )

	if 'postfields' in kwargs:
		c.setopt( pycurl.POSTFIELDS, kwargs['postfields'])

	if 'headers' in kwargs and kwargs['headers'] != None:
		h = kwargs['headers']
		try:
			h.get('0')
			def wrapperfunc(h):
				extra = ['']
				def process_line(h, line):
					a = line.split(':', 1)
					if len(a) > 1:
						v = a[1].lstrip()
						if v[len(v) - 1] == '\r':
							v = v[:len(v) - 1]
						h[a[0]] = v
				def tmpfunc(str):
					if str == None:
						if extra[0] != '':
							process_line(h, extra[0])
						return 0
					retval = len(str)
					str = extra[0] + str
					idx = str.rfind('\n')
					if idx == -1:
						extra[0] = str
					else:
						lines = str.split('\n')
						extra[0] = lines.pop()
						for line in lines:
							process_line(h, line)
					return retval
				return tmpfunc
			c.setopt( pycurl.HEADERFUNCTION, wrapperfunc(h))
		except AttributeError, e:
			c.setopt( pycurl.HEADERFUNCTION, h )

	if 'username' in kwargs and 'password' in kwargs:
		c.setopt( pycurl.USERPWD, '%s:%s'%(kwargs['username'], kwargs['password']) )

	if 'auth' in kwargs:
		if kwargs['auth'] == 'negotiate':
			c.setopt( pycurl.HTTPAUTH, pycurl.HTTPAUTH_GSSNEGOTIATE )
		elif kwargs['auth'] == 'bearer':
			c.setopt( pycurl.HTTPHEADER, ["Authorization: Bearer %s" %(kwargs['token'])])
		else:
			c.setopt( pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANY )

	idata = None
	fp = None
	if 'method' in kwargs:
		if str(kwargs['method']) == 'POST':
			c.setopt( pycurl.POST, 1 )
			if 'idata' in kwargs:
				c.setopt( pycurl.POSTFIELDS, str(kwargs['idata']) )
			else:
				c.setopt( pycurl.POSTFIELDS, "" )				
		elif str(kwargs['method']) == 'PUT':
			c.setopt( pycurl.PUT, 1 )
			tmp = None
			if 'idata' in kwargs:
				tmp = str(kwargs['idata'])
			else:
				tmp = ""
			c.setopt( pycurl.UPLOAD, 1 )
			idata = StringIO.StringIO(tmp)
			c.setopt( pycurl.READFUNCTION, idata.read )
			c.setopt( pycurl.INFILESIZE_LARGE, len(tmp) )
		elif str(kwargs['method']) == 'DELETE':
			c.setopt( pycurl.CUSTOMREQUEST, 'DELETE' )
		elif str(kwargs['method']) == 'HEAD':
			c.setopt( pycurl.NOBODY, 1 )
		elif str(kwargs['method']) == 'DOWNLOAD':
			fp = open( kwargs['filename'], "wb" )
			wcb = fp.write
			if 'bytesrecieved' in kwargs:
				brc = _BytesRecievedCounter(fp.write, kwargs['bytesrecieved'])
				wcb = brc.write
			c.setopt( pycurl.WRITEFUNCTION, wcb )
		else: # assume GET
			c.setopt( pycurl.HTTPGET, 1 )
	else: # assume GET
		c.setopt( pycurl.HTTPGET, 1 )

	header = []
	if 'content_type' in kwargs:
		header.append('Content-Type: '+str(kwargs['content_type']))
	if 'accept' in kwargs:
		header.append('Accept: '+str(kwargs['accept']))
	c.setopt(pycurl.HTTPHEADER, header)
	c.perform()
	http_code = c.getinfo( pycurl.HTTP_CODE )
	if http_code / 100 != 2:
		raise CurlException(http_code)
	if not 'method' in kwargs or kwargs['method'] != 'DOWNLOAD':
		if getread != None:
			return None
		odata.seek(0)
		return odata.read()
	else:
		if fp:
			fp.close()
		return

if __name__ == '__main__':
	import doctest
	doctest.testmod(verbose=True)

