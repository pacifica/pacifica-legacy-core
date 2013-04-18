#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")

import os
import pgdb
import time
import StringIO
import ConfigParser
from myemsl import dbconnect

class TestingDB:
	def __init__(self):
		self. port = 7592
		self.datadir = "/tmp/myemsldb.%s" %(self.port)
		self.root = True
	def failUnless(self, res, reason):
		if not res:
			sys.stderr.write("%s\n")
			sys.exit(-1)
	def tearDown(self):
		pg_stop = "pg_ctl stop -m fast -D \"%s\"" %(self.datadir)
		if self.root:
			pg_stop = "su - postgres -c '%s'" %(pg_stop)
		res = os.system(pg_stop)
		self.failUnless(res == 0, "Failed to stop postgres")
        def setUp(self):
		pg_rmdb = "rm -rf \"%s\"" %(self.datadir)
		pg_initdb = "(echo test; echo test) | initdb -D \"%s\" --pwprompt" %(self.datadir)
		pg_setport = "echo port = %s >> %s/postgresql.conf" %(self.port, self.datadir)
		pg_start = "pg_ctl start -D \"%s\"" %(self.datadir)
		if self.root:
			pg_initdb = "su - postgres -c '%s'" %(pg_initdb)
			pg_start = "su - postgres -c '%s'" %(pg_start)
		res = os.system(pg_rmdb)
		res = os.system(pg_initdb)
		self.failUnless(res == 0, "Failed to init postgres")
		res = os.system(pg_setport)
		self.failUnless(res == 0, "Failed to set postgres port")
		res = os.system(pg_start)
		self.failUnless(res == 0, "Failed to start postgres")
		time.sleep(2)
		sqldir = '/home/kfox/svn/myemsl2/myemsl2/trunk/src/pgsql_schema'
		sql = "psql -h localhost -p %s -U postgres -c '\i %s/myemsl_users.sql'" %(self.port, sqldir)
		res = os.system(sql)
		sql = "(LOCATION='%s'; echo -e 'create schema eus;ALTER SCHEMA eus OWNER TO metadata_admins;set search_path = eus, public;'; cat $LOCATION/eus.sql $LOCATION/myemsl.sql $LOCATION/eus_auth.sql $LOCATION/myemsl_authz.sql) | psql -h localhost -p %s -U postgres myemsl_metadata" %(sqldir, self.port)
		res = os.system(sql)
		
		config = ConfigParser.SafeConfigParser()
		config.read('myemsl_testdb.ini')
		self.config = config
		cnx = dbconnect.myemsldb_connect(dbconf = config, myemsl_schema_versions=['1.0'])
		cursor = cnx.cursor()
		sql = "\n".join(["insert into eus.users(person_id, network_id) values(%s, 'user%s');" %(i, i) for i in range(1, 2+1)])
		cursor.execute(sql)
		sql = "\n".join(["insert into myemsl.items(item_id, type) values(%s, 'file');" %(i) for i in range(1, 8+1)])
		cursor.execute(sql)
		sql = """
		insert into myemsl.transactions(transaction, submitter) values(1, 1);
		insert into myemsl.transactions(transaction, submitter) values(2, 2);
		insert into myemsl.transactions(transaction, submitter) values(3, 1);
		insert into myemsl.transactions(transaction, submitter) values(4, 2);
		"""
		cursor.execute(sql)
		sql = """
		insert into myemsl.files(name, subdir, transaction, item_id) values('f1', '', 1, 1);
		insert into myemsl.files(name, subdir, transaction, item_id) values('f2', '', 2, 2);
		insert into myemsl.files(name, subdir, transaction, item_id) values('f3', '', 1, 3);
		insert into myemsl.files(name, subdir, transaction, item_id, aged) values('f4', '', 2, 4, 'Y');
		insert into myemsl.files(name, subdir, transaction, item_id, aged) values('f5', '', 3, 5, 'Y');
		insert into myemsl.files(name, subdir, transaction, item_id) values('f6', '', 3, 6);
		insert into myemsl.files(name, subdir, transaction, item_id) values('f5', '', 4, 7);
		insert into myemsl.files(name, subdir, transaction, item_id, aged) values('f6', '', 4, 8, 'Y');
		"""
		cursor.execute(sql)
		sql = """
		insert into myemsl.groups(group_id, type, name) values(1, 'proposal', 'prop1');
		insert into myemsl.groups(group_id, type, name) values(2, 'proposal', 'prop2');
		insert into myemsl.groups(group_id, type, name) values(3, 'project', 'uberproj');
		insert into myemsl.groups(group_id, type, name) values(4, 'subproposal', 'subproposal1');
		insert into myemsl.groups(group_id, type, name) values(5, 'subproposal', 'subproposal2');
		"""
		cursor.execute(sql)
		sql = """
		insert into myemsl.subgroups(parent_id, child_id) values(3, 1);
		insert into myemsl.subgroups(parent_id, child_id) values(3, 2);
		insert into myemsl.subgroups(parent_id, child_id) values(1, 4);
		insert into myemsl.subgroups(parent_id, child_id) values(2, 5);
		"""
		cursor.execute(sql)
		sql = """
		insert into eus.proposals(group_id, proposal_id, title) values(1, 'prop1', 'Proposal number 1');
		insert into eus.proposals(group_id, proposal_id, title) values(2, 'prop2', 'Proposal number 2');
		"""
		cursor.execute(sql)
		sql = """
		insert into eus.proposal_members(proposal_member_id, proposal_id, person_id, active) values(1, 'prop1', 1, 'Y');
		insert into eus.proposal_members(proposal_member_id, proposal_id, person_id, active) values(2, 'prop2', 2, 'Y');
		insert into eus.proposal_members(proposal_member_id, proposal_id, person_id, active) values(3, 'prop2', 1, 'Y');
		"""
		cursor.execute(sql)
		sql = """
		insert into myemsl.group_items(group_id, item_id) values(4, 1);
		insert into myemsl.group_items(group_id, item_id) values(5, 2);
		"""
		cursor.execute(sql)
#Permission bits:
		sql = """
		insert into myemsl.permission_group(permission_group_id, type, name) values(1, 'RBAC', 'testgroup');
		insert into myemsl.permission_group(permission_group_id, type, name) values(2, 'EUS', 'testgroup2');
		insert into myemsl.permission_group_members(permission_group_id, person_id) values(1, 1);
		insert into myemsl.permission_group_members(permission_group_id, person_id) values(2, 2);
		insert into myemsl.permission_set(permission_set_id) values(1);
		insert into myemsl.permission_set(permission_set_id) values(2);
		insert into myemsl.permission_set_perms(permission_set_id, permission) values(1, 'p');
		insert into myemsl.permission_set_perms(permission_set_id, permission) values(1, 'a');
		insert into myemsl.permission_set_perms(permission_set_id, permission) values(2, 'a');
		insert into myemsl.permissions(permission_set_id, permission_group_id, permission_class) values(1, 1, 'instrument.test');
		insert into myemsl.permissions(permission_set_id, permission_group_id, permission_class) values(2, 2, 'instrument.test');
		"""
		cursor.execute(sql)
		cnx.commit()
		cnx.close()
#		sql = "psql -h localhost -p %s -U postgres myemsl_metadata" %(port)
#		res = os.system(sql)
		return None

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.stderr.write("You must specify either start or stop\n")
		sys.exit(1)
	db = TestingDB()
	if sys.argv[1] == 'stop':
		db.tearDown()
	elif sys.argv[1] == 'start':
		db.setUp()
	else:
		sys.stderr.write("Unknown action\n")
		sys.exit(1)
