#!/usr/bin/python
"""
This is the User Info service that does the work of gathering user info from SQL.
"""
import os
import sys
import errno
import urllib
import myemsl.elasticsearch
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
     * EUS proposals for the user
     * EUS custodian table for instruments
     * EUS instruments for those proposals
    """
    ##
    # get user information from EUS
    ##
    sql = """
SELECT
  person_id,
  network_id,
  first_name,
  last_name,
  email_address,
  last_change_date
FROM
  eus.users
WHERE
  person_id=%(person_id)d
    """
    cnx = myemsldb_connect(myemsl_schema_versions=['1.8'])
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':user})
    rows = cursor.fetchall()
    if len(rows) != 1:
        error(dtype, "multiple users with (%s)"%(user), writer)
    (person_id, network_id, first_name, last_name, email_address, last_change_date) = rows[0]
    data = {
        "person_id": person_id,
        "network_id": network_id,
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
        "last_change_date": last_change_date,
        "proposals": {},
        "instruments": {}
    }
    global_instruments = {}
    global_proposals = {}
    ##
    # This pulls the instruments from custodians and gets
    # the associated proposals
    ##
    sql = """
SELECT
  instrument_id
FROM
  eus.emsl_staff_inst
WHERE
  person_id = %(person_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':person_id})
    for instrument_id in cursor.fetchall():
        global_instruments[instrument_id[0]] = 1
        sql = """
SELECT
  proposal_id
FROM
  eus.proposal_instruments
WHERE
  proposal_instruments.instrument_id = %(instrument_id)s
        """
        cursor = cnx.cursor()
        cursor.execute(sql, {'instrument_id':instrument_id})
        for proposal_id in cursor.fetchall():
            global_proposals[proposal_id[0]] = 1
    ##
    # Get the proposals the user is on
    ##
    sql = """
SELECT
  proposal_id
FROM
  eus.proposal_members
WHERE
  person_id = %(person_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':person_id})
    for proposal_id in cursor.fetchall():
        global_proposals[proposal_id] = 1
    ##
    # get proposal information from EUS for all proposals
    ##
    for proposal_id in global_proposals.keys():
        sql = """
SELECT
  proposal_id,
  title,
  group_id,
  accepted_date,
  actual_end_date,
  actual_start_date,
  closed_date
FROM
  eus.proposals
WHERE
  proposal_id = %(proposal_id)s
        """
        cursor = cnx.cursor()
        cursor.execute(sql, {'proposal_id':proposal_id})
        for row in cursor.fetchall():
            (
                proposal_id,
                title,
                group_id,
                accepted_date,
                actual_end_date,
                actual_start_date,
                closed_date
            ) = row
            data["proposals"][str(proposal_id)] = {
                "title": title,
                "group_id": group_id,
                "accepted_date": accepted_date,
                "actual_end_date": actual_end_date,
                "actual_start_date": actual_start_date,
                "closed_date": closed_date,
                "instruments": []
            }
            sql = """
SELECT
  instrument_id
FROM
  eus.proposal_instruments
WHERE
  proposal_instruments.proposal_id = %(proposal_id)s
            """
            cursor = cnx.cursor()
            cursor.execute(sql, {'proposal_id':proposal_id})
            data["proposals"][str(proposal_id)]["instruments"] = cursor.fetchall()
            for i in data["proposals"][str(proposal_id)]["instruments"]:
                i = i[0]
                global_instruments[i] = 1
    for instrument_id in global_instruments.keys():
        sql = """
SELECT
  instrument_id,
  instrument_name,
  last_change_date,
  name_short,
  eus_display_name,
  active_sw
FROM
  eus.instruments
WHERE
  eus.instruments.instrument_id = %(instrument_id)d
        """
        cursor = cnx.cursor()
        cursor.execute(sql, {'instrument_id':instrument_id})
        rows = cursor.fetchall()
        if len(rows) != 1:
            error(dtype, "multiple instruments with id (%s)"%(str(instrument_id)), writer)
        (
            instrument_id,
            instrument_name,
            last_change_date,
            name_short,
            eus_display_name,
            active_sw
        ) = rows[0]
        data["instruments"][str(instrument_id)] = {
            "instrument_id": instrument_id,
            "instrument_name": instrument_name,
            "last_change_date": last_change_date,
            "name_short": name_short,
            "eus_display_name": eus_display_name,
            "active_sw": active_sw
        }
    formatdata(dtype, data, writer)
    return 0

if __name__ == '__main__':
    sys.exit(userinfo(sys.argv[1], sys.argv[2], sys.stdout))

