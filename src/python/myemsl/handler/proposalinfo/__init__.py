#!/bin/bash -xe
"""
User info handler ment to be called from mod_python embedded in apache.
"""
from mod_python import apache

from myemsl.service import proposalinfo

def handler(req):
    """
    This is the mod python handler to split the url and call service method.
    """
    if 'Accept' in req.headers_in:
        accept_types = req.headers_in['Accept'].split(',')
        accept_types = [ a.split(';')[0] for a in accept_types ]
        if '*/*' in accept_types:
            dtype = "application/json"
        else:
            dtype = accept_types[0]
    else:
        dtype = "application/json"
    proposalinfo.proposalinfo(str(req.path_info[1:]), dtype, req)
    return apache.OK

