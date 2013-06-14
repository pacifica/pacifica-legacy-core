#!/usr/bin/env python

import os
from myemsl.authenhandler import *

def authenhandler(req):
	return general_authenhandler(req, 'myemsl', anon_ok=True)
