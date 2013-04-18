#!/usr/bin/env python

import sys
import pgdb

from subprocess import PIPE, Popen

from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect

def nagios_rm_trans(transaction, req):
	transaction = int(transaction)
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	try:
		cursor = cnx.cursor()
		cursor.execute("""
SELECT
  a.t and b.t
FROM 
  (
    SELECT
      count(*)=2 as t
    FROM
      myemsl.files
    WHERE
      transaction=%d
  ) as a,
  (
    SELECT
      count(*)=1 as t
    FROM
      myemsl.files
    WHERE
      transaction=%d and
      name='Nagios Test.txt' and
      subdir=''
  ) as b""", [transaction, transaction])
		rows = cursor.fetchall()
		ok = False
		for row in rows:
			if row[0]:
				ok = True
		if not ok:
			cursor.execute("select count(*)=0 as t from myemsl.files as f where f.transaction=%i;", [transaction])
			rows = cursor.fetchall()
			ok = False
			for row in rows:
				if row[0]:
					ok = row[0]
			if not ok:
				raise Exception("Not correct number of files in bundle")
			else:
				req.write("OK\n")
				return
		cursor.execute("select count(*) from myemsl.files where transaction=%d and name='Nagios Test.txt' and subdir='';", [transaction])
		rows = cursor.fetchall()
		ok = False
		for row in rows:
			if row[0] == 1:
				ok = True
		if not ok:
			raise Exception("No Nagios Test.txt file found.")
		cursor.execute("create temporary table foo without oids on commit drop as select item_id from myemsl.files where transaction=%d;", [transaction])
		cursor.execute("delete from myemsl.hashsums where item_id in (select item_id from foo);")
		cursor.execute("delete from myemsl.group_items where item_id in (select item_id from foo);")
		cursor.execute("delete from myemsl.files where transaction=%d;", [transaction])
		cursor.execute("delete from myemsl.items where item_id in (select item_id from foo);")
		cursor.execute("delete from myemsl.transactions where transaction=%d;", [transaction])
		p1 = Popen(["/usr/bin/myemsl_nagios_rmtrans", '--transaction', str(transaction)], stdout=PIPE)
		print p1.communicate()
		res = p1.wait()
		if res == 0:
			req.write("OK\n")
			cnx.commit()
		else:
			cnx.rollback()
	except pgdb.DatabaseError, e:
		cnx.rollback()
		raise
	cnx.close()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "You must specify a transaction number."
		sys.exit(-1)
	nagios_rm_trans(sys.argv[1], sys.stdout)
