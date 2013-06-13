#!/usr/bin/python

import rfc3339
import simplejson as json

import os
import sys
import gdbm
import errno
import urllib
import tempfile
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

import myemsl.id2filename
import myemsl.elasticsearch.metadata
import myemsl.elasticsearch.metadata.emsl_base
import myemsl.elasticsearch.metadata.emsl_dms

from myemsl.elasticsearch.jsonentry import *

logger = getLogger(__name__)

def cursoriter(cursor):
	while True:
		val = cursor.fetchone()
		if val:
			yield val
		else:
			return

class fs_cached_metadata_callback_plugin:
	def __init__(self, callback, rebuild=False):
		self.callback = callback
		self.rebuild = rebuild
		self.jsoncache = "/var/lib/myemsl/metadata/jsoncache"
		try:
			self.jsoncache = config.get('metadata', 'jsoncache')
		except:
			pass
		try:
			os.makedirs(self.jsoncache + '/.tmp')
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise
	def __del__(self):
		pass
	def not_cached(self, entry):
		return self.callback(entry)
		#entry.done(True)
		#entry.done(False)
	def always_callback(self, id, entry, strentry, cached, cache_failure):
		if not cached and not cache_failure:
			(f, name) = tempfile.mkstemp(dir=self.jsoncache + '/.tmp')
			f = os.fdopen(f, 'w')
			f.write(strentry)
			f.close()
			newname = prefix + myemsl.id2filename.id2filename(id)
			try:
				os.rename(name, prefix + myemsl.id2filename.id2filename(id))
			except OSError, e:
				if e.errno != errno.ENOENT:
					raise
				else:
					dirname = newname[:newname.rindex('/')]
					try:
						os.makedirs(dirname)
					except OSError, e2:
        					if e2.errno != errno.EEXIST or not os.path.isdir(dirname):
							raise e2
					os.rename(name, prefix + myemsl.id2filename.id2filename(id))
		#print id, cached, cache_failure
	def match(self, id, strentry):
		cached = False
		try:
			file = myemsl.id2filename.open(self.jsoncache, id, 'r+')
			cached = file.read() == strentry
			file.close()
		except IOError, e:
			if e.errno != errno.ENOENT:
				raise
		return cached

class gdbm_cached_metadata_callback_plugin:
	def __init__(self, callback, rebuild=False):
		self.callback = callback
		self.rebuild = rebuild
		self.jsoncache = "/var/lib/myemsl/metadata/jsoncache"
		try:
			self.jsoncache = config.get('metadata', 'jsoncache')
		except:
			pass
		try:
			os.makedirs(self.jsoncache + '/.tmp')
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise
		self.gdb = gdbm.open(self.jsoncache + "/cache.db", "w")
	def __del__(self):
		#self.gdb.reorganize()
		self.gdb.sync()
		self.gdb.close()
	def not_cached(self, entry):
		return self.callback(entry)
		#entry.done(True)
		#entry.done(False)
	def always_callback(self, id, entry, strentry, cached, cache_failure):
		if not cached and not cache_failure:
			self.gdb[str(id)] = strentry
	def match(self, id, strentry):
		cached = False
		try:
			cached = self.gdb[str(id)] == strentry
		except KeyError, e:
			pass
		return cached

def all_metadata_with_cache(callback, rebuild=None):
#FIXME make this modular so that it can be replaced by non file system caches.
	cmcp = gdbm_cached_metadata_callback_plugin(callback, rebuild=rebuild)
	def cache(entry):
		id = entry.entry['_id']
		strentry = json.dumps(entry.entry, sort_keys=True)
		cached = cmcp.match(id, strentry)
		cache_failure = False
		if not cached or rebuild:
#FIXME should be a list.
			entry.done_cb.append(lambda entry, is_ok: cmcp.always_callback(id, entry, strentry, cached, not is_ok))
			cmcp.not_cached(entry)
		else:
			cmcp.always_callback(id, entry.entry, strentry, True, cache_failure)
