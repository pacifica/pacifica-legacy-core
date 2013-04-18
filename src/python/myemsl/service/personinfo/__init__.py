#!/usr/bin/python

import os
import sys
import errno
import urllib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

logger = getLogger(__name__)

def error(type, message, writer):
	if type:
		writer.write("<?xml version=\"1.0\"?><myemsl><error message=\"%s\"/></myemsl>\n" %(message))
	else:
		brand('header', writer)
		brand('middle', writer)
		writer.write("%s" %(message))
		brand('footer', writer)

def xstr(s):
	if s:
		return s
	return ''

def personinfo(user, person_id, dtype, writer):
	type = None
	person_id = int(person_id)
	sql = """
	select first_name, last_name, email_address, lower(network_id) from eus.users where person_id=%(person_id)s
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':person_id})
	rows = cursor.fetchall()
	for row in rows:
		if dtype:
			writer.write("<?xml version=\"1.0\"?>\n<myemsl>\n")
			writer.write("   <personid>%s</personid>\n" %(person_id))
			writer.write("   <firstname>%s</firstname>\n" %(xstr(row[0])))
			writer.write("   <lastname>%s</lastname>\n" %(xstr(row[1])))
			writer.write("   <emailaddress>%s</emailaddress>\n" %(row[2]))
			writer.write("   <networkid>%s</networkid>\n" %(xstr(row[3])))
			writer.write("</myemsl>\n")
		else:
       			brand('header', writer)
       			brand('middle', writer)
			writer.write("<table id=\"myemsl_personinfo_table\">\n")
			writer.write("<tr><td>Person ID</td><td>%s</dt></tr>\n" %(person_id))
			writer.write("<tr><td>First Name</td><td>%s</dt></tr>\n" %(xstr(row[0])))
			writer.write("<tr><td>Last Name</td><td>%s</dt></tr>\n" %(xstr(row[1])))
			writer.write("<tr><td>Email Address</td><td>%s</td></tr>\n" %(row[2]))
			writer.write("<tr><td>Network ID</td><td>%s</td></tr>\n" %(xstr(row[3])))
			writer.write("</table>\n")
       			brand('footer', writer)
	return 0

if __name__ == '__main__':
	sys.exit(personinfo(sys.argv[1], sys.argv[1], None, sys.stdout))

