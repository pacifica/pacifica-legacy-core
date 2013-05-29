from pymongo import Connection

def collection_name_get(db, chanel, version=None):
	if version == None:
		version = db['notification_versions'].find({'_id':chanel}).next()['value']
	return "%s_notify_%s" %(chanel, int(version))

def notification_version_get(host, port, db, chanel):
	client = Connection(host, port)
	db = client[db]
	scollection = db['notification_versions']
	doc = scollection.find({'_id':chanel}).next()
	version = doc['value']
	return int(version)
