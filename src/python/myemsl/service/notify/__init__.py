#!/usr/bin/python

import sys
import urllib
import nntplib
import tempfile
import servicepoke
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def notify(transaction, writer):
#FIXME make configurable
	res = servicepoke.poke('/var/tmp/myemsl_elasticsearch', 'simple_items', 1)
	transaction = int(transaction)
	sql = """
select type, name, p.group_id is not NULL as proposal from (with recursive t(group_id) as (select group_id from myemsl.group_items, myemsl.files where transaction=%(trans)s and myemsl.group_items.item_id = myemsl.files.item_id group by group_id
union                                 
select parent_id as group_id from myemsl.subgroups as s, t where s.child_id = t.group_id
) select t.group_id, type, name from t, myemsl.groups as g where t.group_id = g.group_id
) as g left join eus.proposals as p on p.group_id = g.group_id;
	"""
	group_ids_for_item_id_sql = """
SELECT
  type,
  name,
  p.group_id is not NULL AS proposal
FROM (
  WITH RECURSIVE 
    t(group_id)
  AS (
    SELECT
      group_id
    FROM
      myemsl.group_items 
    WHERE
      myemsl.group_items.item_id = %(item_id)s 
    GROUP BY
      group_id                          
    UNION                                 
    SELECT
      parent_id AS group_id
    FROM
      myemsl.subgroups AS s,
      t
    WHERE
      s.child_id = t.group_id
  )
  SELECT
    t.group_id,
    type,
    name
  FROM 
    t,
    myemsl.groups AS g
  WHERE
    t.group_id = g.group_id
) as g
LEFT JOIN
  eus.proposals AS p ON p.group_id = g.group_id;
"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'trans':transaction})
	rows = cursor.fetchall()
	groups = []
	proposals = []
	for row in rows:
		type = row[0]
		name = row[1]
		is_proposal = row[2]
		groups.append([type, name])
		if is_proposal:
			proposals.append(name)
	sql = """
	select subdir, name, item_id from myemsl.files where transaction=%(trans)s;
	"""
	cursor = cnx.cursor()
	cursor.execute(sql, {'trans':transaction})
	rows = cursor.fetchall()
	filenames = []
	file_groups = {}
	for row in rows:
		subdir = row[0]
		name = row[1]
		if subdir == None:
			subdir = ''
		if subdir != '':
			subdir = "%s/" %(subdir)
		cursor = cnx.cursor()
		cursor.execute(group_ids_for_item_id_sql, {'item_id':row[2]})
		file_groups["%s%s" %(subdir, name)] = cursor.fetchall()
		filenames.append("%s%s" %(subdir, name))
	sql = """
	select submitter from myemsl.transactions where transaction=%(trans)s;
	"""
	cursor = cnx.cursor()
	cursor.execute(sql, {'trans':transaction})
	rows = cursor.fetchall()
	submitter = None
	for row in rows:
		submitter = row[0]
	nntp = nntplib.NNTP(config.get('notification', 'nntp_server'))
	f = tempfile.TemporaryFile(mode="w+")
	f.write("From: svc-myemsl <myemsl@my.emsl.pnl.gov>\n");
	f.write("Newsgroups: local.myemsl.incoming.notifications\n");
	f.write("Subject: %s\n" %(transaction));
	f.write("Mime-Version: 1.0\n");
	f.write("Content-Type: text/plain; charset=US-ASCII\n");
	f.write("Content-Transfer-Encoding: 7bit\n\n");
	f.write("<?xml version=\"1.0\"?>\n")
	f.write("<myemsl version=\"1.0.0\">\n")
	f.write("  <submitter>%s</submitter>\n" %(submitter))
	f.write("  <transaction>%s</transaction>\n" %(transaction))
	f.write("  <groups>\n")
	for (type, name) in groups:
		f.write("    <group><type>%s</type><name>%s</name></group>\n" %(type, name))
	f.write("  </groups>\n")
	f.write("  <proposals>\n")
	for name in proposals:
		f.write("    <proposal>%s</proposal>\n" %(name))
	f.write("  </proposals>\n")
	f.write("  <files>\n")
	for n in filenames:
		f.write("    <file>\n      <name>%s</name>\n      <groups>\n" %(n))
		for (type, name, is_proposal) in file_groups[n]:
			f.write("        <group><type>%s</type><name>%s</name></group>\n"% (type, name))
		f.write("      </groups>\n    </file>\n");
	f.write("  </files>\n")
	f.write("</myemsl>\n")
	f.seek(0)
	nntp.post(f)
	writer.write("OK")
	return 0

if __name__ == '__main__':
	sys.exit(notify(sys.argv[1], sys.stdout))

