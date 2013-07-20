#!/usr/bin/python

import sys
import simplejson as json
from pymongo import Connection as mongoconnection

def process_item(instanceuuid, item_id, collection, cb):
	trusted = {}
	unknown = {}
	f = collection.find({"_id":item_id})
	for doc in f:
		strans = None
		submitter = None
		while True:
			newdoc = {
				'_id': doc['_id'],
				'sz': doc['sz'],
				'pver': doc['ver']
			}
#			print json.dumps(doc, indent=4)
			for (transaction, row) in doc['trans'].iteritems():
				if strans == None or transaction < strans:
					strans = transaction
					submitter = row['s']
			newdoc['submitter'] = submitter
			for (transaction, rows) in doc['trusts']['instanceuuid'].iteritems():
				for row in rows:
					item = doc['vals'][str(row[0])]
					if row[1] >= 1:
						trusted[item[0]] = item[1]
					elif row[1] > -1:
						unknown[item[0]] = item[1]
			if len(trusted) > 0:
				newdoc['trusted'] = trusted
			if len(unknown) > 0:
				newdoc['unknown'] = unknown
			cb(newdoc)
			break;

def main():
#FIXME
	client = mongoconnection('m11.emsl.pnl.gov', 27017)
	collection = client['pacifica_db']['tmds_collection']
	instanceuuid = 'instanceuuid'

	id = int(sys.argv[1])
	def cb(doc):
		print json.dumps(doc, indent=4)
	process_item(instanceuuid, id, collection, cb)

if __name__ == '__main__':
	main()
