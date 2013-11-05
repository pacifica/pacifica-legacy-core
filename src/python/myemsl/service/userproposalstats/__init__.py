#!/usr/bin/python
from bson.code import Code
import datetime
import pymongo
import simplejson as json
from myemsl.callcurl import call_curl
from myemsl.dbconnect import myemsldb_connect
import sys
from myemsl.getconfig import getconfig
config = getconfig()

chunk_size = 100

#FIXME share this code.
def cursoriter(cursor):
	while True:
		val = cursor.fetchone()
		if val:
			yield val
		else:
			return

def log_items_to_person_proposals(start, end, found_cb):
	single_map_cb = Code("""
	function() {
		emit(this.i, {pid: [this.p]});
	}
	""")

	single_reduce_cb = Code("""
	function(item, vals) {
		var res = {pid:[]};
		for(var v in vals) {
			var value = vals[v];
			if(value.pid !== undefined) {
				for(var j in value.pid) {
					res.pid.push(value.pid[j]);
				}
			}
		}
		return res;
	}
	""")

	date_query = {'d': {"$gte": start, "$lt": end}, 'p': {'$exists': True}}
	db_host = config.get('download_log', 'server')
	db_port = config.getint('download_log', 'port')
	connection = pymongo.Connection(db_host, db_port)
	db = connection[config.get('download_log', 'db_name')]

	db_name_single_items = config.get('download_log', 'single_collection')
	db_name_cart_items = config.get('download_log', 'cart_collection')
	db_name_uniq_cart_items = config.get('download_log', 'uniq_cart_collection')
	db_name_uniq_items = config.get('download_log', 'uniq_single_collection')
	db_name_user2proposals = config.get('download_log', 'user2proposals_collection')
	
	cart_map_cb = Code("""
	function() {
		emit(this.c, {pid: [this.p]});
	}
	""")

	cart_reduce_cb = Code("""
	function(item, vals) {
		var res = {pid:[]};
		for(var v in vals) {
			var value = vals[v];
			if(value.pid !== undefined) {
				for(var j in value.pid) {
					res.pid.push(value.pid[j]);
				}
			}
		}
		return res;
	}
	""")

	db[db_name_cart_items].ensure_index([('d', pymongo.ASCENDING)])
	db[db_name_cart_items].map_reduce(cart_map_cb, cart_reduce_cb, out={'replace': db_name_uniq_cart_items}, query=date_query);
	def cart_process(chunk_items, collection):
		sql = "SELECT cart_id, item_id FROM myemsl.cart_items WHERE cart_id in (%s) ORDER by cart_id;" %(','.join([str(i) for i in chunk_items]))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
		cursor = cnx.cursor()
		cursor.execute(sql)
		old_cart_id = None
		cart_list = {}
		for row in cursoriter(cursor):
			toset = cart_list.setdefault(row[0], [])
			toset.insert(0, row[1])
		for key in cart_list.iterkeys():
			collection.update({'_id': key}, {"$set": {'value.i': cart_list[key]}}, w=1)

	chunk_items = []
	collection = db[db_name_uniq_cart_items]
	for item in db[db_name_uniq_cart_items].find(fields={'_id':1}):
		chunk_items.insert(0, int(item['_id']))
		if len(chunk_items) >= chunk_size:
			cart_process(chunk_items, collection)
			chunk_items = []
	if len(chunk_items) > 0:
		cart_process(chunk_items, collection)


	db[db_name_single_items].ensure_index([('d', pymongo.ASCENDING)])
	db[db_name_single_items].map_reduce(single_map_cb, single_reduce_cb, out={'replace': db_name_uniq_items}, query=date_query);

	map2_cb = Code("""
	function() {
		for(var i in this.value.i) {
			emit(this.value.i[i], {pid: this.value.pid});
		}
	}
	""")

	reduce2_cb = Code("""
	function(item, vals) {
		var res = {p:[], pid:[]};
		for(var v in vals) {
			var value = vals[v];
			if(value.p !== undefined) {
				for(var j in value.p) {
					res.p.push(value.p[j]);
				}
			}
			if(value.pid !== undefined) {
				for(var j in value.pid) {
					res.pid.push(value.pid[j]);
				}
			}
		}
		return res;
	}
	""")
	db[db_name_uniq_cart_items].map_reduce(map2_cb, reduce2_cb, out={'reduce': db_name_uniq_items});

	def proposals_process(chunk_items, collection):
		query = {
			"fields": [
				"proposals"
			],
			"query": {
				"constant_score": {
					"filter": {
						"ids": {
							"values": chunk_items
						}
					}
				}
			}
		}
		server = config.get('elasticsearch', 'server')
		results = json.loads(call_curl("%s/myemsl_current_simple_items/simple_items/_search" %(server), method='POST', idata=json.dumps(query)))
		if results['hits']['total'] != len(chunk_items):
			raise Exception('Failed to find some items')
		for hit in results['hits']['hits']:
			if 'fields' in hit and 'proposals' in hit['fields']:
				collection.update({'_id': int(hit['_id'])}, {"$set": {'value.p': hit['fields']['proposals']}}, w=1)

	chunk_items = []
	collection = db[db_name_uniq_items]
	for item in db[db_name_uniq_items].find(fields={'_id':1}):
		chunk_items.insert(0, int(item['_id']))
		if len(chunk_items) >= chunk_size:
			proposals_process(chunk_items, collection)
			chunk_items = []
	if len(chunk_items) > 0:
		proposals_process(chunk_items, collection)

	map3_cb = Code("""
	function() {
		for(var i in this.value.pid) {
			var pid = this.value.pid[i];
			emit(pid, {p: this.value.p});
		}
	}
	""")

	reduce3_cb = Code("""
	function(item, vals) {
		var tp = {}
		var res = {p:[]};
		for(var v in vals) {
			var value = vals[v];
			for(var j in value.p) {
				tp[value.p[j]] = 1;
			}
		}
		for(var p in tp) {
			res.p.push(p);
		}
		return res;
	}
	""")
	db[db_name_uniq_items].map_reduce(map3_cb, reduce3_cb, out={'replace': db_name_user2proposals});

	for item in db[db_name_user2proposals].find():
		if item['value']['p'] != None:
			found_cb(int(item['_id']), item['value']['p'])

def main():
	start = datetime.datetime(2013, 12, 14)
	end = datetime.datetime(2013, 12, 24)
	log_items_to_person_proposals(start, end, print_cb)

if __name__ == '__main__':
	main()
