#!/usr/bin/python

import sys
import urllib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def qrscan(user, type, id, writer):
	sql = """
	insert into myemsl.qrs_history(person_id, type, id) values(%(user)s, %(type)s, %(id)s)
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'user':user, 'type':type, 'id':id})
	cnx.commit()
	return 0

if __name__ == '__main__':
	sys.exit(qrscan(sys.argv[1], sys.argv[2], sys.argv[3], sys.stdout))