#FIXME remove
#		callback(wrapper)
	all_metadata_to_json(cache)

def all_metadata_to_json(callback, rebuild=None):
#FIXME don't hard code this like this.
	all_icons =  dict([(i[:-len('.png')], True) for i in os.listdir('/var/www/myemsl/static/1/icons') if i.endswith('.png')])
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
	cursor = cnx.cursor()
	sql = """
select proposal_id, person_id from eus.proposal_members;
"""
	cursor.execute(sql)
	proposal_info = {}
	for row in cursoriter(cursor):
		p = proposal_info.get(row[0])
		if not p:
			p = {"members":[]}
			proposal_info[row[0]] = p
		p['members'].append(row[1])
	sql = """
CREATE OR REPLACE FUNCTION myemsl_group_id_sort (ANYARRAY)
RETURNS ANYARRAY LANGUAGE SQL
AS $$
SELECT ARRAY(SELECT DISTINCT unnest($1) ORDER BY 1)
$$;

CREATE TEMP TABLE "temp_group_sets" (
        "group_set_id" SERIAL PRIMARY KEY,
        "group_temp_key" text,
        "group_set_members" bigint[]
)
WITHOUT OIDS
ON COMMIT DROP;

CREATE TEMP TABLE "temp_group_flattened" (
        "group_id" bigint,
        "group_member" bigint
)
WITHOUT OIDS
ON COMMIT DROP;

CREATE TEMP TABLE "temp_group_set_members" (
        "group_set_id" int,
        "group_member" bigint
)
WITHOUT OIDS
ON COMMIT DROP;

CREATE TEMP TABLE "temp_item_to_group_set" (
        "item_id" bigint PRIMARY KEY,
        "group_set_id" int
)
WITHOUT OIDS
ON COMMIT DROP;

insert into temp_group_sets(group_temp_key, group_set_members)
select distinct group_temp_key, group_set_members from (
select array_to_string(agg, ',') as group_temp_key, agg as group_set_members from (select myemsl_group_id_sort(agg) as agg from (select array_agg(group_id) as agg from myemsl.group_items group by item_id) as g group by agg) as g
) as g;

CREATE INDEX temp_group_sets_group_temp_key_idx ON temp_group_sets USING btree (group_temp_key);

insert into temp_group_flattened(group_member, group_id)
with recursive t(parent_id, child_id) as (
select parent_id, child_id from myemsl.subgroups as s
union
select s.parent_id, t.child_id from myemsl.subgroups as s, t where t.parent_id = s.child_id
) select parent_id, child_id from t where parent_id is not NULL
union select group_id, group_id from myemsl.groups where group_id not in (select child_id from myemsl.subgroups)
union select child_id, child_id from myemsl.subgroups;

insert into temp_group_set_members(group_set_id, group_member)
select tgs.group_set_id, tgf.group_member from (select group_set_id, unnest(group_set_members) as group_id from temp_group_sets) as tgs, temp_group_flattened as tgf where tgs.group_id = tgf.group_id;

drop table temp_group_flattened;

insert into temp_item_to_group_set(item_id, group_set_id)
select item_id, group_set_id from (select item_id, myemsl_group_id_sort(array_agg(group_id)) as agg from myemsl.group_items group by item_id) as g, temp_group_sets as tgs where array_to_string(g.agg, ',') = tgs.group_temp_key;

drop table temp_group_sets;

select group_set_id, g.group_id, type, name, proposal_id from (select group_set_id, group_id, type, name from temp_group_set_members as gsm, myemsl.groups as g where gsm.group_member = g.group_id) as g left join eus.proposals as p on p.group_id = g.group_id;
"""
	cursor.execute(sql)
	group_sets = {}
#FIXME make this list use a config file somehow.
	mdp = myemsl.elasticsearch.metadata.metadata_processor()
	myemsl.elasticsearch.metadata.emsl_base.metadata(mdp)
	myemsl.elasticsearch.metadata.emsl_dms.metadata(mdp)
	print 'MD Loaded'
