import sys
import time
import sqlite3

class trustifier_state:
	def create_schema(self, conn):
		c = conn.cursor()

		sql="""
CREATE TABLE system(
	name STRING PRIMARY KEY,
	value STRING
);
CREATE UNIQUE INDEX system1 ON system(name);
CREATE TABLE ruletype(
	ruletype_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name STRING NOT NULL
);
CREATE UNIQUE INDEX ruletype1 ON ruletype(name);
CREATE TABLE usersetids(
	userset_id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE userset(
	userset_id INTEGER NOT NULL,
	user_id INT8 NOT NULL,
	FOREIGN KEY(userset_id) REFERENCES usersetids(userset_id)
);
CREATE TABLE rule(
	rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
	ruletype_id INTEGER NOT NULL,
	predicate STRING NOT NULL,
	extra STRING NOT NULL,
	FOREIGN KEY(ruletype_id) REFERENCES ruletype(ruletype_id)
);
CREATE UNIQUE INDEX rule1 ON rule(ruletype_id, predicate, extra);
CREATE TABLE range(
	range_id INTEGER PRIMARY KEY AUTOINCREMENT,
	start INT8 NOT NULL DEFAULT (strftime('%s','now')),
	end INT8
);
CREATE TABLE window(
	rule_id INTEGER NOT NULL,
	range_id INTEGER NOT NULL,
	userset_id INTEGER,
	FOREIGN KEY(rule_id) REFERENCES rule(rule_id),
	FOREIGN KEY(range_id) REFERENCES range(range_id),
	FOREIGN key(userset_id) REFERENCES userset(userset_id)
);
CREATE UNIQUE INDEX window1 ON window(rule_id, range_id, userset_id);
INSERT INTO system(name, value) VALUES('version', '1.0');
"""
		for s in sql.split(';'):
			try:
				conn.execute(s)
			except sqlite3.OperationalError, e:
				print s
				raise
	def ruletype_get(self, conn, name):
		res = None
		sql = """
SELECT
	ruletype_id
FROM 
	ruletype
WHERE
	name = :name
"""
		cur = conn.cursor()
		cur.execute(sql, {"name":name})
		found = False
		for row in cur.fetchall():
			found = True
			res = row[0]
		if found == False:
			sql = """
INSERT INTO ruletype(name) VALUES(:name);
"""
			cur = conn.execute(sql, {"name": name})
			res = cur.lastrowid
			conn.commit()
		return res

	def rules_of_type_get(self, conn, name):
		sql = """
SELECT
	rule_id,
	predicate,
	extra
FROM 
	rule,
	ruletype
WHERE
	rule.ruletype_id = ruletype.ruletype_id AND
	ruletype.name = :name
"""
		cur = conn.cursor()
		cur.execute(sql, {"name":name})
		for row in cur.fetchall():
			print row
	def userset_compare(self, conn, userlist, userset_id):
		s = dict([(i, 1) for i in userlist])
		sql = """
SELECT
        user_id
FROM 
        userset
WHERE
	userset_id = :userset_id
"""
		cur = conn.cursor()
		cur.execute(sql, {"userset_id":userset_id})
		row = cur.fetchone()
		while row != None:
			try:
				del s[row[0]]
			except KeyError, e:
				return False
			row = cur.fetchone()
		if len(s) == 0:
			return True
		return False
	def userset_id_of_users(self, conn, userlist):
		count = len(userlist)
		sql = """
SELECT
        userset_id,
        count(userset_id) AS c
FROM 
        userset
GROUP BY
        userset_id
HAVING
	c = :count;
"""
		found = False
		cur = conn.cursor()
		cur.execute(sql, {"count":len(userlist)})
		row = cur.fetchone()
		while row != None:
			found = self.userset_compare(conn, userlist, row[0])
			if found:
				userset_id = row[0]
				break
			row = cur.fetchone()
		if found == False:
			cur2 = conn.cursor()
			sql = """
INSERT INTO usersetids(userset_id) VALUES(NULL);
"""
			cur2.execute(sql)
			userset_id = cur2.lastrowid
			sql = """
INSERT INTO userset(userset_id, user_id) VALUES(?, ?);
"""
			cur2.executemany(sql, [(userset_id, i) for i in userlist])
			conn.commit()
		print userset_id
	def rule_id_of_rule(self, conn, typename, predicate, extra):
		sql = """
SELECT
	rule_id
FROM 
	rule,
	ruletype
WHERE
	predicate = :predicate AND
	extra = :extra AND
	rule.ruletype_id = ruletype.ruletype_id AND
	ruletype.name = :name
"""
		found = False
		cur = conn.cursor()
		cur.execute(sql, {'predicate':predicate, 'extra':extra, 'name':typename})
		row = cur.fetchone()
		while row != None:
			found = True
			return row[0]
		ruletype_id = self.ruletype_get(conn, typename)
		cur2 = conn.cursor()
		sql = """
INSERT INTO rule(predicate, extra, ruletype_id) VALUES(:predicate, :extra, :ruletype_id);
"""
		cur2.execute(sql, {'predicate':predicate, 'ruletype_id':ruletype_id, 'extra':extra})
		userset_id = cur2.lastrowid
		conn.commit()
		print userset_id
	def range_id_get(self, conn, start, end=None):
		res = None
		if end == None:
			sql = """
SELECT
	range_id
FROM 
	range
WHERE
	start = :start AND
	end is NULL
"""
		else:
			sql = """
SELECT
	range_id
FROM 
	range
WHERE
	start = :start AND
	end = :end
"""
		cur = conn.cursor()
		cur.execute(sql, {"start":start, "end":end})
		found = False
		for row in cur.fetchall():
			found = True
			res = row[0]
		if found == False:
			if end == None:
				sql = """
INSERT INTO range(start) VALUES(:start);
"""
			else:
				sql = """
INSERT INTO range(start, end) VALUES(:start, :end);
"""
			cur = conn.execute(sql, {"start":start, "end":end})
			res = cur.lastrowid
			conn.commit()
		return res

conn = sqlite3.connect('/var/lib/pacifica/trustifier.sdb')
ts = trustifier_state()
#ts.create_schema(conn)
#print ts.rules_of_type_get(conn, sys.argv[1])
#print ts.userset_id_of_users(conn, [1,2,3,5,7])
print ts.rule_id_of_rule(conn, "rbacfoo", "foopred2", "d7")
ts.rules_of_type_get(conn, 'rbacfoo')
print ts.range_id_get(conn, int(time.time()))
