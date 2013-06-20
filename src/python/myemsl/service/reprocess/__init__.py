#!/usr/bin/python

import sys
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

from myemsl.logging import getLogger

logger = getLogger(__name__)

def reprocess(person_id, name, method, xml):
	select_sql = """
SELECT
  definition
FROM
  myemsl.reprocessors
WHERE
  person_id = %(pid)i and
  name = %(name)s;
"""
	delete_sql = """
DELETE FROM
  myemsl.reprocessors
WHERE
  person_id = %(pid)i and
  name = %(name)s;
"""
	update_sql = """
UPDATE
  myemsl.reprocessors
SET
  definition=%(xml)s
WHERE
  person_id = %(pid)i and
  name = %(name)s
"""
	insert_sql = """
INSERT INTO
  myemsl.reprocessors
  (
    person_id,
    name,
    definition
  )
VALUES
  (
    %(pid)i,
    %(name)s,
    %(xml)s
  );
"""
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
	cursor = cnx.cursor()
	if method == "GET":
		cursor.execute(select_sql, {'pid':int(person_id), 'name':name})
		ret = cursor.fetchall()
		ret = "\n".join(ret[0])
	if method == "DELETE":
		cursor.execute(delete_sql, {'pid':int(person_id), 'name':name})
		ret = ""
	if method == "POST" or method == "PUT":
		# TODO validate xml using xsd
		cursor.execute(select_sql, {'pid':int(person_id), 'name':name})
		if len(cursor.fetchall()):
			cursor.execute(update_sql, {'pid':int(person_id), 'name':name, 'xml':xml})
		else:
			cursor.execute(insert_sql, {'pid':int(person_id), 'name':name, 'xml':xml})
		ret = ""
	cnx.commit()
	cnx.close()
	return ret
		
