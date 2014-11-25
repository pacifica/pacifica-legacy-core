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
    bits = req.path_info.split('/', 3)
    dtype = None
    if len(bits) > 2:
        dtype = bits[2]
        req.content_type = type
    else:
        req.content_type = "application/json"
    userinfo.userinfo(req.user, dtype, req)
    return apache.OK

