#!/usr/bin/python

import subprocess
import sys
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def get_user(type, username, writer):
	person_id = -1
	eussync_tried = False
	writer.write("<?xml version=\"1.0\"?>\n")
	writer.write("<myemsl-getuser version=\"1.0\">\n")
	if type == 'network_id':
		username = username.split('@', 1)[0]
#FIXME lower
		sql = "select person_id from eus.users where upper(network_id) = upper(%(username)s)"
	elif type == 'email_address':
		sql = "select person_id from eus.users where email_address = %(username)s"
	else:
		writer.write("  <error message=\"unknown network type: %s\"/>\n" %(type))
		writer.write("</myemsl-getuser>")
		return
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	while True:
		cursor = cnx.cursor()
		cursor.execute(sql, {'username':username})
		rows = cursor.fetchall()
		if len(rows) < 1:
			if not eussync_tried:
				#FIXME create new personid.
				#call eus sync
				out = open('/dev/null', 'w')
				res = subprocess.call(['/usr/sbin/eus_table_sync.php'], stdout=out, stderr=out)
				eussync_tried = True
				if res == 0:
					continue
				else:
					writer.write("  <error message=\"Failed to eus table sync\"/>\n")
					writer.write("</myemsl-getuser>\n")
					return
					print 'failure'
		else:
			for row in rows:
				person_id = row[0]
				break
		break
	if person_id != -1:
		writer.write("  <user id=\"%s\"/>\n" %(person_id))
	else:
		writer.write("  <error message=\"unknown user\"/>\n")
	writer.write("</myemsl-getuser>\n")
	return

def get_user_base(url, writer):
	s = url.split('/', 2)
	if not s or len(s) != 2:
		writer.write("<?xml version=\"1.0\"?>\n")
		writer.write("<myemsl-getuser version=\"1.0\">\n")
		writer.write("  <error message=\"invalid arugments\"/>\n")
		writer.write("</myemsl-getuser>\n")
	else:
		get_user(s[0], s[1], writer)

if __name__ == '__main__':
	get_user(sys.argv[1], sys.argv[2], sys.stdout)

