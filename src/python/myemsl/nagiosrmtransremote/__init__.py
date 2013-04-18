#!/usr/bin/env python

import sys
import pycurl
import urllib
import ConfigParser
import StringIO
from myemsl.logging import getLogger
from myemsl import websessionremote

logger = getLogger(__name__)

def nagios_rm_trans_remote(transaction, web_session_remote=None):
	"""This lets you remotely delete a nagios transaction"""
	try:
#FIXME which host to remove from
		url = "https://a3.my.emsl.pnl.gov/myemsl/nagiosrmtrans/%s" %(transaction)
		if web_session_remote == None:
			web_session_remote = websessionremote.web_session_remote()
		data = web_session_remote.get(url)
		d = data.read()
		if d == 'OK\n':
			return True
		raise Exception(d)
	except Exception, e:
		logger.error("%s", e)
		raise e
	return None

if __name__ == '__main__':
	print nagios_rm_trans_remote(sys.argv[1])
