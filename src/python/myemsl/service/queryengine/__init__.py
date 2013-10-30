#!/usr/bin/python 

#SQL injection notes:
#Do not call do:
# foo = ".... %s" %(pg_escape_string(stuff_from_user))
# foo = .... + foo %(some_stuff)
# Also under this form of sql injection protection never use the params argument of execute(many)

"""
this script is meant to be called with a path parameter.

#QUERY url looks like:
#/user/cat/arg/arg/cat/cat/arg/.../data/t1/t2/realdata/realdata/...

>>> import sys, StringIO

>>> def q(query):
...  base_query(query, sys.stdout)

Create a dummy database connection for testing.
>>> class D:
... 	class C:
... 		def __init__(self, *x, **y): pass
...			def execute(self, *x, **y): return (x, y)
... 		def fetchall(self, *x, **y): return [(x, y)]*6
...
... 	def __init__(self, *x, **y): pass
...		def cursor(self): return self.C()
>>> myemsldb_connect = D

>>> q("/")
<?xml version="1.0"?>
<myemsl-readdir version="1.0.0">
  <error message="You must specify a user"/>
</myemsl-readdir>

>>> q("/shor461")
<?xml version="1.0"?>
<myemsl-readdir version="1.0.0">
  <dir name="raw" type="0"/>
  <dir name="transaction" type="0"/>
  <dir name="group" type="0"/>
  <dir name="item" type="0"/>
  <dir name="submit_time" type="0"/>
  <dir name="submitter" type="0"/>
  <dir name="directly_derived_from_item" type="0"/>
  <dir name="proposal" type="0"/>
  <dir name="data" type="4"/>
  <dir name="group_name" type="0"/>
</myemsl-readdir>

>>> q("/shor461/data")

>>> q("/shor461/x")
<?xml version="1.0"?>
<myemsl-readdir version="1.0.0">
  <error message="Unknown function x"/>
</myemsl-readdir>

>>> q("/shor461/submitter")
"""
import sys

from xml.sax import saxutils

from myemsl.dbconnect import myemsldb_connect

from myemsl.logging import getLogger

import time
import myemsl.token
import myemsl.token.rfc3339enc as rfc3339enc

try:
	from pg import escape_string as pg_escape_string
except:
	import pgdb
	def pg_escape_string(string):
		return pgdb._quote(str(string))[1:-1]

logger = getLogger(__name__)

#QUERY url looks like:
#/user/cat/arg/arg/cat/cat/arg/.../data/t1/t2/realdata/realdata/...

DOCUMENT_FILTERS, DOCUMENT_FILTER_ARGS, DOCUMENT_REGULAR, DOCUMENT_ERROR, DOCUMENT_DATA = (0, 1, 2, 3, 4)

def return_document(directories, files, error, type, after_data, op, auth_add, user, writer):
	writer.write("<?xml version=\"1.0\"?>\n")
	tag = "unknown"
	if op == "readdir" or op == "stat":
		tag = op
	else:
		error = "Unknown op type."
	writer.write("<myemsl-%s version=\"1.0.0\">\n" %(tag))
	if error:
		writer.write("  <error message=\"%s\"/>\n" %(saxutils.escape(error)))
	else:
#FIXME only put this in if not already later
#This is not right. Data seen and later != 0?
		if not after_data and type == DOCUMENT_FILTER_ARGS:
			writer.write("  <dir name=\"-later-\" type=\"%s\"/>\n" %(DOCUMENT_FILTER_ARGS))
		if directories:
			for d in directories:
				tmptype = type
				if d["name"] == 'data' and type == DOCUMENT_FILTERS:
					tmptype = DOCUMENT_DATA
				name = ""
				if op != "stat":
					name = " name=\"%s\"" %(saxutils.escape(str(d["name"])))
				writer.write("  <dir%s type=\"%s\"/>\n" %(name, tmptype))
		if files:
#FIXME make this configurable.
			items_per_auth_token = 100
			token_offset = 0
			auth_tokens = []
			auth_items = []
			for f in files:
				auth_str = ""
				if auth_add:
					auth_str = " authidx=\"%s\"" %(token_offset)
				name = ""
				if op != "stat":
					name = " name=\"%s\"" %(saxutils.escape(str(f["name"])))
