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
        req.log_error(req.headers_in['Accept'])
        accept_types = req.headers_in['Accept'].split(',')
        accept_types = [ a.split(';')[0] for a in accept_types ]
        if '*/*' in accept_types:
            dtype = "application/json"
        else:
            dtype = accept_types[0]
    else:
        dtype = "application/json"
    userinfo.userinfo(int(req.user), dtype, req)
    return apache.OK

