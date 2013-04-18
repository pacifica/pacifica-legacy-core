#!/usr/bin/python

import myemsl.elasticsearch.metadata
from myemsl.dbconnect import myemsldb_connect

class metadata:
	def __init__(self, mdp):
		self.person_id = {}
		sql = "select person_id, network_id, first_name, last_name from eus.users"
		cnx = myemsldb_connect(myemsl_schema_versions=['1.2'])
		cursor = cnx.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		for row in rows:
			self.person_id[row[0]] = {'name': "%s %s" %(row[2], row[3]), 'network_id': str(row[1]).lower(), 'id': row[0]}
		
		instrument = {None: None}
		mdp.register_join('gov_pnnl_emsl_instrument', instrument)
		sql = "select instrument_id, name_short from eus.instruments"
		cursor = cnx.cursor()
		cursor.execute(sql)
		row = cursor.fetchone()
		while row:
			instrument[row[0]] = {'id': row[0], 'name': row[1]}
			row = cursor.fetchone()
		cnx.close()

		mdp.register_join('gov_pnnl_emsl_proposal', myemsl.elasticsearch.metadata.entry_to_id)

		mdp.emsl_basic_metadata = self

	def pid2info(self, user):
		return self.person_id.get(user)

