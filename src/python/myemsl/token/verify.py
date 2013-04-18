#!/usr/bin/python
from M2Crypto import X509, m2
import sys

x509 = None

#FIXME Pass key in.
def verify(s, sig):
	global x509
	if x509 == None:
		x509 = X509.load_cert('/etc/myemsl/keys/item/local.crt')
	pubkey = x509.get_pubkey()
	pubkey.reset_context(md="sha256")
	pubkey.verify_init()
	pubkey.verify_update(s)
	return m2.verify_final(pubkey.ctx, sig, pubkey.pkey)
