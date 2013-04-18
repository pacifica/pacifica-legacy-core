#!/usr/bin/python

import sys
import base64
import random
from myemsl.dbconnect import myemsldb_connect

def session_add(user_id):
#FIXME rename myemsl.eus_auth
	pw = str(random.getrandbits(512))
	session_id = base64.b64encode(pw)
	sql = "insert into myemsl.eus_auth(user_name, session_id) values(%(uid)s, %(sid)s)"
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'uid':user_id, 'sid':session_id})
	cnx.commit()
	return session_id

def session_remove(user_id, session_id=None):
#FIXME rename myemsl.eus_auth
	where = "where user_name = %(uid)s"
	if session != None:
		where = where+" and session_id = %(sid)s"
	sql = "delete from myemsl.eus_auth %s" %(where)
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'uid':user_id, 'sid':session_id})
	cnx.commit()
	return

if __name__ == '__main__':
	print session_add(sys.argv[1])

