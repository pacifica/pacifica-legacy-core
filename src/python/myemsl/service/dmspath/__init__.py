#!/usr/bin/python 

import sys

import simplejson as json

from myemsl.dbconnect import myemsldb_connect

from myemsl.logging import getLogger

import time
import myemsl.token
import myemsl.token.rfc3339enc as rfc3339enc

logger = getLogger(__name__)

#FIXME make this configurable
items_per_auth_token = 100

def auth_sign(items):
#FIXME read in from config.
	uuid = 'huYNwptYEeGzDAAmucepzw';
#FIXME read in from config.
	duration = 60 * 60
	js = {'s':rfc3339enc.rfc3339(time.time()), 'd':duration, 'u':uuid, 'i':items, 'o':0}
	stok = myemsl.token.token_gen(js, '')
	return stok

def base_query(user, path, auth_add, writer, config=None, indent=None):
	path = path.strip('/')
	logger.info("path %s", path)
	sql = """
SELECT
	f.name,
	f.item_id
FROM
	(
	SELECT
		f.subdir,
		f.name,
		max(f.transaction) as transaction
	FROM
		myemsl.files AS f,
		myemsl.transactions as t
	WHERE
		f.subdir = %(subdir)s AND
		t.submitter = %(person_id)i AND
		t.transaction = f.transaction
	GROUP BY
		f.subdir,
		f.name
	) as fs,
	myemsl.files as f
WHERE
	fs.transaction = f.transaction AND
	fs.name = f.name AND
	fs.subdir = fs.subdir
"""
	logger.info("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'], dbconf=config)
	cursor = cnx.cursor()
	cursor.execute(sql, params={'subdir':path, 'person_id':int(user)})
	rows = cursor.fetchall()
	dirs = []
	files = []
	auth_items = []
	auth_tokens = []
	token_offset = 0
	document = {'files':files, 'dirs':dirs}
	for (name, item_id) in rows:
		file = {'name': name, 'item_id': item_id}
		if auth_add:
			file['token'] = token_offset
			auth_items.append(item_id)
			if len(auth_items) >= items_per_auth_token:
				auth_tokens.append(auth_sign(auth_items))
				auth_items = []
				token_offset += 1
		files.append(file)
	if auth_add:
		if len(files) > 0 and len(auth_items) > 0:
			auth_tokens.append(auth_sign(auth_items))
		document['myemsl_auth'] = auth_tokens
	sql = """
SELECT DISTINCT
	split_part(f.subdir, '/', %(part)i)
FROM
	myemsl.files as f,
	myemsl.transactions as t
WHERE
	t.submitter = %(person_id)i AND
	t.transaction = f.transaction AND
	f.subdir LIKE %(pattern)s ESCAPE '^'
"""
	pattern = path.replace('^', '^^').replace('%', '^%').replace('_', '^_')
	part = path.count('/') + 1
	if pattern != '':
		part += 1
		pattern += '/'
	pattern += '%'
	cursor.execute(sql, params={'pattern':pattern, 'person_id':int(user), 'part':part})
	rows = cursor.fetchall()
	for (dir,) in rows:
		dirs.append({'name':dir})
	json.dump(document, writer, indent=indent)

if __name__ == '__main__':
	sys.exit(base_query(sys.argv[1], sys.argv[2], True, sys.stdout, indent=4))

