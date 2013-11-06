#!/usr/bin/python

from myemsl.dbconnect import do_sql_insert, do_sql_select, myemsldb_connect

def child_group_of_parent_check_by_id(parent_id, child_id):
	sql = """
WITH RECURSIVE
  t(group_id)
AS (
  SELECT
    parent_id AS group_id
  FROM
    myemsl.subgroups AS s
  WHERE
    s.child_id = %(child_id)s
UNION ALL
  SELECT
    myemsl.subgroups.parent_id AS group_id
  FROM
    myemsl.subgroups, t
  WHERE
    myemsl.subgroups.child_id = t.group_id
)
SELECT
  true
FROM
  t
WHERE
  t.group_id = %(parent_id)s
GROUP BY
  g.type, g.name;
"""
	rows = do_sql_select(sql, True, myemsl_schema_versions=['1.0'], params={'parent_id':parent_id, 'child_id':child_id})
	try:
		return rows[0][0]
	except:
		return False

def child_group_of_parent_check(parent_type, parent_name, child_type, child_name):
	sql = """
WITH RECURSIVE
  t(group_id)
AS (
  SELECT
    parent_id AS group_id
  FROM
    myemsl.subgroups AS s, myemsl.groups AS g
  WHERE
    s.child_id = g.group_id AND type=%(child_type)s AND name=%(child_name)s
UNION ALL
  SELECT
    myemsl.subgroups.parent_id AS group_id
  FROM
    myemsl.subgroups, t
  WHERE
    myemsl.subgroups.child_id = t.group_id
)
SELECT
  true
FROM
  t, myemsl.groups AS g
WHERE
  t.group_id = g.group_id AND g.type=%(parent_type)s AND g.name=%(parent_name)s
GROUP BY
  g.type, g.name;
"""
	rows = do_sql_select(sql, True, myemsl_schema_versions=['1.0'], params={'parent_type':parent_type, 'parent_name':parent_name, 'child_type':child_type, 'child_name':child_name})
	try:
		return rows[0][0]
	except:
		return False

def update_transaction_stime(trans):
	sql = """
UPDATE
  myemsl.transactions
SET
  stime=now()
WHERE
  transaction=%(trans)s
RETURNING
  stime AT TIME ZONE current_setting('TIMEZONE');
"""
	res = do_sql_select(sql, True, myemsl_schema_versions=['1.0'], params={'trans':str(trans)});
	if res and len(res) > 0 and len(res[0]) > 0:
		res = res[0][0]
	return res

def insert_file(trans, subdir, name, size, hashsum, groups, cursor=None):
	"""Insert file into database. Returns the item_id of the file inserted."""
	insert_item('file', cursor)
	sql = """
INSERT INTO
  myemsl.files
  (
    item_id,
    transaction,
    subdir,
    name,
    size
  )
VALUES
  (
    currval(pg_get_serial_sequence('myemsl.items', 'item_id')), 
    %(trans)i,
    %(subdir)s,
    %(name)s,
    %(size)i
);
INSERT INTO
  myemsl.hashsums
  (
    item_id,
    hashtime,
    hashsum,
    hashtype
  ) 
VALUES
  (
    currval(pg_get_serial_sequence('myemsl.items', 'item_id')),
    now(),
    %(sum)s,
    %(type)s
);
SELECT
  currval(pg_get_serial_sequence('myemsl.items', 'item_id'))
;
"""
	if not cursor:
		cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
		cursor = cnx.cursor()
	cursor.execute(sql, params={'trans':int(trans), 'subdir':str(subdir), 'name':str(name), 'size':int(size), 'type':'sha1', 'sum':hashsum})
	found = False
	rows = cursor.fetchall()
	for row in rows:
		id = row[0]
		found = True
	if found != True:
		raise Exception("Could not get id")
	for group in groups:
		sql = """
INSERT INTO
  myemsl.group_items(group_id, item_id)
VALUES
  (%(gid)i, currval(pg_get_serial_sequence('myemsl.items', 'item_id')));
"""
		cursor.execute(sql, params={'gid':get_group_id(group['name'], group['type'])})
	if not cursor:
		try:
			cnx.commit()
		except Exception, ex:
			cnx.rollback()
		cnx.close()
	return id

def insert_item(item_type, cursor=None):
	sql = """
INSERT INTO
  myemsl.items(type)
VALUES
  (%(type)s);
"""
	if cursor:
		cursor.execute(sql, params={'type':item_type})
	else:
		do_sql_insert(sql, False, myemsl_schema_versions=['1.3'], params={'type':item_type})

def insert_group(grp_name, grp_type):
	sql = """
INSERT INTO
  myemsl.groups(name, type) 
VALUES
  (%(name)s, %(type)s);
"""
	do_sql_insert(sql, True, myemsl_schema_versions=['1.0'], params={'name':str(grp_name), 'type':str(grp_type)})

def insert_subgroup(child_id, parent_id):
	sql = """
INSERT INTO
  myemsl.subgroups(child_id, parent_id)
VALUES
  (%(child_id)s, %(parent_id)s);
"""
	do_sql_insert(sql, True, myemsl_schema_versions=['1.0'], params={'child_id':str(child_id), 'parent_id':str(parent_id)})
	

def get_proposal_gid(prop):
	sql = """
SELECT
  group_id
FROM
  eus.proposals
WHERE
  eus.proposals.proposal_id = %(proposal)s;
"""
	rows = do_sql_select(sql, True, myemsl_schema_versions=['1.0'], params={'proposal':str(prop)})
	return rows[0][0]

def get_group_id(grp_name, grp_type):
	sql = """
SELECT
  group_id
FROM
  myemsl.groups
WHERE
  name = %(name)s and type = %(type)s;
"""
	rows = do_sql_select(sql, True, myemsl_schema_versions=['1.0'], params={'name':str(grp_name), 'type':str(grp_type)})
	return rows[0][0]
