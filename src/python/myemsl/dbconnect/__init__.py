#!/bin/env python

import pg
import re
import pgdb

from myemsl.getconfig import getconfig_secret

from myemsl.logging import getLogger

logger = getLogger(__name__)

def myemsldb_connect(dbconf = None, myemsl_schema_versions=None):
	if dbconf == None:
		dbconf = getconfig_secret()
	if myemsl_schema_versions == None:
		raise Exception("You did not specify any supported versions")
	versions = {}
	for x in myemsl_schema_versions:
		(major, minor) = x.split('.')
		versions[major] = minor
	cnx = pgdb.connect(database=dbconf.get('metadata', 'database'), user=dbconf.get('metadata', 'user'), host=dbconf.get('metadata', 'host'), password=dbconf.get('metadata', 'password'))
	sql = """
	select value from myemsl.system where key='schema_version'
	"""
	cursor = cnx.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	schema_version = None
	for row in rows:
		schema_version = row[0]
	(major, minor) = schema_version.split('.')
	if major in versions:
		if minor < versions[major]:
			err = "Schema version too old. Got %s.%s, support %s" %(major, minor, str(versions))
			logger.error(err)
			raise Exception(err)

	else:
		err = "Schema version mismatch. Got %s.%s, support %s" %(major, minor, str(versions))
		logger.error(err)
		raise Exception(err)
	return cnx

def do_sql_select(sql, fail_ok=0, myemsl_schema_versions=None, params=None):
	cnx = myemsldb_connect(myemsl_schema_versions=myemsl_schema_versions)
	try:
		cursor = cnx.cursor()
		cursor.execute(sql, params)
		rows = cursor.fetchall()
		cnx.commit()
	except pg.DatabaseError, e:
		if not fail_ok:
			raise
	cnx.close()
	return rows

def do_sql_insert(sql, fail_ok=0, myemsl_schema_versions=None, params=None):
	cnx = myemsldb_connect(myemsl_schema_versions=myemsl_schema_versions)
	already_exists_match = re.compile("error \'ERROR:  duplicate key value violates unique constraint.*")
	try:
		cursor = cnx.cursor()
		cursor.execute(sql, params)
		cnx.commit()
	except pg.DatabaseError, e:
		if not fail_ok or not already_exists_match.match(str(e)):
			raise
	cnx.close()


