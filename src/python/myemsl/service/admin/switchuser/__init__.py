#!/usr/bin/python

import subprocess
import sys
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def switch_user(session_id, new_user, writer):
	current_user = ''
	sql = "select user_name from myemsl.eus_auth where session_id = %(session_id)s;"
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'session_id':str(session_id)})
	rows = cursor.fetchall()
	if len(rows) < 1:
		return 400
	for row in rows:
		current_user = int(row[0])
#FIXME Unhardcode this.
	if not current_user in [39822, 22583, 34002]:
		return 403
	sql = "update myemsl.eus_auth set user_name = %(new_user)s where user_name = %(current_user)s and session_id = %(session_id)s;"
	cursor = cnx.cursor()
	cursor.execute(sql, {'current_user':str(current_user), 'new_user':str(new_user), 'session_id':str(session_id)})
	cnx.commit()
	writer.write('{"ok":true}\n')
	return 200

if __name__ == '__main__':
	print switch_user(sys.argv[1], sys.argv[2], sys.stdout)

