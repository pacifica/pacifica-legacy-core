#!/usr/bin/python

import binascii

def encode(s):
	s = s.replace('-', '')
	s = binascii.unhexlify(s)
	s = s.encode('base64')
	s = s.replace('=', '')
	s = s.replace('\n', '')
	return s

def decode(s):
	s = s + '=='
	s = s.decode('base64')
	s = binascii.hexlify(s)
	s = "%s-%s-%s-%s-%s" %(s[0:8], s[8:12], s[12:16], s[16:20], s[20:32])
	return s

if __name__ == "__main__":
	s = '86e60dc2-9b58-11e1-b30c-0026b9c7a9cf'
	e = encode(s)
	print e
	s2 = decode(e)
	print s, s2
	print s == s2