#FIXME remove location once item server is fully in place.
				writer.write("  <file%s location=\"%s\" itemid=\"%s\" size=\"%s\"%s/>\n" %(name, saxutils.escape(str(f["location"])), f["itemid"], f["size"], auth_str))
				if auth_add:
					auth_items.append(f["itemid"])
					if len(auth_items) >= items_per_auth_token:
						auth_tokens.append(myemsl.token.simple_items_token_gen(auth_items, person_id=user_id))
						auth_items = []
						token_offset += 1
			if auth_add:
				if files and len(auth_items) > 0:
					auth_tokens.append(auth_sign(auth_items))
				writer.write("  <auth>\n")
				for t in auth_tokens:
					writer.write("    <token>%s</token>\n" %(t))
				writer.write("  </auth>\n")
	writer.write("</myemsl-%s>\n" %(tag))

def base_query(QUERY, op, auth_add, writer, config=None):
	query = QUERY.split('/')
	logger.info("%s", QUERY)

	later = []
	query[:] = [i for i in query if i != '']
	if len(query) < 1:
		return_document(None, None, "You must specify a user", DOCUMENT_ERROR, False, op, False, None, writer)
		return -1
	user = query.pop(0)
	for (id, value) in enumerate(query):
		if value == '-later-':
			later.append(id)
			query[id] = '-any-'
	return raw_query(query, later, int(user), False, op, auth_add, writer, config=config)

base_sql = """
SELECT 'f' as type, name, subdir, transaction, item_id, aged FROM myemsl.files
"""
#base_sql = """
#SELECT 'd' as type, inode, parent_inode, name, regexp_replace(fullpath_name, '^/myemsl/[^/]*/bundle/[0-9]*(.*)/[^/]+$', '\\\\1', '') as subdir, regexp_replace(fullpath_name, '^/myemsl/[^/]*/bundle/([0-9]+).*', '\\\\1', '') as bundle, regexp_replace(fullpath_name, '^/myemsl/([^/]*)/bundle/.*$', '\\\\1', '') as submitter, 0 as item_id FROM dirs where fullpath_name ~ '^/myemsl/[^/]*/bundle/[0-9]*'
#union
#SELECT 'f' as type, inode, parent_inode, name, regexp_replace(fullpath_name, '^/myemsl/[^/]*/bundle/[0-9]*(.*)/[^/]+$', '\\\\1', '') as subdir, regexp_replace(fullpath_name, '^/myemsl/[^/]*/bundle/([0-9]+).*', '\\\\1', '') as bundle, regexp_replace(fullpath_name, '^/myemsl/([^/]*)/bundle/.*$', '\\\\1', '') as submitter, item_id FROM files where fullpath_name ~ '^/myemsl/[^/]*/bundle/[0-9]*'
#"""
def raw_query(query, later, user, after_data, op, auth_add, writer, config=None):
	sql = base_sql
	id = 0
	#print query
	while id < len(query):
		if not funcs.has_key(query[id]):
			return_document(None, None, "Unknown function %s" %(query[id]), DOCUMENT_ERROR, False, op, False, user, writer)
			return -1
		result = funcs[query[id]](query, sql, id + 1, later, user, after_data, op, auth_add, writer, config=config)
		if result["done"]:
			return 0
		sql = result["sql"]
		id = id + result["consumed"] + 1
	#if here, didn't end.
#FIXME is DOCUMENT_FILTERS correct?
	if op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
		return {"done":True}
	return_document([{"name":i} for i in funcs.iterkeys()], None, None, DOCUMENT_FILTERS, after_data, op, False, user, writer)
	return 0

