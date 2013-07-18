#!/usr/bin/python

import sys
import simplejson as json
from pymongo import Connection as mongoconnection
from myemsl.getconfig import getconfig_notification
import myemsl.elasticsearch.metadata
import myemsl.elasticsearch.metadata.emsl_base
import myemsl.elasticsearch.metadata.emsl_dms

#FIXME this was copied from jsondumper. share and make more generic
def join(extended_metadata, mdp):
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
					extended_metadata['gov_pnnl_emsl_proposal'].extend(extra_proposals)
	extended_metadata = mdp.resolv(extended_metadata)
	return extended_metadata

def process_item(item_id, collection, cb, mdp, joinable):
	f = collection.find({"_id":item_id})
	extended_metadata = None
	for doc in f:
		for key in joinable.keys():
			entry = doc['trusted'].get(key)
			if entry != None:
				if extended_metadata == None:
					extended_metadata = {}
				extended_metadata[joinable[key]] = entry
				print "joinable entry found: %s" %(key)
		if extended_metadata != None:
			extended_metadata = join(extended_metadata, mdp)
			doc['extended_metadata'] = extended_metadata
		cb(doc)
		break;

def main():
#FIXME Special for metadata?
	config = getconfig_notification('fmds')
	client = mongoconnection(config.notification.hostname, config.notification.port)
	collection = client['pacifica_db']['fmds_collection']
	id = int(sys.argv[1])
	def cb(doc):
		print json.dumps(doc, indent=4)
#FIXME copied from jsondumper. Also need to be able to refresh this somehow...
#FIXME make this list use a config file somehow.
	mdp = myemsl.elasticsearch.metadata.metadata_processor()
	myemsl.elasticsearch.metadata.emsl_base.metadata(mdp)
	myemsl.elasticsearch.metadata.emsl_dms.metadata(mdp)
	print 'MD Loaded'
#FIXME make this a property
	print mdp.jointable.keys()
#FIXME For now map back to the older names for these things until migration is compete.
	joinable = {
		'gov_pnnl_emsl_my/instrument': 'gov_pnnl_emsl_instrument',
		'gov_pnnl_emsl_my/proposal': 'gov_pnnl_emsl_proposal',
		'gov_pnnl_emsl_my/dms/datapackage': 'gov_pnnl_emsl_dms_datapackage',
		'gov_pnnl_emsl_my/dms/dataset': 'gov_pnnl_emsl_dms_dataset'
	}

	process_item(id, collection, cb, mdp, joinable)

if __name__ == '__main__':
	main()

