#!/usr/bin/python

import os
import sys
import errno
import urllib
import myemsl.elasticsearch
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

logger = getLogger(__name__)

#FIXME this code is now slower then it could be. It already has all the metadata from elasticsearch, just use it instead of db calls.

def error(type, message, writer):
	if type == 'text/xml':
		writer.write("<?xml version=\"1.0\"?><myemsl><error message=\"%s\"/></myemsl>\n" %(message))
	elif type == 'text/html':
		brand('header', writer)
		brand('middle', writer)
		writer.write("%s" %(message))
		brand('footer', writer)
	elif type == 'application/json':
		writer.write("{'error':'"+message+"'}")
	else:
		writer.write(message)


def formatdata(type, data, writer):
	if type == 'application/json':
		try:
			import json
		except:
			import simplejson as json
		writer.write(json.dumps(data))
	else:
		error(type, "Unsupported Accept Type", writer)

def userinfo(user, dtype, writer):
	type = None
	sql = """
SELECT
  person_id,
  network_id,
  first_name,
  last_name,
  email_address,
  last_change_date
FROM
  myemsl.users
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
		"proposals": {}
		"instruments": {}
	}
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
  eus.proposals,
  eus.proposal_members
WHERE
  proposal_members.proposal_id = proposals.proposal_id,
  proposal_members.person_id = %(person_id)d
	"""
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':user})
	rows = cursor.fetchall()
	global_instruments = {}
	for row in rows:
		(proposal_id, title, group_id, accepted_date, actual_end_date, actual_start_date, closed_date) = row
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
  proposal_instruments.proposal_id = %(proposal_id)d
		"""
		cursor = cnx.cursor()
		cursor.execute(sql, {'proposal_id':proposal_id})
		data["proposals"][str(proposal_id)]["instruments"] = cursor.fetchall()
		for i in data["proposals"][str(proposal_id)]["instruments"]:
			global_instruments[i] = 1
	for intstrument_id in global_instruments.keys():
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
  eus.instrument_id = %(instrument_id)d
		"""
		cursor = cnx.cursor()
		cursor.execute(sql, {'instrument_id':instrument_id})
		rows = cursor.fetchall()
		if len(rows) != 1:
			error(dtype, "multiple instruments with id (%s)"%(str(instrument_id)), writer)
		(instrument_id, instrument_name, last_change_date, name_short, eus_display_name, active_sw) = row[0]
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

