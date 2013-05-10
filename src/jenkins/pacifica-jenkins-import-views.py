#!/usr/bin/python

import os
import os.path
import sys
import xml.dom.minidom

configfile = sys.argv[1]
file = open(configfile, "r")
config = xml.dom.minidom.parse(file)
file.close

path = os.path.dirname(os.path.abspath(__file__))

views = {}
for i in os.listdir(path + "/views"):
	file = open(path + "/views/%s" %(i), "r")
	x = xml.dom.minidom.parse(file)
	file.close()
	for j in x.firstChild.childNodes:
		if j.nodeType == j.ELEMENT_NODE and j.nodeName == 'name':
			views[j.firstChild.data] = x.firstChild


to_delete = []

for i in config.firstChild.childNodes:
	if i.nodeType == i.ELEMENT_NODE and i.nodeName == 'views':
		for j in i.childNodes:
			if j.nodeType == j.ELEMENT_NODE:
				for k in j.childNodes:
					if k.nodeType == k.ELEMENT_NODE and k.nodeName == 'name':
						if k.firstChild.data in views:
							to_delete.append(j)
		for j in to_delete:
			i.removeChild(j)
		for (key, val) in views.iteritems():
			i.appendChild(val)

file = open("/tmp/tmp-config.xml", "w")
file.write(config.toxml())
file.close()
os.rename("/tmp/tmp-config.xml", configfile)

