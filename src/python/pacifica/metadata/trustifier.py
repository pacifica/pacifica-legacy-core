#!/usr/bin/python

import sys
import simplejson as json
from pymongo import Connection as mongoconnection

def checkperm(perms, perm, value, transaction, submitter):
	tocheck = perm
	if perm == 'gov_pnnl_emsl_my/instrument':
		tocheck = "Instrument.%s" %(value)
	elif perm == 'gov_pnnl_emsl_my/proposal':
		tocheck = "proposal"
	elif perm == 'gov_pnnl_emsl_my/dms/dataset':
		tocheck = "omics.dms.dataset_id"
	if tocheck in perms:
		if submitter in perms[tocheck]:
			return True
	return False

def process_item(instanceuuid, perms, item_id, collection, cb):
	f = collection.find({"_id":item_id})
	for doc in f:
		transactions = [int(t) for t in doc['trans'].keys()]
		transactions.sort()
		doc['trusts'] = {instanceuuid:{}}
		for t in transactions:
			submitter = doc['trans'][str(t)]['s']
			trusted = []
			doc['trusts'][instanceuuid][str(t)] = trusted
			for i in doc['trans'][str(t)]['v']:
				a = doc['vals'][str(i)]
				if a[0] in ['gov_pnnl_emsl_my/instrument', 'gov_pnnl_emsl_my/proposal', 'gov_pnnl_emsl_my/dms/dataset']:
					all_pass = True
					if isinstance(a[1], (list, tuple)):
						for testval in a[1]:
							if submitter == 70000: #DMS
								continue #Trust DMS specified values always.
							tst = checkperm(perms, a[0], testval, t, submitter)
							if tst == False:
								all_pass = False
								break
					else:
						all_pass = checkperm(perms, a[0], a[1], t, submitter)
					if all_pass:
						trusted.append([int(i), 1])
					else:
						trusted.append([int(i), -1])
	#Just trust filenames for now.
	#Always trust keywords.
				elif a[0] in ['gov_pnnl_emsl_pacifica/subdir', 'gov_pnnl_emsl_pacifica/filename', 'gov_pnnl_emsl_pacifica/keyword']:
					trusted.append([int(i), 1])
				else:
	#Dummy trust, everything else is unknown.
					trusted.append([int(i), 0])
		cb(doc)
		break;

def main():
#FIXME
	client = mongoconnection('m11.emsl.pnl.gov', 27017)
	collection = client['pacifica_db']['rmds_collection']
	perms = json.load(open('/var/lib/myemsl/myemsl.dumppg.json'))
	instanceuuid = 'instanceuuid'

	id = int(sys.argv[1])
	def cb(doc):
		print json.dumps(doc, indent=4)
	process_item(instanceuuid, perms, id, collection, cb)

if __name__ == '__main__':
	main()
