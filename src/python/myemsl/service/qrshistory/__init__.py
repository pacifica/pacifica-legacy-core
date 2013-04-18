#!/usr/bin/python

import sys
import urllib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def qrshistory(user, num, type, writer):
	writer.write("<?xml version=\"1.0\"?>\n")
	writer.write("<myemsl-qrshistory version=\"1.0\">\n")
	if not num:
		num = 10
	if not type:
		sql_type = ""
	else:
		sql_type = " and type = %(type)s"
	sql = """
	select type, id, time from myemsl.qrs_history where person_id = %(pid)s%(sql_type)s order by time desc limit %(num)s
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'pid':user, 'sql_type':sql_type, 'num':num})
	rows = cursor.fetchall()
	for row in rows:
		writer.write("  <entry><type>%s</type><itemid>%s</itemid><time>%s</time></entry>\n" %(row[0], row[1], row[2]))
	writer.write("</myemsl-qrshistory>\n")
	return 0

if __name__ == '__main__':
	sys.exit(qrscan(sys.argv[1], sys.argv[2], sys.argv[3], sys.stdout))

