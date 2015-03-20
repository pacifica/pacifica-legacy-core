#!/usr/bin/env python

import sys

from myemsl.dbconnect import myemsldb_connect
from myemsl.getconfig import getconfig_secret
config = getconfig_secret()

from myemsl.logging import getLogger
from myemsl.metadata import get_proposals_from_user, get_custodian_instruments, get_proposals_from_instrument

logger = getLogger(__name__)

def get_network_id_to_person_id_hash():
	user_hash = {}
	try:
		sql = "select person_id, network_id from eus.users where network_id is not null"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		for row in rows:
			if row[1] != None and row[1] != '':
				user_hash[row[1].upper()] = row[0]
	except Exception, e:
		logger.error("%s", e)
		raise
	return user_hash

def get_permission_group_members(type, name):
	group_members = []
	try:
		sql = "select person_id from myemsl.permission_group as pg, myemsl.permission_group_members as pgm where pg.type = %(type)s and pg.name = %(name)s and pg.permission_group_id = pgm.permission_group_id"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"type":type, "name":name})
		rows = cursor.fetchall()
		for row in rows:
			group_members.append(row[0])
	except Exception, e:
		logger.error("%s", e)
		raise
	return group_members

def get_permission_group_id(type, name):
	id = None
	try:
		sql = "select permission_group_id from myemsl.permission_group as pg where pg.type = %(type)s and pg.name = %(name)s"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"type":type, "name":name})
		rows = cursor.fetchall()
		for row in rows:
			id = row[0]
	except Exception, e:
		logger.error("%s", e)
		raise
	return id

def get_permission_set_id(perms):
	l = len(perms)
	if l <= 0:
		raise Exception("Not enough perms")
	id = None
	try:
		perms_hash = {}
		where = ''
		count = 1
		for perm in perms:
			if count != 1:
				where += 'or '
			where += "permission=%%(%s)s" %(str(count));
			perms_hash[str(count)] = str(perm)
			count += 1
		logger.debug("where %s", where)
		sql = "select permission_set_id from (select permission_set_id, count(*) as count from myemsl.permission_set_perms as psp where %s group by permission_set_id) as s where s.count = %i" %(where, l)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, perms_hash)
		rows = cursor.fetchall()
		for row in rows:
			id = row[0]
			break
	except Exception, e:
		logger.error("%s", e)
		raise
	return id

def get_or_create_permission_set_id(perms):
	id = get_permission_set_id(perms)
	if id == None:
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		sql = "insert into myemsl.permission_set(permission_set_id) values(DEFAULT);"
		cursor.execute(sql)
		cursor.executemany("insert into myemsl.permission_set_perms(permission_set_id, permission) values(currval(pg_get_serial_sequence('myemsl.permission_set', 'permission_set_id')), %(perm)s)", [{'perm':str(i)} for i in perms])
		cnx.commit()
		id = get_permission_set_id(perms)
	return id

def create_permission_group(type, name):
	id = None
	try:
		sql = "insert into myemsl.permission_group(type, name) values(%(type)s, %(name)s)"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"type":type, "name":name})
		cnx.commit()
		id = get_permission_group_id(type, name)
	except Exception, e:
		logger.error("%s", e)
		raise
	return id

def add_permission_group_member(pgid, person_id):
	try:
		sql = "insert into myemsl.permission_group_members(permission_group_id, person_id) values(%(pgid)s, %(person_id)s)"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"pgid":pgid, "person_id":person_id})
		cnx.commit()
	except Exception, e:
		logger.error("%s", e)
		raise
	return id

def remove_permission_group_member(pgid, person_id):
	try:
		sql = "delete from myemsl.permission_group_members where permission_group_id = %(pgid)s and person_id = %(person_id)s"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"pgid":pgid, "person_id":person_id})
		cnx.commit()
	except Exception, e:
		logger.error("%s", e)
		raise
	return

def network_id_to_person_id(user_hash, users):
	new_users = []
	for user in users:
		person_id = user_hash.get(user)
		if person_id != None:
			new_users.append({'person_id':person_id, 'network_id':user})
		else:
			logger.warning("Unknown user %s", user)
	return new_users

def create_permission(gid, cls, psid):
	try:
		sql = "insert into myemsl.permissions(permission_group_id, permission_set_id, permission_class) values(%(gid)i, %(psid)i, %(cls)s)"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql, {"gid":gid, "psid":psid, "cls":cls})
		cnx.commit()
	except Exception, e:
		logger.error("%s", e)
		raise
	return

def get_permission_ingest(metadata, userid):
	"""
	pseudo code to manage ingest permissions

	if user is memeber of proposal
	  return True
	elif user is custodian of the instrument and the proposal has instrument 
	  return True
	fi
	return False

	This has to be made generic for multiple formats of metadata.
	So to be more specific...

	get list of proposals user is a member of
	get list of proposals in the metadata
	for all proposals in metadata
	  if proposal is not in proposals for user
	    questionable_proposals += proposal
	
	if questionable_proposals is empty
	  return True

	get list of instruments user is custodian on
	if custodian instrument list is empty and questionable_proposals is not empty
	  return False
	else
	  get list of proposals from custodian instrument list
	  for all proposals in questionable_proposals
	    if proposal in questionable_proposals
	      remove proposal from questionable_proposals
	if questionable_proposals is empty
	  return True
	return False
	"""
	my_proposals = get_proposals_from_user(userid)
	requested_proposals = {}
	if 'eusInfo' in metadata:
		if 'proposalID' in metadata['eusInfo']:
			requested_proposals[metadata['eusInfo']['proposalID']] = 1
	if 'file' in metadata:
		for file in metadata['file']:
			if 'groups' in file and file['groups']:
				for group in file['groups']:
					if group['type'] == 'proposal':
						requested_proposals[group['name']] = 1
	questionable_proposals = []
	for prop in requested_proposals.keys():
		if not prop in my_proposals:
			questionable_proposals.append(prop)

	if len(questionable_proposals) == 0:
		return True

	instrument_proposals = {}
	for instrument in get_custodian_instruments(userid):
		for prop in get_proposals_from_instrument(instrument):
			instrument_proposals[prop] = 1

	for prop in instrument_proposals.keys():
		if prop in questionable_proposals:
			questionable_proposals.remove(prop)

	if len(questionable_proposals) == 0:
		return True
	return False
