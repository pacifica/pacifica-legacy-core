import os
import errno
import struct
from pymongo import Connection

def collection_name_get(db, chanel, version=None):
	if version == None:
		version = db['notification_versions'].find({'_id':chanel}).next()['value']
	return "%s_notify_%s" %(chanel, int(version))

def writer_socket_get(chanel):
	dir = '/var/lib/pacifica/metanotification/sockets'
	return "%s/%s" %(dir, chanel)

class writer_socket_writer:
	def __init__(self, name, sync=False):
		try:
    			os.mkfifo(name)
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise
		flags = os.O_WRONLY
		if not sync:
			flags |= os.O_NONBLOCK
		self.fh = os.open(name, flags)
	def write(self, data):
		try:
			os.write(self.fh, data)
		except OSError, e:
			if e.errno != errno.EAGAIN:
				raise
	def entry(self, item_id, version):
		packed = struct.pack("<2q", item_id, version)
		self.write(packed)

def notification_version_get(host, port, db, chanel):
	client = Connection(host, port)
	db = client[db]
	scollection = db['notification_versions']
	doc = scollection.find({'_id':chanel}).next()
	version = doc['value']
	return int(version)