#FIXME split if blocks into functions
def data_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
#FIXME validate math
	if len(later) > 0:
		#This branch handles filling in all the -later-'s with the user specified var and restarting the query so that the filters get their arguments.
		if len(query) - arg_offset >= len(later):
			shorten_by = len(later)
			first_part = query[:(arg_offset)]
			second_part = query[(arg_offset + shorten_by):]
			new_query = first_part + second_part
			#print later, first_part, second_part, len(query), len(later), arg_offset, (arg_offset - shorten_by)
			for (i, qid) in enumerate(later):
				new_query[qid] = query[arg_offset + i]
			raw_query(new_query, [], user, True, op, auth_add, writer, config=config)
			return {"done":True}
		#This branch handles the case that there are not enough arguments to handle all of the -later-'s so it truncates the query down to the missing -later-
		else:
			num = len(query) - arg_offset
			new_query = query[:(arg_offset - 2)]
			for (i, qid) in enumerate(later):
				logger.info('i qid %s, %s', i, qid)
				if len(query) > arg_offset + i:
					new_query[qid] = query[arg_offset + i]
				else:
					new_query = new_query[:qid]
			logger.info("Running raw query %s", new_query)
			raw_query(new_query, [], user, True, op, auth_add, writer, config=config)
			return {"done":True}
	return select_and_return(sql, query[arg_offset:], user, op, auth_add, writer, config=config)

#Takes rough query built up by filters and applies
# * Permissions
# * Directory building
# * Uniqueness

def select_and_return(sql, left, user, op, auth_add, writer, config=None):
	#sql = "select type, inode, parent_inode, name, subdir, bundle, submitter from (%s) as foo where subdir = ''" %(sql)
	if left == None or len(left) == 0:
		subdir = ""
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_DATA, True, op, auth_add, user, writer)
			return {"done":True}
	else:
		tmpleft = left
		if op == "stat":
			tmpleft = left[0:-1]
		subdir = "%s" %('/'.join([str(i) for i in tmpleft]))
#	sql = "select name, max(bundle) as bundle from (%s) as foo where subdir = '%s' group by name" %(sql, subdir)
#	sql = "select type, inode, parent_inode, foo.name, subdir, foo.bundle, submitter from (%s) as foo, (%s) as basefiles where basefiles.bundle = foo.bundle and basefiles.name = foo.name and subdir = '%s'" %(sql, base_sql, subdir)
	#Authz stuff
#FIXME order?
	file_proposal_member = """
foo.item_id in (with recursive t(group_id) as (
select eus.proposals.group_id from eus.proposal_members, eus.proposals, myemsl.groups where eus.proposal_members.person_id = %s and eus.proposals.proposal_id = eus.proposal_members.proposal_id and eus.proposals.group_id = groups.group_id
union
select myemsl.subgroups.child_id as group_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id
) select item_id from t, myemsl.group_items where myemsl.group_items.group_id = t.group_id)
	""" %(int(user))
	new_sql = """
	select type, name, subdir, foo.transaction, submitter, item_id from (%s) as foo, myemsl.transactions where (submitter = %s or foo.aged = TRUE or %s) and foo.transaction = myemsl.transactions.transaction order by transaction desc
	""" %(sql, int(user), file_proposal_member)
	sql = new_sql
	#Dirs stuff
	if subdir == '':
		subdirstuff = "subdir like '%%'"
		start = 1
	else:
		like_escape = pg_escape_string(subdir).replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
		subdirstuff = "subdir like '%s/%%'" %(like_escape)
		start = len(subdir) + 2
	new_sql = """
	select case when subdir = '%s' then 'f' else 'd' end as type, case when subdir = '%s' then name else split_part(substr(subdir, '%s'), '/', 1) end as name, subdir, transaction, submitter, item_id from (%s) as foo where (subdir = '%s' or %s)
	""" %(pg_escape_string(subdir), pg_escape_string(subdir), pg_escape_string(start), sql, pg_escape_string(subdir), subdirstuff)
	sql = new_sql
	if op == "stat":
		name = left[-1:][0]
		new_sql = """
		select type, name, transaction from (%s) as foo where name = '%s'
		""" %(sql, name)
		sql = new_sql
	#Remove duplicates
	new_sql = """
	select type, name, max(transaction) as transaction from (%s) as foo group by name, type
	""" %(sql)
	sql = new_sql
#FIXME remove subdir
	#Add submitter back
	new_sql = """
	select type, name, foo.transaction as transaction, submitter from (%s) as foo left outer join myemsl.transactions on (foo.transaction = myemsl.transactions.transaction)
	""" %(sql)
	sql = new_sql
	new_sql = """
	select type, foo.name, '%s' as subdir, foo.transaction, submitter, item_id, size from (%s) as foo left outer join myemsl.files on (foo.transaction = myemsl.files.transaction and foo.name = myemsl.files.name and myemsl.files.subdir = '%s')
	""" %(pg_escape_string(subdir), sql, pg_escape_string(subdir))
	sql = new_sql
	logger.info("%s", sql)
	#Dirs stuff
