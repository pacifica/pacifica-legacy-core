#!/usr/bin/env python

import sys

from myemsl.dbconnect import myemsldb_connect
from myemsl.getconfig import getconfig_secret
config = getconfig_secret()

from myemsl.logging import getLogger

logger = getLogger(__name__)

def get_permission_bool(person_id, permission_class, permission, config=None):
	retval = False
	try:
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		user_hash = {}
		cursor = cnx.cursor()
		cursor.execute("""
SELECT
  count(*)
FROM
  myemsl.permission_set_perms as psp,
  myemsl.permissions as p,
  myemsl.permission_group_members as pgm,
  myemsl.permission_group as pg
WHERE
  pg.permission_group_id = pgm.permission_group_id and
  p.permission_group_id = pg.permission_group_id and
  p.permission_set_id = psp.permission_set_id and
  psp.permission = %(permission)s and
  p.permission_class = %(class)s and
  person_id = %(person_id)i;
""", {'permission':permission, 'class':permission_class, 'person_id':person_id})
		rows = cursor.fetchall()
		for row in rows:
			if row[0] > 0:
				retval = True
	except Exception, e:
		logger.error("%s", e)
		raise
	return retval

def get_permission_upload(person_id, proposal_id, config):
	retval = False
	try:
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'], dbconf=config)
		cursor = cnx.cursor()
		sql = """
SELECT
  True 
FROM
  eus.proposal_members
WHERE
  proposal_id = %(proposal)s and
  person_id = %(person_id)i;
"""
		cursor.execute(sql, {'proposal':str(proposal_id), 'person_id':int(person_id)})
		rows = cursor.fetchall()
                for row in rows:
                        if row[0]:
                                retval = True;
	except Exception, e:
		logger.error("%s", e)
		raise
	return retval


if __name__ == '__main__':
	print get_permission_bool(int(sys.argv[1]), sys.argv[2], sys.argv[3])
