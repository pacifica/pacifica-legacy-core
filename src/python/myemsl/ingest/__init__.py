#!/usr/bin/python

from socket import gethostname
from myemsl.callcurl import call_curl
from myemsl.getconfig import getconfig_secret
from myemsl.metadata import *
from myemsl.id2filename import id2dirandfilename
import os
import myemsl.util
import myemsl.getpermission
import xml.dom.minidom
config = getconfig_secret()

from myemsl.dbconnect import do_sql_insert as do_sql
from myemsl.dbconnect import do_sql_select as do_sql_select

"""
new_state

insert a new state line into the ingest_state table
"""
def new_state(jobid):
	sql = """
INSERT INTO
	myemsl.ingest_state(host,jobid)
VALUES
	(%(host)s,%(jobid)i);
"""
	params= {
		'jobid':int(jobid),
		'host':str(gethostname())
	}
	do_sql(sql, False, myemsl_schema_versions=['1.5'], params=params)

"""
update_state

Update the state in the database appropriately.

step values between [0-6]
status one of ['SUCCESS', 'ERROR', 'UNKNOWN']
message any text
"""
def update_state(jobid, step, status, message, host=None):
	sql = """
UPDATE
	myemsl.ingest_state
SET
	step = %(step)i,
	status = %(status)s,
	message = %(message)s
WHERE
	jobid = %(jobid)i and
	host = %(host)s;
"""
	if host == None:
		host = str(gethostname())
	params= {
		'step':int(step),
		'status':str(status),
		'message':str(message),
		'jobid':int(jobid),
		'host':host
	}
	do_sql(sql, False, myemsl_schema_versions=['1.5'], params=params)

def _update_int(jobid, value, column):
	sql = """
UPDATE
	myemsl.ingest_state
SET
	%(column)s = %%(value)i
WHERE
	jobid = %%(jobid)i and
	host = %%(host)s;
"""%{'column':column}
	params = {
		'value': int(value),
		'jobid':int(jobid),
		'host':str(gethostname())
	}
	do_sql(sql, False, myemsl_schema_versions=['1.5'], params=params)

def update_trans_id(jobid, trans_id):
	_update_int(jobid, trans_id, 'trans_id')

def update_person_id(jobid, person_id):
	_update_int(jobid, person_id, 'person_id')

#FIXME ideally, this function should be recoded to have item id's already allocated and files in their final position before this gets called. This is currently not the case.
def ingest_metadata(metadata, files, username, transaction, itemlogfilename):
	try:
		proposal = metadata['eusInfo']['proposalID']
	except:
		proposal = None
		pass
	try:
		subgroups = metadata['eusInfo']['subgroups']
	except:
		subgroups = []
		pass
	try:
		instrument = metadata['eusInfo']['instrumentName']
	except:
		instrument = None
		pass

	file_groups = []
	file_subgroups = []
	if 'file' in metadata:
		for file in metadata['file']:
			if 'subgroups' in file and file['subgroups']:
				file_subgroups += file['subgroups']
			if 'groups' in file and file['groups']:
				file_groups += file['groups']

	groups = []
	if 'eusInfo' in metadata and 'groups' in metadata['eusInfo']:
		groups = metadata['eusInfo']['groups']
	# May not make sense here.
	#if len(groups+file_groups) < 1:
	#	raise Exception('You must specify at least one group.')

	proposals = []
	for g in file_groups:
		if not g:
			continue
		if 'type' in g and 'name' in g and g['type'] == 'proposal':
			proposals.append(g['name'])

	if proposal:
		proposals.append(proposal)

	for prop in proposals:
		perm = myemsl.getpermission.get_permission_bool(int(username), 'proposal', 'p', config)
		if not perm:
			perm = myemsl.getpermission.get_permission_upload(prop, int(username), config)
		if not perm:
			raise Exception('You(%s) do not have upload permissions to proposal %s.\n'%(str(username), prop))


	def validate_group(group):
		if not ('name' in group and group['name'] != None):
			raise Exception('Group specified but no group name')
		if not ('type' in group and group['type']):
			raise Exception('Group specified but no group type')

	for group in groups + file_groups:
		if not group:
			continue
		validate_group(group)
		p_perm = myemsl.getpermission.get_permission_bool(int(username), group['type'], 'p', config=config)
		if p_perm:
			insert_group(group['name'], group['type'])
		else:
			raise Exception('You(%s) do not have permissions to add a group of type %s.\n'%(str(username), group['type']))

	for subgroup in subgroups + file_subgroups:
		pgrp = subgroup[0]
		cgrp = subgroup[1]
		validate_group(pgrp)
		validate_group(cgrp)
		p_perm = myemsl.getpermission.get_permission_bool(int(username), pgrp['type'], 'p', config=config)
		c_perm = myemsl.getpermission.get_permission_bool(int(username), cgrp['type'], 'p', config=config)
		if not p_perm or not c_perm:
			raise Exception('You(%s) do not have permissions to subgroup %s to %s.'%(str(username),cgrp['type'], pgrp['type']))
		if pgrp['type'] == 'proposal':
			pgid = get_proposal_gid(pgrp['name'])
		else:
			pgid = get_group_id(pgrp['name'], pgrp['type'])
		if cgrp['type'] == 'proposal':
			cgid = get_proposal_gid(cgrp['name'])
		else:
			cgid = get_group_id(cgrp['name'], cgrp['type'])
		if not child_group_of_parent_check_by_id(cgid, pgid):
			insert_subgroup(cgid, pgid)

	update_transaction_stime(transaction)
