#!/usr/bin/python

#FIXME This is a start of an implementation for this. It is close to, but non-functional at the moment.

import authz_token

def allow_access(environ, host):
	var_lookup = environ['mod_ssl.var_lookup'] 
	file = open('/tmp/foodump.txt', 'w')
	file.write("%s %s" %(environ, dir(var_lookup)))
	file.close()
	return True #host in ['localhost']

def groups_for_user(environ, user):
    file = open('/tmp/foodump.txt', 'w')
    file.write("%s %s" %(environ, user))
    if user == 'spy':
        return ['secret-agents']
    return ['']

def check_password(environ, user, password):
#FIXME
	items = password.split(' ', 1)
	if len(items) < 2:
		return False
	if items[0].strip() != 'Bearer':
		return False
	password = password.split(' ', 1)[1].strip()
	pub, priv = authz_token.token_parse(password)
	valid = authz_token.token_validate_time(pub)
	return valid
