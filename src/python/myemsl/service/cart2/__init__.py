#!/usr/bin/python

import os
import sys
import errno
import urllib
import pycurl
import time
import servicepoke
import myemsl.cart
import myemsl.util
import myemsl.token
import myemsl.token.rfc3339enc as rfc3339enc
from StringIO import StringIO
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.getservices import getservices
services = getservices()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

import simplejson as json

logger = getLogger(__name__)

#FIXME pull this from somewhere else instead of hardcoded.
admin_users = [39822, 34002]

def cartresubmit(user, req, cart_id):
	user_id = int(user)
	if not user_id in admin_users:
		return 403
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	sql = """
	lock table myemsl.cart;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':user_id})
	sql = """
	update myemsl.cart set state='submitted', last_mtime = now() where cart_id = %(cart_id)i and state='admin_notified' returning cart_id;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'cart_id':int(cart_id)})
	rows = cursor.fetchall()
	for row in rows:
		cnx.commit()
#FIXME make configurable
		res = servicepoke.poke('/var/tmp/myemsl_cartd', 'cart_process2', 1)
		return 200
	return 404

def cartsget(user, req, cart_id=None, detail=False):
	user_id = int(user)
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	extra = ""
	if cart_id != None and cart_id != '':
		detail = True
		cart_id = int(cart_id)
		extra = ' and cart_id = %(cart_id)i'
	sql = "select cart_id, last_mtime, state from myemsl.cart where person_id = %(person_id)i" + extra + "order by submit_time;"
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':int(user), 'cart_id':cart_id})
	rows = cursor.fetchall()
	res = {'carts':[]}
	for row in rows:
		state = row[2]
		if state == 'admin_notified':
			state = 'admin'
		elif state == 'ingest':
			state = 'unsubmitted'
		elif state == 'amalgam' or state == 'downloading':
			state = 'building'
		elif state == 'email':
			state = 'available'
		elif state == 'download_expiring' or state == 'expiring' or state == 'expired':
			state = 'expired'
		elif state != 'submitted' and state != 'admin':
			state = 'unknown'
		cart_id = row[0]
		nrow = cart_id
		if detail == True:
			nrow = {'cart_id':cart_id, 'last_mtime':row[1], 'state':state}
			nrow['last_mtime'] = row[1]
			nrow['state'] = state
			if state == 'available':
				nrow['url'] = "%s%s/%s.amalgam/%s.tar" %(services['cart_download'], user, cart_id, cart_id)
		res['carts'].append(nrow)
	req.write(json.dumps(res))
	logger.debug("Carts get")
	return 200

def cartsadminget(user, req):
	user_id = int(user)
	if not user_id in admin_users:
		return 403
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	sql = """
	select cart_id, person_id, last_mtime, email_address, size, submit_time, items from myemsl.cart where state='admin_notified' order by submit_time;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	res = {'carts':[]}
	for row in rows:
		res['carts'].append({'cart_id':row[0], 'person_id':row[1], 'last_mtime':row[2], 'email_address':row[3], 'size':row[4], 'submit_time':row[5], 'items':row[6]})
	req.write(json.dumps(res))
	logger.debug("Cart admin get")
	return 200

def cartdel(user, req, cart_id):
	user_id = int(user)
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	sql = """
	select person_id, state from myemsl.cart where cart_id = %(cart_id)i;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':user_id, 'cart_id':int(cart_id)})
	rows = cursor.fetchall()
	common_allowed_states = ['email', 'downloading', 'download_expiring', 'expiring', 'ingest']
	common_allowed_states = dict([(i, 1) for i in common_allowed_states])
	state = 'expired'
	for row in rows:
		state = row[1]
		if not ((user_id in admin_users and (state == 'admin_notified' or state in common_allowed_states)) or (int(row[0]) == user_id and state in common_allowed_states)):
			return 403
	logger.debug("Cart delete %s" %(cart_id))
	if state != 'download_expiring' and state != 'expiring' or state != 'expired':
		new_state = 'expiring'
		if state == 'downloading':
			new_state = 'download_expiring'
		sql = "update myemsl.cart set state=%(new_state)s where cart_id = %(cart_id)s;"
		sys.stderr.write("SQL: %s\n" %(sql))
		cursor = cnx.cursor()
		cursor.execute(sql, {'cart_id':int(cart_id), 'new_state':new_state})
		cnx.commit()
