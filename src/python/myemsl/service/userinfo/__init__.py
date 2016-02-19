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

def userinfo(user, dtype, writer):
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
    data = myemsl.metadata.get_user_info(user)
    global_instruments = {}
    global_proposals = {}
    custodian_instruments = []
    ##
    # apply all proposals attached to instruments that the user is a
    # custodian on.
    ##
    custodian_instruments = myemsl.metadata.get_custodian_instruments(user)
    for instrument_id in custodian_instruments:
        global_instruments[instrument_id] = 1
    for proposal_id in myemsl.metadata.get_proposals_from_instrument_user(user):
        global_proposals[proposal_id] = 1
    ##
    # Get the proposals the user is on
    ##
    for proposal_id in myemsl.metadata.get_proposals_from_user(user):
        global_proposals[proposal_id] = 1
    ##
    # get proposal information from EUS for proposals
    ##
    for proposal_id in global_proposals.keys():
        data["proposals"][str(proposal_id)] = myemsl.metadata.get_proposal_info(proposal_id)
        inst_list = myemsl.metadata.get_instruments_from_proposal(proposal_id)
        inst_list.extend(custodian_instruments)
        data["proposals"][str(proposal_id)]["instruments"] = inst_list
        for instrument_id in inst_list:
            global_instruments[instrument_id] = 1
    ##
    # get instrument information from EUS for instruments
    ##
    for instrument_id in global_instruments.keys():
        data["instruments"][str(instrument_id)] = myemsl.metadata.get_instrument_info(instrument_id)
    formatdata(dtype, data, writer)
    return 0

if __name__ == '__main__':
    sys.exit(userinfo(int(sys.argv[1]), sys.argv[2], sys.stdout))

