#!/bin/bash -xe
"""
User info handler ment to be called from mod_python embedded in apache.
"""
from mod_python import apache

from myemsl.service import userinfo

def handler(req):
    """
    This is the mod python handler to split the url and call service method.
    """
    if 'Accept' in req.headers_in:
        dtype = req.headers_in['Accept']
    else:
        dtype = "application/json"
    userinfo.userinfo(int(req.user), dtype, req)
    return apache.OK

