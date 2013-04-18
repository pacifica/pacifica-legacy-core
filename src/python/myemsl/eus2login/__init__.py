#!/usr/bin/python

import base64
import myemsl.euslogin
import myemsl.getuserremote
import myemsl.eushandoff

def eus2login(user, password, session=True):
	res = {}
	login = myemsl.euslogin.eus_auth(base64.b64encode(user), password)
	if login:

		res['person_id'] = myemsl.getuserremote.get_user_remote(user)
#		myemsl.eushandoff.eus_user_remove(res['person_id'])
		if session:
			res['session_id'] = myemsl.eushandoff.eus_user_add(res['person_id'], res)
	return res

if __name__ == '__main__':
	import sys
	import getpass
	user = sys.argv[1]
	password = getpass.getpass()
	res = eus2login(user, password)
	print "User: %s\nPassword: %s\nURL: %s://%s%s" %(res['person_id'], res['session_id'], res['proto'], res['hostname'], res['path'])
