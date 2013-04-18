#!/usr/bin/python

import os
import sys
import atexit
import tempfile

_myemsl_keytab_cache = None

def load_keytab(keytab, user):
	global _myemsl_keytab_cache
	if _myemsl_keytab_cache == None:
		_myemsl_keytab_cache = tempfile.NamedTemporaryFile()
		atexit.register(_myemsl_keytab_cache.close)
	os.environ['KRB5CCNAME'] = _myemsl_keytab_cache.name
	res = os.system("/usr/kerberos/bin/kinit -5 -k -t %s %s" %(keytab, user))
	if res != 0:
		raise Exception("Failed to kinit")

if __name__ == '__main__':
	load_keytab(sys.argv[1], sys.argv[2])
	os.system("/usr/kerberos/bin/klist")
