#!/usr/bin/python

# Author: Brock Erwin
# Description: Get/Set notification preferences per proposal

import os
import sys
import errno
import urllib
import simplejson
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

logger = getLogger(__name__)

def getnotifications(person_id, writer):
	type = None
	logger.debug( str(person_id) )
	_person_id = int(person_id)
	sql = """
	(
	 	select notification.proposal_id, true, title
				from
			myemsl.notification join eus.proposals
				on
			notification.proposal_id = proposals.proposal_id
	) union all (
		
		select proposals.proposal_id, false, title
				from
			proposal_members join proposals
				on
			proposal_members.proposal_id = proposals.proposal_id
				where
			person_id = %(person_id)s
				and
			proposals.proposal_id not in
					(select proposal_id from myemsl.notification where person_id = %(person_id)s  )
	)
		order by proposal_id;
	"""
	sql = """
		select
			case when myemsl.notification.person_id is null
					then
				true
					else
				false
			end, q1.proposal_id, title
					from
				(
				 	select
						proposals.proposal_id, proposal_members.person_id, title
							from
						eus.proposal_members join eus.proposals on proposal_members.proposal_id = proposals.proposal_id
							where
						person_id = %(person_id)s
				) as q1
					left join
				myemsl.notification
					on
				q1.proposal_id = myemsl.notification.proposal_id
					and
				q1.person_id = myemsl.notification.person_id
					order by
				proposal_id;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':_person_id})
	rows = cursor.fetchall()
	writer.write(simplejson.dumps(rows, sort_keys=True, indent=4))

# For a given person and a dictionary proposal IDs, for each proposal id in the list
# turn on notifications for that proposal.  Any other proposals will NOT be notified
# to the user

def setnotifications(person_id, proposals):
	_person_id = int(person_id)
	logger.debug(str(proposals))
	positiveNotifications = [] # Contains proposals to be notified on
	negativeNotifications = [] # Contains proposals to be notified on

	sql = """
	select proposal_id from eus.proposal_members where person_id = %(person_id)s;
	"""
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':_person_id})
	rows = cursor.fetchall()
	user_proposals = []
	for row in rows:
		user_proposals.append(row[0])

	# Separate each proposal into two lists:
	#  First list: proposals to be notified on
	#  Second list: proposals not to be notified on
	for item in proposals:
		#logger.debug(' stuff %s : %s ' % (item, proposals[item]))
		parts = item.split('-')
		# Validate input, prevent SQL injection attack
		# TODO: Return or raise some helpful error message
		if len(parts) != 2 or parts[0] != 'proposal' or parts[1].find('\'') != -1 or len(proposals[item]) != 1:
			return
		if parts[1] not in user_proposals:
			logger.debug('person_id: %d does not have access to proposal %s!' % (_person_id, parts[1]))
			return
		if proposals[item][0].upper() == 'TRUE':
			positiveNotifications.append(parts[1])
		elif proposals[item][0].upper() == 'FALSE':
			negativeNotifications.append(parts[1])
		else:
			return
	if len(positiveNotifications) > 0:
		sql = """
		delete from myemsl.notification
			where
				person_id = %(person_id)s and (
		"""
		justEnteredLoop = True	
		for id in positiveNotifications:
			if not justEnteredLoop:
				sql += " or "
			justEnteredLoop = False
			sql += " proposal_id = '%s' " % id
		sql += ' ) '
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':_person_id})
		cnx.commit()

	if len(negativeNotifications) > 0:
		sql = """
		insert into myemsl.notification values
		"""
		justEnteredLoop = True
		for id in negativeNotifications:
			if not justEnteredLoop:
				sql += ", "
			justEnteredLoop = False
			sql += "	(%d, '%s')" % (_person_id, id)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':_person_id})
		cnx.commit()

		
	logger.debug(str(positiveNotifications))
#notification.setpositivenotifications(req.user, positiveNotifications)
