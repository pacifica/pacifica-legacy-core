#!/usr/bin/env python

from myemsl.authzpersondir import *

def authzhandler(req):
	return general_authzhandler(req, position=5)
