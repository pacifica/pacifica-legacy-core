#!/usr/bin/python

import sys
import hashlib
import threading
import simplejson as json

#Helper functions
def merge(data, data2):
	retval = {}
	for (k, v) in data.iteritems():
		if data2.get(k):
			retval[k] = v + data2[k]
			del data2[k]
		else:
			retval[k] = v
	for (k, v) in data2.iteritems():
		retval[k] = v
	return retval
def merge_left(data, data2):
	if data2 == None:
		return data
	for (k, v) in data2.iteritems():
		t = data.get(k)
		if t:
			t.extend(v)
		else:
			data[k] = v[:]
	return data
def entry_copy(data):
	return data
def entry_to_id(data):
	return {'id': data}
def set_if_exist(d, key, value):
	if value:
		d[key] = value
	return d
def gen_empty_id_if_none(table):
	def closed(id):
		res = table.get(id)
		if res:
			return res
		return {'id': id}
	return closed
def dedup(data):
	for (k, v) in data.iteritems():
		data[k] = dict([(i, 1) for i in v]).keys() #deduplicate

class metadata_processor:
	def __init__(self):
		self.jointable = {}
		self.lock = threading.Lock()
	def reinit(self):
		self.jointable = {}
#FIXME should need to register these things so we can easily clear them.
		self.emsl_basic_metadata = None
		self.emsl_dms_metadata = None
	def register_join(self, key, resolver):
		self.jointable[key] = resolver
	def resolv(self, data):
		retval = {}
		for (k, v) in data.iteritems():
			tv = dict([(i, 1) for i in v]).keys() #deduplicate
			v = tv
			j = self.jointable[k]
			if isinstance(j, dict):
				retval[k] = [j.get(i) for i in v]
			else:
				retval[k] = [j(i) for i in v]
		return retval

def main():
	mdp = metadata_processor()
	sys.exit(-1)

if __name__ == '__main__':
	#import profile
	#profile.run('main()')
	main()
