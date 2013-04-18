#!/usr/bin/python

import myemsl.prefixtree
import myemsl.elasticsearch.metadata
import simplejson as json
from myemsl.elasticsearch.metadata import merge, merge_left, set_if_exist, gen_empty_id_if_none

class metadata:
	def __init__(self, mdp):
		doc = json.load(open('/var/lib/myemsl/dms.json', 'r'))
		
		dms_instrument = {None: None}
		dms_instrument_full = {None: None}
		mdp.register_join('gov_pnnl_emsl_dms_instrument', dms_instrument)
		table = 'instrument'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			i = {
				'id': row[idx['instrument_id']],
				'name': row[idx['instrument_name']],
			}
			id = row[idx['instrument_id']]
			dms_instrument[id] = i
			i2 = {
				'gov_pnnl_emsl_dms_instrument': [id]
			}
			if row[idx['eus_instrument_id']]:
				i2['gov_pnnl_emsl_instrument'] = [row[idx['eus_instrument_id']]]
			dms_instrument_full[id] = i2

		campaign = {}
		campaign_full = {}
		mdp.register_join('gov_pnnl_emsl_dms_campaign', campaign)
		for v in ['gov_pnnl_emsl_dms_pi', 'gov_pnnl_emsl_dms_technical_lead', 'gov_pnnl_emsl_dms_proj_mgr']:
			mdp.register_join(v, mdp.emsl_basic_metadata.pid2info)

		table = 'campaign'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			c = {
				'id': row[idx['campaign_id']],
				'name': row[idx['name']],
			}
			id = row[idx['campaign_id']]
			campaign[id] = c
			c2 = {
				'gov_pnnl_emsl_dms_campaign': [id]
			}
			for (k, v) in [('pi', 'gov_pnnl_emsl_dms_pi'), ('technical_lead', 'gov_pnnl_emsl_dms_technical_lead'), ('proj_mgr', 'gov_pnnl_emsl_dms_proj_mgr')]:
				t = row[idx[k]]
				if t:
					c2[v] = [t]
			campaign_full[id] = c2

		organism = {}
		organism_full = {}
		table = 'organism'
		mdp.register_join('gov_pnnl_emsl_dms_organism', organism)
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			o = {
				'id': row[idx['organism_id']],
				'name': row[idx['name']],
				'short_name': row[idx['short_name']],
			}
			for x in ['domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']:
				t = row[idx[x]]
				if t != None and t != 'na':
					o[x] = t
			id = row[idx['organism_id']]
			organism[id] = o
			organism_full[id] = {'gov_pnnl_emsl_dms_organism': [id]}

		experiment = {}
		experiment_full = {}
		mdp.register_join('gov_pnnl_emsl_dms_experiment', experiment)
		mdp.register_join('gov_pnnl_emsl_dms_researcher', mdp.emsl_basic_metadata.pid2info)
		table = 'experiment'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			e = {
				'name': row[idx['name']],
				'id': row[idx['exp_id']]
			}
			set_if_exist(e, 'reason', row[idx['reason']])
			set_if_exist(e, 'comment', row[idx['comment']])
			id = row[idx['exp_id']]
			experiment[id] = e
			e2 = {
				'gov_pnnl_emsl_dms_experiment': [id]
			}
			t = row[idx['researcher']]
			if t:
				e2['gov_pnnl_emsl_dms_researcher'] = [t]
			t = row[idx['organism_id']]
			if t:
				e2['gov_pnnl_emsl_dms_organism'] = [t]
			t = row[idx['campaign_id']]
			if t:
				e2 = merge(e2, campaign_full[t])
			experiment_full[id] = e2

		dataset = {}
		dataset_full = {}
		datasetname2datasetid = {}
		mdp.register_join('gov_pnnl_emsl_dms_dataset', dataset)
		mdp.register_join('gov_pnnl_emsl_dms_dataset_operator', mdp.emsl_basic_metadata.pid2info)
		table = 'dataset'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			id = row[idx['dataset_id']]
			d = {
				'id': id,
				'name': row[idx['name']]
			}
			datasetname2datasetid[row[idx['name']]] = id
			set_if_exist(d, 'comment', row[idx['dataset_comment']])
			dataset[id] = d
			d2 = {
				'gov_pnnl_emsl_dms_dataset': [id] #,
				#'gov_pnnl_emsl_dms_instrument': [row[idx['instrument_id']]]
			}
			t = row[idx['dataset_operator']]
			if t:
				d2['gov_pnnl_emsl_dms_dataset_operator'] = [t]
			t = row[idx['exp_id']]
			if t:
				d2 = merge(d2, experiment_full[t])
			t = row[idx['instrument_id']]
			if t:
				d2 = merge(d2, dms_instrument_full[t])
			dataset_full[id] = d2
		self.datasetname2datasetid = datasetname2datasetid

		datapackage_proposals = {}
		table = 'datapackage_proposal'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			id = row[idx['datapackage_id']]
			pid = row[idx['proposal_id']]
			if not pid:
				continue
			d = datapackage_proposals.get(id)
			if not d:
				d = []
				datapackage_proposals[id] = d
			d.append(pid)

		datapackage2dataset = {}
		dataset2datapackage = {}
		dataset_proposals = {}
		table = 'datapackage_dataset'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			dpid = row[idx['datapackage_id']]
			dsid = row[idx['dataset_id']]
			t = datapackage2dataset.get(dpid)
			if not t:
				t = []
				datapackage2dataset[dpid] = t
			datapackage2dataset[dpid].append(dsid)
			t = dataset2datapackage.get(dsid)
			if not t:
				t = []
				dataset2datapackage[dsid] = t
			dataset2datapackage[dsid].append(dpid)
			props = datapackage_proposals.get(dpid)
			if props:
				t = dataset_proposals.get(dsid)
				if not t:
					t = {}
					dataset_proposals[dsid] = t
				for prop in props:
					t[prop] = 1

		for (k, v) in dataset_proposals.iteritems():
			dataset_proposals[k] = v.keys()

		datapackage = {}
		datapackage_full = {}
		mdp.register_join('gov_pnnl_emsl_dms_datapackage', gen_empty_id_if_none(datapackage))
		table = 'datapackage'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			id = row[idx['datapackage_id']]
			d = {
				'id': id,
				'name': row[idx['datapackage_name']]
			}
			datapackage[id] = d
			d2 = {
				'gov_pnnl_emsl_dms_datapackage': [id]
			}
		#	t = datapackage_proposals.get(id)
		#	if t:
		#		df['proposals'] = t
			dsets = datapackage2dataset.get(id)
			if dsets:
				for t in dsets:
					merge_left(d2, dataset_full[t])
			proposals = datapackage_proposals.get(id)
			if proposals:
				d2['gov_pnnl_emsl_proposal'] = proposals
			datapackage_full[id] = d2
		#	print json.dumps(mdp.resolv(d2)) #, indent=2)

		analysistool = {}
		table = 'analysistool'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			id = row[idx['id']]
			name = row[idx['name']]
			analysistool[id] = {
				'id': id,
				'name': name
			}

		analysisjob = {None: None}
		dataset2analysisjobid = {}
		table = 'analysisjob'
		idx = dict([(i[1], i[0]) for i in enumerate(doc['dms'][table]['cols'])])
		for row in doc['dms'][table]['ensurerows']:
			id = row[idx['analysisjob_id']]
			dsid = row[idx['dataset_id']]
			results_dir = row[idx['results_dir']]
			if results_dir:
				nrow = dataset2analysisjobid.get(dsid)
				if not nrow:
					nrow = []
					dataset2analysisjobid[dsid] = nrow
				nrow.append([results_dir, id])
			analysisjob[id] = {
				'id': id,
				'name': row[idx['results_dir']],
				'tool': analysistool[row[idx['analysisjob_tool_id']]]
			}
		for (k, v) in dataset2analysisjobid.iteritems():
			tree = myemsl.prefixtree.prefix_tree_make_dict(dict(v))
			dataset2analysisjobid[k] = tree
#FIXME remove
		self.dataset = dataset_full
		self.datapackage = datapackage_full
		self.dataset_proposals = dataset_proposals
		self.analysisjob = analysisjob
		def datasetid_subdir2analysisjobid(dsid, subdir):
			tree = dataset2analysisjobid.get(dsid)
			if not tree:
				return None
			entry = myemsl.prefixtree.prefix_tree_find_dir(subdir, tree)
			if not entry:
				return None
			return entry[1]
		self.datasetid_subdir2analysisjobid = datasetid_subdir2analysisjobid
		mdp.emsl_dms_metadata = self