#FIXME make this prefix configurable?
	prefix = "/srv/myemsl-ingest/"
	sql = ''
	# we'll just have to do this manually for sql injection checking
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
	cursor = cnx.cursor()
	try:
		metadata_merged = {}
		for file in metadata["file"]:
			i = file["destinationDirectory"] + "/" + file["fileName"]
			if not i in metadata_merged:
				metadata_merged[i] = {}
			metadata_merged[i]['sha1Hash'] = file["sha1Hash"]
			if "groups" in file:
				metadata_merged[i]['groups'] = file['groups']
		itemlogfile = open(itemlogfilename, 'w')
		for file,size in files:
			subdir = file.rsplit('/', 1)
			if len(subdir) < 2:
				name = subdir[0]
				subdir = ''
			else:
				name = subdir[1]
				subdir = subdir[0]
			hashsum = None
			try:
				hashsum = metadata_merged[subdir + '/' + name]['sha1Hash']
			except:
				pass
			file_groups = []
			try:
				file_groups = metadata_merged[subdir + '/' + name]['groups']
			except:
				pass
			pgroup = []
			if proposal:
				pgroup.append({'name':proposal, 'type':'proposal'})
			item_id = insert_file(transaction, subdir, name, size, hashsum, groups+file_groups+pgroup, cursor)
			(d, f, ff) = id2dirandfilename(item_id)
			final_fulldir = "%s/bundle/%s" %(prefix, d)
			myemsl.util.try_mkdir(final_fulldir)
			final_fullfile = "%s/%s" %(final_fulldir, f)
			old_fullfile = "%s/%s/bundle/%s/%s/%s" %(prefix, username, transaction, subdir, name)
			os.rename(old_fullfile, final_fullfile)
			itemlogfile.write("%s %s/%s" %(item_id, subdir, name)
		itemlogfile.close()
		bundledir = "%s/%s/bundle/" %(prefix, username)
		for (root, dirs, files) in os.walk(bundledir, topdown=False):
			for d in dirs:
				os.rmdir("%s/%s" %(root, d))
		cnx.commit()
	except Exception, e:
		cnx.rollback()
		cnx.close()
		raise Exception('Unable to insert file metadata (%s).'%(str(e)))
	cnx.close()

def get_transaction(user):
	transxml = call_curl(
		"%s/%s" %(config.get('metadata', 'transaction_base_url'), user), 
		capath=None,
		cainfo='/etc/myemsl/keys/server/local.crt',
		sslcert='/etc/myemsl/keys/server/local.pem',
		sslcerttype='PEM',
		insecure=config.get('webservice', 'ssl_verify_peer') != 'False'
	)
	dom = xml.dom.minidom.parseString(transxml)
	transaction = -1
	found = False
	for x in dom.firstChild.childNodes:
		if x.nodeType == x.ELEMENT_NODE and (x.nodeName == 'transaction'):
			transaction = int(x.getAttribute('id'))
			found = True
			break
	if not found:
		raise Exception("Could not get transaction number from server")
	return transaction


