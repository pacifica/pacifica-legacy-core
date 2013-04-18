#!/usr/bin/python

import sys
import urllib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def transaction(submitter, writer):
	sql = """
	insert into myemsl.transactions(submitter) values(%(submitter)s);
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.1'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'submitter':submitter})
	sql = """
	select currval(pg_get_serial_sequence('myemsl.transactions', 'transaction'));
	"""
	cursor.execute(sql)
	rows = cursor.fetchall()
	transaction = None
	for row in rows:
		transaction = row[0]
	if transaction == None:
		raise Exception()
	cnx.commit()
	writer.write('<?xml version="1.0"?>\n')
	writer.write('<myemsl>\n')
	writer.write('  <transaction id="%s" />\n' %(transaction))
	writer.write('</myemsl>\n')
	return 0

if __name__ == '__main__':
	sys.exit(transaction(sys.argv[1], sys.stdout))

