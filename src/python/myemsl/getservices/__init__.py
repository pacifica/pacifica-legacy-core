#!/bin/env python

import xml.dom.minidom

def getservices(url=None):
	if url != None:
		raise Exception("Not implemented yet")
	file = open('/etc/myemsl/services.xml', 'r')
	data = file.read()
	file.close()
	dom = xml.dom.minidom.parseString(data)
	prefix = ''
	services = []
	retval = {}
	for x in dom.firstChild.childNodes:
		if x.nodeType == x.ELEMENT_NODE:
			if x.nodeName == 'prefix':
				prefix = ''.join([i.data for i in x.childNodes if i.nodeType == i.TEXT_NODE])
			elif x.nodeName == 'services':
				services = x
	for x in services.childNodes:
		if x.nodeType == x.ELEMENT_NODE:
			if x.nodeName == 'service':
				name = x.getAttribute('name')
				location = x.getAttribute('location')
				if location[:1] == '/':
					location = prefix + location
				retval[name] = location
	return retval

if __name__ == '__main__':
	print getservices()