#	new_sql = "SELECT 'd' as type, name, subdir, 0 as transaction, -1 as submitter, 0 as item_id FROM myemsl.dirs where subdir = '%s' union %s" %(subdir, sql)
#	sql = new_sql
	sys.stderr.write("SQL: %s, Left: %s\n" %(sql, left))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'], dbconf=config)
	cursor = cnx.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	dirs = []
	files = []
	if op == "stat":
		dirfound = False
		for row in rows:
			if(row[0] == 'd'):
				dirfound = True
			else:
				files.append({"name":"stat", "location":"%s/bundle/%s/%s/%s" %(row[4], row[3], row[2], row[1]), "itemid":row[5], "size":row[6]})
		if dirfound:
			dirs.append({"name":"stat"})
			files = []
	else:
		for row in rows:
			if(row[0] == 'd'):
				dirs.append({"name":row[1]})
			else:
				files.append({"name":row[1], "location":"%s/bundle/%s/%s/%s" %(row[4], row[3], row[2], row[1]), "itemid":row[5], "size":row[6]})
	if len(dirs) == 0:
		dirs = None
	if len(files) == 0:
		files = None
#FIXME is DOCUMENT_REGULAR correct?
	return_document(dirs, files, None, DOCUMENT_REGULAR, True, op, auth_add, user, writer)
	return {"done":True}

def submitter_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select submitter from (%s) as foo, myemsl.transactions where foo.transaction = myemsl.transactions.transaction group by myemsl.transactions.submitter" %(sql)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		qry_string = ", myemsl.transactions where submitter='%s' and myemsl.transactions.transaction = bar.transaction" %(pg_escape_string(query[arg_offset]))
	return {"done":False, "consumed":1, "sql":"select type, name, subdir, bar.transaction, item_id, aged from (%s) as bar%s" %(sql, qry_string)}

#The list of instruments attached to files.
def instrument_id_sql(sql):
	sql = """
select substring(g.type from 12) as instrument_id from (
with recursive t(group_id) as (
select group_id from (%s) as foo, myemsl.group_items as gi where gi.item_id = foo.item_id group by gi.group_id
 union all select myemsl.subgroups.parent_id as group_id from myemsl.subgroups, t where myemsl.subgroups.child_id = t.group_id) select group_id from t) as tmp, myemsl.groups as g where tmp.group_id = g.group_id and g.type like 'Instrument.%%'
""" %(sql)
	return sql

def instrument_id_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = instrument_id_sql(sql)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		sql = """
select type, name, subdir, transaction, files.item_id, aged from (%s) as files, (select item_id from myemsl.group_items, (with recursive t(group_id) as (select myemsl.groups.group_id from myemsl.groups where myemsl.groups.type = 'Instrument.%s' union all select child_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id) select group_id from t) as groups where myemsl.group_items.group_id = groups.group_id) as items where files.item_id = items.item_id
""" %(sql, pg_escape_string(query[arg_offset]))
	return {"done":False, "consumed":1, "sql":sql}

def instrument_name_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select name_short from (%s) as foo, eus.instruments as i where i.instrument_id = foo.instrument_id::integer" %(instrument_id_sql(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		sql = """
select type, name, subdir, transaction, files.item_id, aged from (%s) as files, (select item_id from myemsl.group_items, (with recursive t(group_id) as (select myemsl.groups.group_id from myemsl.groups, eus.instruments where eus.instruments.name_short = '%s' and myemsl.groups.type = 'Instrument.' || eus.instruments.instrument_id union all select child_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id) select group_id from t) as groups where myemsl.group_items.group_id = groups.group_id) as items where files.item_id = items.item_id
""" %(sql, pg_escape_string(query[arg_offset]))
	return {"done":False, "consumed":1, "sql":sql}

#FIXME this query returns all proposals that are attached to any file. No permission checks are done.
def proposal_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = """
select eus.proposals.proposal_id from (with recursive t(group_id) as (select myemsl.group_items.group_id from (%s) as foo, myemsl.items, myemsl.group_items where foo.item_id = myemsl.items.item_id and myemsl.items.item_id = myemsl.group_items.item_id group by myemsl.group_items.group_id union all select myemsl.subgroups.parent_id as group_id from myemsl.subgroups, t where myemsl.subgroups.child_id = t.group_id) select group_id from t) as groups, eus.proposals where eus.proposals.group_id = groups.group_id group by eus.proposals.proposal_id;
""" %(sql)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		qry_string =  " where eus.proposals.proposal_id = '%s'" %(pg_escape_string(query[arg_offset]))
	sql = """