#FIXME unhardcode this
	extended_metadata_reference = {
		'omics.dms.datapackage_id': {'id':'gov_pnnl_emsl_dms_datapackage', 'type':int},
		'omics.dms.dataset': {'id':'gov_pnnl_emsl_dms_dataset', 'type':lambda x: mdp.emsl_dms_metadata.datasetname2datasetid.get(x)},
	}
	for row in cursoriter(cursor):
		gs = group_sets.get(row[0])
		if not gs:
			gs = {'groups':[], 'proposals':{}, 'extended_metadata':{'gov_pnnl_emsl_proposal':[], 'gov_pnnl_emsl_instrument':[]}}
			group_sets[row[0]] = gs
		if(row[4] != None):
			gs['extended_metadata']['gov_pnnl_emsl_proposal'].append(row[3])
		else:
			if row[2][:len("Instrument.")] == "Instrument.":
				gs['groups'].append([row[1], "Instrument", row[2][len("Instrument."):]])
				gs['extended_metadata']['gov_pnnl_emsl_instrument'].append(row[2][len("Instrument."):])
			elif row[2][:len("gov_pnnl_erica/irn")] == "gov_pnnl_erica/irn":
				gs['extended_metadata']['gov_pnnl_erica/irn'] = json.loads(row[3])
			else:
				gs['groups'].append([row[1], row[2], row[3]])
				e = extended_metadata_reference.get(row[2])
				if e:
					list = gs['extended_metadata'].get(e['id'])
					if not list:
						list = []
						gs['extended_metadata'][e['id']] = list
					list.append(e['type'](row[3]))
	for (gsid, gs) in group_sets.iteritems():
		users = {}
#		extended_metadata = {
#			'gov_pnnl_emsl_proposal': gs['proposals']
			#FIXME 'gov_pnnl_emsl_users': users.keys()}
#		}
#		dpid = gs.get('groups.omics.dms.datapackage_id')
#		if dpid:
#			extended_metadata['gov_pnnl_emsl_dms_datapackage'] = dpid
		extended_metadata = gs['extended_metadata']
		myemsl.elasticsearch.metadata.dedup(extended_metadata)
		dp = extended_metadata.get('gov_pnnl_emsl_dms_datapackage')
		if dp:
			for id in dp[:]:
				print "Processing:", id, dp
				myemsl.elasticsearch.metadata.merge_left(extended_metadata, mdp.emsl_dms_metadata.datapackage.get(id))
		else:
			dp = extended_metadata.get('gov_pnnl_emsl_dms_dataset')
			if dp:
				for id in dp[:]:
					print "Processing:", id, dp
					myemsl.elasticsearch.metadata.merge_left(extended_metadata, mdp.emsl_dms_metadata.dataset.get(id))
					extra_proposals = mdp.emsl_dms_metadata.dataset_proposals.get(id)
					if extra_proposals != None:
						gs['extended_metadata']['gov_pnnl_emsl_proposal'].extend(extra_proposals)
		extended_metadata = mdp.resolv(extended_metadata)
		if len(extended_metadata) > 0:
#FIXME Plugin related stuff...
			for x in ['gov_pnnl_emsl_dms_pi', 'gov_pnnl_emsl_dms_technical_lead', 'gov_pnnl_emsl_dms_proj_mgr', 'gov_pnnl_emsl_dms_researcher', 'gov_pnnl_emsl_dms_dataset_operator']:
				list = extended_metadata.get(x)
				if list:
					for i in list:
						users[i['id']] = 1
			gs['extended_metadata'] = extended_metadata
		else:
			del gs['extended_metadata']
		proposals = [i['id'] for i in gs['extended_metadata']['gov_pnnl_emsl_proposal']]
#		dedup_proposals = {}
		for proposal in proposals:
#			dedup_proposals[proposal] = 1
			pi = proposal_info.get(proposal)
			if pi:
				for member in pi['members']:
					users[member] = 1
#FIXME
		gs['proposals'] = proposals
		gs['users'] = users.keys()
		print gs
	sql = """
select instrument_id, name_short from eus.instruments;
"""
	cursor.execute(sql)
	instruments = {}
	for row in cursoriter(cursor):
		instruments[row[0]] = row[1]
#FIXME remove
	import time
	count = 0
	print time.time()
	sql = """
	select name, submitter, eus.users.first_name, eus.users.last_name, EXTRACT(EPOCH FROM stime), subdir, size, myemsl.files.item_id, aged, group_set_id from myemsl.files, myemsl.transactions, eus.users, temp_item_to_group_set where myemsl.transactions.transaction = myemsl.files.transaction and eus.users.person_id = myemsl.transactions.submitter and temp_item_to_group_set.item_id = myemsl.files.item_id and (name != 'metadata.txt' or subdir != '');
	"""
	cursor.execute(sql)
	for row in cursoriter(cursor):
#FIXME
		if count == 0:
			print time.time(), count
		group_set_id = row[0]
		if count % 1000 == 0:
			print time.time(), count
		count += 1
#remove till here
		if row[4] == None:
			print "Id %s bad stime." %(row[7])
			continue
		entry = {}
		item_id = row[7]
		entry['filename'] = row[0]
		idx = row[0].rfind('.')
		entry['ico'] = 'file'
		if idx != -1:
			entry['ext'] = row[0][idx + 1:]
			newicon = all_icons.get(entry['ext'])
			if newicon:
				entry['ico'] = entry['ext']
		entry['subdir'] = row[5]
		entry['size'] = row[6]
		first = row[2]
		if not first:
			first = ''
		last = row[3]
		if not last:
			last = ''
		if first != '' and last != '':
			entry['submittername'] = "%s %s" %(first, last)
		entry['first'] = first
		entry['last'] = last
		entry['submitterid'] = row[1]
		aged = "false"
#FIXME make this a bool in elasticsearch later
		if row[8]:
			aged = "true"
		entry['aged'] = aged
		users = {row[1]:1}
		groups = {}
		proposals = []
		gs = group_sets.get(row[9])
		if gs:
			for g in gs['groups']:
				groups[g[1]] = g[2]
			proposals = gs['proposals']
			for user in gs['users']:
				users[user] = 1
			emd = gs.get('extended_metadata')
			if emd and len(emd) > 0:
				entry['extended_metadata'] = emd
		ds = groups.get('omics.dms.dataset')
		if ds:
			#FIXME generalize this. extended_metadata on metadata specific file entries need to be compied so modifications don't affect others.
			entry['extended_metadata'] = entry['extended_metadata'].copy()
			tsubdir = entry['subdir']
			if tsubdir.startswith(ds + '/'):
				tsubdir = tsubdir[len(ds) + 1:]
			dsid = mdp.emsl_dms_metadata.datasetname2datasetid.get(ds)
			if dsid:
				ajid = mdp.emsl_dms_metadata.datasetid_subdir2analysisjobid(mdp.emsl_dms_metadata.datasetname2datasetid[ds], tsubdir)
				if ajid == None:
					aj = {'tool': {'name':'Raw'}}
				else:
					aj = mdp.emsl_dms_metadata.analysisjob[ajid]
				entry['extended_metadata']['gov_pnnl_emsl_dms_analysisjob'] = [aj]
		if len(proposals) > 0:
			entry['proposals'] = proposals
		if len(groups) > 0:
			for k, v in groups.iteritems():
#FIXME escape
				entry["groups.%s" %(k)] = v
				if k == 'Instrument' and v.isdigit():
					tv = instruments.get(int(v))
					if tv:
						entry["instrumentname"] = tv
		entry['users'] = users.keys()
		entry['stime'] = rfc3339.rfc3339(row[4])
		entry['_id'] = item_id
		callback(jsonentry(entry))
	return 0