#FIXME make configurable
		res = servicepoke.poke('/var/tmp/myemsl_cartd', 'cart_process2', 1)
	return 200

def cartsubmit(user, req, cart_id, email_addr):
	user_id = int(user)
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	sql = """
	select person_id, state = 'ingest' from myemsl.cart where person_id = %(person_id)i and cart_id = %(cart_id)i;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'person_id':user_id, 'cart_id':int(cart_id)})
	rows = cursor.fetchall()
	for row in rows:
		if int(row[0]) != user_id or row[1] != True:
			return 403
	logger.debug("Cart submit %s" %(cart_id))
	sql = """
	update myemsl.cart set last_mtime = now(), submit_time = now(), state='submitted', email_address=%(email_addr)s where cart_id = %(cart_id)s;
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cursor = cnx.cursor()
	cursor.execute(sql, {'cart_id':int(cart_id), 'email_addr':email_addr})
	cnx.commit()
#FIXME make configurable
	res = servicepoke.poke('/var/tmp/myemsl_cartd', 'cart_process2', 1)
	return 200

def cartadd(user, req, cart_id=None):
	req_data = req.read()
	request = json.loads(req_data)
	token = request['auth_token']
	user_id = int(user)
	pub = None
	try:
		pub, priv = myemsl.token.token_parse(token)
	except:
		pass
#FIXME Most of this code is common with the item server auth module. Generalize.
	if not pub:
		time.sleep(2)
		return 401
	logger.debug("Authorization: %s", pub)
	valid = myemsl.token.token_validate_time(pub)
	if not valid:
		return 401
	if not pub.has_key('i'):
		return 403
	try:
		auth_items = dict([(x, 1) for x in pub['i']])
		all_found = True
		for i in request['items']:
			if not auth_items.has_key(i):
				all_found = False
				break
		if all_found == False:
			return 403
	except:
		return 403
	cnx = myemsldb_connect(myemsl_schema_versions=['1.6'])
	if not cart_id:
		sql = """
		lock table myemsl.cart;
		"""
		sys.stderr.write("SQL: %s\n" %(sql))
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':user_id})
		sql = """
		insert into myemsl.cart(person_id) values(%(person_id)i) returning cart_id;
		"""
		sys.stderr.write("SQL: %s\n" %(sql))
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':user_id})
		rows = cursor.fetchall()
		for row in rows:
			cart_id = row[0];
		cnx.commit()
	else:
		sql = """
		select person_id, state = 'ingest' from myemsl.cart where person_id = %(person_id)i and cart_id = %(cart_id)i;
		"""
		sys.stderr.write("SQL: %s\n" %(sql))
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':user_id, 'cart_id':int(cart_id)})
		rows = cursor.fetchall()
		for row in rows:
			if int(row[0]) != user_id or row[1] != True:
				return 403
	last_mtime = None
	if not cart_id:
		return 500
	for i in request['items']:
		sql = """
		insert into myemsl.cart_items(cart_id, item_id) values(%(cart_id)i, %(item_id)i);
		update myemsl.cart set last_mtime = now() where cart_id = %(cart_id)i;
		select last_mtime from myemsl.cart where cart_id = %(cart_id)i;
		"""
		cursor = cnx.cursor()
		cursor.execute(sql, {'person_id':user_id, 'cart_id':int(cart_id), 'item_id':int(i)})
		rows = cursor.fetchall()
		for row in rows:
			last_mtime = row[0]
	cnx.commit()
	req.write(json.dumps({'cart_id':cart_id, 'last_mtime':last_mtime}))
	return 200

if __name__ == '__main__':
	sys.exit(cartadd(sys.argv[1], sys.stdout))

