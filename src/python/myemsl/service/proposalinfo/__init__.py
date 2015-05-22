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

def proposalinfo(proposal_id, dtype, writer):
    """
    This does the bulk of the SQL to gather the appropriate data to send back to the user.
    Currently it consists of the:
     * EUS proposal information
     * EUS users in the proposal
     * EUS instruments in the proposal
    """
    ##
    # get proposal information from EUS
    ##
    data = myemsl.metadata.get_proposal_info(proposal_id)
    ##
    # get members of the propsal and return their info
    ##
    data["members"] = {}
    user_list = myemsl.metadata.get_users_from_proposal(proposal_id)
    for person_id in user_list:
        data["members"][str(person_id)] = myemsl.metadata.get_user_info(person_id)
    ##
    # get instrument information from EUS for instruments
    ##
    data["instruments"] = {}
    inst_list = myemsl.metadata.get_instruments_from_proposal(proposal_id)
    for instrument_id in inst_list:
        data["instruments"][str(instrument_id)] = myemsl.metadata.get_instrument_info(instrument_id)
    formatdata(dtype, data, writer)
    return 0

if __name__ == '__main__':
    sys.exit(userinfo(sys.argv[1], sys.argv[2], sys.stdout))