def proposal_info_to_json(callback, rebuild=None):
	sql = """
	select proposal_id, accepted_date, title from eus.proposals;
	"""
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
	cursor = cnx.cursor()
	cursor.execute(sql)
	for row in cursoriter(cursor):
		if row[1] == None:
			print "Id %s bad atime." %(row[0])
			continue
		entry = {}
		proposal_id = row[0]
		entry['title'] = row[2]
		entry['accepted_date'] = row[1]
		sql = """
select pm.person_id, u.network_id, u.first_name, u.last_name, u.email_address from eus.proposal_members as pm, eus.users as u where pm.proposal_id=%(proposal_id)s and pm.person_id = u.person_id;
		"""
		cursor2 = cnx.cursor()
		cursor2.execute(sql, {"proposal_id":proposal_id})
		person_ids = []
		network_ids = []
		person_names = []
		email_addresses = []
		for row2 in cursoriter(cursor2):
			person_id = row2[0]
			network_id = row2[1]
			first_name = row2[2]
			last_name = row2[3]
			email_address = row2[4]
			if person_id:
				person_ids.append(person_id)
			if network_id:
				network_ids.append(network_id)
			if first_name or last_name:
				if first_name and last_name:
					person_names.append("%s %s" %(first_name, last_name))
				elif last_name:
					person_names.append(last_name)
				else:
					person_names.append(first_name)
			if email_address:
				email_addresses.append(email_address)
		entry['person_ids'] = person_ids
		entry['network_ids'] = network_ids
		entry['person_names'] = person_names
		entry['email_addresses'] = email_addresses
		sql = """
select i.instrument_name, i.name_short, i.eus_display_name from eus.instruments as i, eus.proposal_instruments as pi where pi.instrument_id = i.instrument_id and pi.proposal_id=%(proposal_id)s group by i.instrument_name, i.name_short, i.eus_display_name;
		"""
		cursor2 = cnx.cursor()
		cursor2.execute(sql, {"proposal_id":proposal_id})
		instrument_names = []
		instrument_short_names = []
		for row2 in cursoriter(cursor2):
			i = []
			if row2[0]:
				i.append(row2[0])
			if row2[1]:
				i.append(row2[1])
				instrument_short_names.append(row2[1])
			if row2[2]:
				i.append(row2[2])
			if len(i) > 0:
				instrument_names.extend(i)
		if len(instrument_short_names) > 0:
			entry['instrument_names'] = instrument_short_names
		if len(instrument_names) > 0:
			entry['instrument_text'] = ' '.join(instrument_names)
		entry['_id'] = proposal_id
		callback(jsonentry(entry))
	return 0

def local_predicates_to_json(callback, rebuild=None):
	sql = """
	select lp.id, lp.desc, lp.person_id, u.first_name, u.last_name from myemsl.local_predicate as lp, eus.users as u where lp.person_id = u.person_id;
	"""
#FIXME version
	cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
	cursor = cnx.cursor()
	cursor.execute(sql)
	for row in cursoriter(cursor):
		if row[1] == None:
			print "Id %s bad atime." %(row[0])
			continue
		entry = json.loads(row[1])
		entry['_id'] = row[0]
		entry['submitter'] = {'name': row[3] + " " + row[4], 'id':row[2]}
		callback(jsonentry(entry))
	return 0

def erica_released_publications_json(callback, rebuild=None):
	j = json.load(open('/var/lib/myemsl/erica.json'))
	for entry in j['publications']:
		entry['_id'] = entry['id']
		del entry['id']
		if entry['completed'] == True and entry['publication_info']['limited_distribution'] == False:
			callback(jsonentry(entry))
	return 0

if __name__ == '__main__':
	sys.exit(all_metadata_to_json(lambda x: sys.stdout.write(str(x.entry) + "\n")))

