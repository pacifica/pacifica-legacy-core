#!/usr/bin/python

import os
import sys
import errno
import urllib
import time
import simplejson as json
from myemsl.dbconnect import myemsldb_connect
from pymongo import Connection as mongoconnection
from myemsl.getconfig import getconfig_notification
config = getconfig_notification('jmds')
from threading import Thread, Lock

from myemsl.logging import getLogger

logger = getLogger(__name__)

#FIXME move this to util. shared in jsondumper too.
def cursoriter(cursor):
	while True:
		val = cursor.fetchone()
		if val:
			yield val
		else:
			return

#FIXME make this plugable
class dms_users:
	def __init__(self):
		self.writerlock = Lock()
		self.last_update = 0
		pass
	def get(self):
		self.writerlock.acquire()
		if self.last_update + 60 * 60 < int(time.time()):
			self.refresh_dms_users()
		d = self.dms_users
		self.writerlock.release()
		return d
	def refresh_dms_users(self):
		cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
		cursor = cnx.cursor()
		sql = """
select distinct person_id from myemsl.permission_group as pg, myemsl.permission_group_members as pgm where pg.name='MyEMSL.Downloader.omics.dms' and pg.permission_group_id = pgm.permission_group_id order by person_id;
"""
		cursor.execute(sql)
		self.dms_users = []
		for row in cursoriter(cursor):
			self.dms_users.append(row[0])

dms_users_plug = dms_users()

def itemusers(item_id, req, retries=1):
	client = mongoconnection(config.notification.hostname, config.notification.port)
	collection = client['pacifica_db']['jmds_collection']
	code = 404
	item_id = int(item_id)
	f = collection.find({"_id":item_id})
	for doc in f:
		list = {}
		if 'agd' not in doc or doc['agd'] == False:
			if 'submitter' in doc:
				list[doc['submitter']] = 1
			if 'trusted' in doc:
				trusted = doc['trusted']
				if 'gov_pnnl_emsl_my/dms/datapackage' in trusted or 'gov_pnnl_emsl_my/dms/dataset' in trusted:
					for i in dms_users_plug.get():
						list[i] = 1
				extended_metadata = doc.get('extended_metadata')
				if extended_metadata:
#FIXME Plugin related stuff...
					for x in ['gov_pnnl_emsl_dms_pi', 'gov_pnnl_emsl_dms_technical_lead', 'gov_pnnl_emsl_dms_proj_mgr', 'gov_pnnl_emsl_dms_researcher', 'gov_pnnl_emsl_dms_dataset_operator']:
						l = extended_metadata.get(x)
						if l:
							for i in l:
								list[i['id']] = 1
		list = list.keys()
		list.sort()
		req.write(json.dumps(list))
		req.write("\n")
		code = 200
		break
	return code

if __name__ == '__main__':
	res = itemusers(sys.argv[1], sys.stdout)
	print res
	sys.exit(res)

