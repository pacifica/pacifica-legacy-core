#!/usr/bin/python
from M2Crypto import EVP
import sys

privkey = None

def sign(s):
	global privkey
	if privkey == None:
#FIXME Change this to a different key.
		privkey = EVP.load_key("/etc/myemsl/keys/item/local.key")
	#FIXME lock around privkey
	#privkey = EVP.load_key("/usr/share/doc/m2crypto-0.16/tests/rsa.priv.pem")
	privkey.reset_context(md='sha256')
	privkey.sign_init()
	privkey.sign_update(s)
	signature = privkey.sign_final()
	return signature
