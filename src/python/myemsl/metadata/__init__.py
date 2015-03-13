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

def get_user_info(userid):
    ##
    # get user information from EUS
    ##
    sql = """
SELECT
  person_id,
  network_id,
  first_name,
  last_name,
  email_address,
  last_change_date
FROM
  eus.users
WHERE
  person_id=%(person_id)d
    """
    cnx = myemsldb_connect(myemsl_schema_versions=['1.8'])
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':userid})
    rows = cursor.fetchall()
    if len(rows) != 1:
        error(dtype, "multiple users with (%s)"%(userid), writer)
    (person_id, network_id, first_name, last_name, email_address, last_change_date) = rows[0]
    data = {
        "person_id": person_id,
        "network_id": network_id,
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
        "last_change_date": last_change_date,
        "proposals": {},
        "instruments": {}
    }
    return data

def get_custodian_instruments(userid):
    ##
    # This pulls the instruments from custodians and gets
    # the associated proposals
    ##
    sql = """
SELECT
  instrument_id
FROM
  eus.emsl_staff_inst
WHERE
  person_id = %(person_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':userid})
    return [ i[0] for i in cursor.fetchall() ]

def get_proposals_from_instrument(instid):
    sql = """
SELECT
  proposal_id
FROM
  eus.proposal_instruments
WHERE
  proposal_instruments.instrument_id = %(instrument_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'instrument_id':instid})
    return [ i[0] for i in cursor.fetchall() ]

def get_proposals_from_user(userid):
    ##
    # Get the proposals the user is on
    ##
    sql = """
SELECT
  proposal_id
FROM
  eus.proposal_members
WHERE
  person_id = %(person_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'person_id':userid})
    return [ i[0] for i in cursor.fetchall() ]

def get_proposal_info(proposal_id):
    sql = """
SELECT
  proposal_id,
  title,
  group_id,
  accepted_date,
  actual_end_date,
  actual_start_date,
  closed_date
FROM
  eus.proposals
WHERE
  proposal_id = %(proposal_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'proposal_id':proposal_id})
    data = {}
    rows = cursor.fetchall()
    if len(rows) == 1:
        (   
            proposal_id,
            title,
            group_id,
            accepted_date,
            actual_end_date,
            actual_start_date,
            closed_date
        ) = rows[0]
        data[str(proposal_id)] = {
            "title": title,
            "group_id": group_id,
            "accepted_date": accepted_date,
            "actual_end_date": actual_end_date,
            "actual_start_date": actual_start_date,
            "closed_date": closed_date,
            "instruments": []
        }
    return data

def get_instruments_from_proposal(proposal_id):
    sql = """
SELECT
  instrument_id
FROM
  eus.proposal_instruments
WHERE
  proposal_instruments.proposal_id = %(proposal_id)s
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'proposal_id':proposal_id})
    return [ i[0] for i in cursor.fetchall() ]

def get_instrument_info(instrument_id):
    sql = """
SELECT
  instrument_id,
  instrument_name,
  last_change_date,
  name_short,
  eus_display_name,
  active_sw
FROM
  eus.instruments
WHERE
  eus.instruments.instrument_id = %(instrument_id)d
    """
    cursor = cnx.cursor()
    cursor.execute(sql, {'instrument_id':instrument_id})
    rows = cursor.fetchall()
    data = {}
    if len(rows) == 1:
        (   
            instrument_id,
            instrument_name,
            last_change_date,
            name_short,
            eus_display_name,
            active_sw
        ) = rows[0]
        data["instruments"][str(instrument_id)] = {
            "instrument_id": instrument_id,
            "instrument_name": instrument_name,
            "last_change_date": last_change_date,
            "name_short": name_short,
            "eus_display_name": eus_display_name,
            "active_sw": active_sw
        }
    return data

