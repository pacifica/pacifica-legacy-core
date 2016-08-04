#!/usr/bin/python
"""
This is the User Info service that does the work of gathering user info from SQL.
"""
import os
import sys
import errno
import urllib
import myemsl.metadata
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand
from myemsl.policy import get_policy_userinfo

def error(dtype, message, writer):
    """
    This is a generic error helper function to output error messages in the appropriate form.
    """
    if dtype == 'text/xml':
        writer.write("<?xml version=\"1.0\"?><myemsl><error message=\"%s\"/></myemsl>\n" %(message))
    elif dtype == 'text/html':
        brand('header', writer)
        brand('middle', writer)
        writer.write("%s" %(message))
        brand('footer', writer)
    elif dtype == 'application/json':
        writer.write("{'error':'"+message+"'}")
    else:
        writer.write(message)


def formatdata(dtype, data, writer):
    """
    This is the format output function to send data to the user in the requested format.
    Supports only JSON for now.
    """
    if dtype == 'application/json':
        try:
            import json
        except ImportError, ex:
            print "Unable to import json (%s)"%(ex)
            import simplejson as json
        writer.write(json.dumps(data))
    else:
        error(dtype, "Unsupported Accept Type", writer)

def userinfo(userid, dtype, writer):
    """
    This does the bulk of the SQL to gather the appropriate data to send back to the user.
    Currently it consists of the:
     * EUS user information
     * EUS custodian table for instruments
     * EUS proposals for the user
     * EUS instruments for those proposals
    """
    ##
    # get user information from EUS
    ##
    data = get_policy_userinfo(userid)
    formatdata(dtype, data, writer)
    return 0

if __name__ == '__main__':
    sys.exit(userinfo(int(sys.argv[1]), sys.argv[2], sys.stdout))

