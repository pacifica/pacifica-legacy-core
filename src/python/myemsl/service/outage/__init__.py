#!/usr/bin/python

import os

def outage_mime(type):
	if type == 'xml':
		return 'text/xml'
	elif type == 'ajax':
		return 'text/json'
	else:
		return 'text/plain'

def outage(type, writer):
	msg = None
	outage_type = "unknown"
	try:
		f = os.stat('/dev/shm/myemsl/inited')
	except:
		msg = "Starting up..."
	try:
		f = open('/dev/shm/myemsl/outage/storage')
		msg = f.read()
		f.close()
		outage_type = "storage"
	except:
		pass
	try:
		f = open('/dev/shm/myemsl/outage/myemsl')
		msg = f.read()
		f.close()
		outage_type = "myemsl"
	except:
		pass
	if msg == None:
		msg = "Not in outage"
	if type == 'xml':
		pass
		writer.write("<?xml version=\"1.0\"?>\n")
	elif type == 'ajax':
		import simplejson
		writer.write('[{"outage":"%s", "message":%s}]' %(outage_type, simplejson.dumps(msg)))
	elif type == 'sstp':
		writer.write('Outage: %s' %(msg))
	else:
		writer.write(str(msg))

if __name__ == '__main__':
	outage(sys.argv[1], sys.stdout)