select type, name, subdir, transaction, files.item_id, aged from (%s) as files, (select item_id from myemsl.group_items, (with recursive t(group_id) as (select eus.proposals.group_id from eus.proposals%s union all select child_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id) select group_id from t) as groups where myemsl.group_items.group_id = groups.group_id) as items where files.item_id = items.item_id
""" %(sql, qry_string)
	return {"done":False, "consumed":1, "sql":sql}

def group_name_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
#FIXME upper
		sql = "select myemsl.groups.name from myemsl.group_items, myemsl.groups, (%s) as d where myemsl.group_items.item_id = d.item_id and myemsl.group_items.group_id = myemsl.groups.group_id and myemsl.groups.name != '' group by myemsl.groups.name" %(sql)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	sql = """
select type, name, subdir, transaction, files.item_id, aged from (%s) as files, (select item_id from myemsl.group_items, (with recursive t(group_id) as (select myemsl.groups.group_id from myemsl.groups where myemsl.groups.name = '%s' union all select child_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id) select group_id from t) as groups where myemsl.group_items.group_id = groups.group_id) as items where files.item_id = items.item_id
""" %(sql, pg_escape_string(query[arg_offset]))
	return {"done":False, "consumed":1, "sql":sql}

def group_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	l = len(query) - arg_offset
	sys.stderr.write("len %s\n" %(l))
	if l == 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
			return {"done":True}
		if query[arg_offset] == '-any-':
			sql = "select myemsl.groups.name from myemsl.group_items, myemsl.groups, (%s) as d where myemsl.group_items.item_id = d.item_id and myemsl.group_items.group_id = myemsl.groups.group_id and myemsl.groups.name != '' group by myemsl.groups.name" %(sql)
		else:
			sql = "select myemsl.groups.name from myemsl.group_items, myemsl.groups, (%s) as d where myemsl.group_items.item_id = d.item_id and myemsl.group_items.group_id = myemsl.groups.group_id and myemsl.groups.name != '' and myemsl.groups.type = '%s' group by myemsl.groups.name" %(sql, pg_escape_string(query[arg_offset]))
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	elif l < 2:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select myemsl.groups.type from myemsl.group_items, myemsl.groups, (%s) as d where myemsl.group_items.item_id = d.item_id and myemsl.group_items.group_id = myemsl.groups.group_id and myemsl.groups.name != '' group by myemsl.groups.type" %(sql)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 2 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-' or query[arg_offset + 1] != '-any-':
		qry_string = ' where '
		if query[arg_offset + 1] != '-any-':
			qry_string += "myemsl.groups.name = '%s'" %(pg_escape_string(query[arg_offset + 1]))
			if query[arg_offset] != '-any-':
				qry_string += ' and '
		if query[arg_offset] != '-any-':
			qry_string += "myemsl.groups.type = '%s'" %(pg_escape_string(query[arg_offset]))
	sql = """
select type, name, subdir, transaction, files.item_id, aged from (%s) as files, (select item_id from myemsl.group_items, (with recursive t(group_id) as (select myemsl.groups.group_id from myemsl.groups%s union all select child_id from myemsl.subgroups, t where myemsl.subgroups.parent_id = t.group_id) select group_id from t) as groups where myemsl.group_items.group_id = groups.group_id) as items where files.item_id = items.item_id
""" %(sql, qry_string)
	return {"done":False, "consumed":2, "sql":sql}

def raw_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	l = len(query) - arg_offset
	sys.stderr.write("len %s\n" %(l))
	if l == 2:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
			return {"done":True}
		if query[arg_offset] == '-any-':
			sql = "select transaction from (%s) as d group by d.transaction" %(sql)
		else:
			sql = "select d.transaction from (%s) as d, myemsl.transactions where d.transaction = myemsl.transactions.transaction and myemsl.transactions.submitter = '%s' group by d.transaction" %(sql, pg_escape_string(query[arg_offset]))
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if l == 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
			return {"done":True}
		dirs = []
		dirs.append({"name":'bundle'})
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	elif l < 3:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select myemsl.transactions.submitter from myemsl.transactions, (%s) as d where myemsl.transactions.transaction = d.transaction group by myemsl.transactions.submitter" %(sql)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 3 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	sql = """
		select type, name, subdir, d.transaction, item_id, aged from (%s) as d, myemsl.transactions where myemsl.transactions.transaction = d.transaction and d.transaction = %s and myemsl.transactions.submitter = %s
""" %(sql, int(query[arg_offset + 2]), int(query[arg_offset]))
	return {"done":False, "consumed":3, "sql":sql}

def item_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	l = len(query) - arg_offset
	sys.stderr.write("len %s\n" %(l))
	if l < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select d.item_id from (%s) as d group by d.item_id" %(sql)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		qry_string = " where item_id = %s" %(int(query[arg_offset]))
	sql = """
		select type, name, subdir, d.transaction, item_id, aged from (%s) as d %s
""" %(sql, qry_string)
	return {"done":False, "consumed":1, "sql":sql}

def transaction_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	l = len(query) - arg_offset
	sys.stderr.write("len %s\n" %(l))
	if l < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select d.transaction from (%s) as d group by d.transaction order by d.transaction" %(sql)
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		qry_string = " where transaction = %s" %(int(query[arg_offset]))
	sql = """
		select type, name, subdir, d.transaction, item_id, aged from (%s) as d%s
""" %(sql, qry_string)
	return {"done":False, "consumed":1, "sql":sql}

def submit_time_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select stime from (%s) as foo, myemsl.transactions where foo.transaction = myemsl.transactions.transaction group by myemsl.transactions.stime order by myemsl.transactions.stime" %(sql)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	qry_string = ''
	if query[arg_offset] != '-any-':
		qry_string = ", myemsl.transactions where stime='%s' and myemsl.transactions.transaction = bar.transaction" %(pg_escape_string(query[arg_offset]))
	return {"done":False, "consumed":1, "sql":"select type, name, subdir, bar.transaction, item_id, aged from (%s) as bar%s" %(sql, qry_string)}

def directly_derived_from_item_function(query, sql, arg_offset, later, user, after_data, op, auth_add, writer, config=None):
	if len(query) - arg_offset < 1:
		if op == "stat":
			return_document([{"name":"stat"}], None, None, DOCUMENT_FILTERS, True, op, auth_add, user, writer)
			return {"done":True}
		sql = "select ai.item_id from (%s) as foo, myemsl.action_output_items as ao, myemsl.action_input_items as ai where foo.item_id = ai.item_id and ai.action_id = ao.action_id group by ai.item_id order by ai.item_id" %(sql)
		cnx = myemsldb_connect(myemsl_schema_versions=['1.0'], dbconf=config)
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		dirs = []
		for row in rows:
			dirs.append({"name":row[0]})
		if len(dirs) == 0:
			dirs = None
		return_document(dirs, None, None, DOCUMENT_FILTER_ARGS, after_data, op, False, user, writer)
		return {"done":True}
	if len(query) - arg_offset == 1 and op == "stat":
		return_document([{"name":"stat"}], None, None, DOCUMENT_FILTER_ARGS, True, op, auth_add, user, writer)
		return {"done":True}
	return {"done":False, "consumed":1, "sql":"select type, name, subdir, transaction, bar.item_id, aged from (%s) as bar, myemsl.action_output_items as ao, myemsl.action_input_items as ai where ai.item_id = %s and ai.action_id = ao.action_id and ao.item_id = bar.item_id" %(sql, int(query[arg_offset]))}

funcs = {"submitter":submitter_function, "proposal":proposal_function, "group":group_function, "group_name":group_name_function, "submit_time":submit_time_function, "raw":raw_function, "directly_derived_from_item":directly_derived_from_item_function, "item":item_function, "transaction":transaction_function, "instrument_id":instrument_id_function, "instrument_name":instrument_name_function, "data":data_function}

if __name__ == '__main__':
	sys.exit(base_query(sys.argv[1], sys.argv[2], False, sys.stdout))

