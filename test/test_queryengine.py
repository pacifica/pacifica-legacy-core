#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")

import os
import pgdb
import time
import unittest 
import StringIO
import ConfigParser
import xml.dom.minidom
from myemsl.service import queryengine
from myemsl import dbconnect

class QueryEngine(unittest.TestCase):
        def setUp(self):
		config = ConfigParser.SafeConfigParser()
		config.read('myemsl_testdb.ini')
		self.config = config
	def getFiles(self, person_id):
		file_2_itemid = None
                data = StringIO.StringIO()
                queryengine.base_query("%s/data" %(person_id), data, config=self.config)
		data.seek(0)
		dom = xml.dom.minidom.parseString(data.read())
		file_2_itemid = {}
		for x in dom.firstChild.childNodes:
			if x.nodeType == x.ELEMENT_NODE and x.nodeName == "file":
				file_2_itemid[x.getAttribute('name')] = x.getAttribute('itemid')
		return file_2_itemid
	def test_f1_queryengine_perm_submitter(self):
		file_2_itemid = self.getFiles(1)
		self.failUnless(file_2_itemid.has_key('f1'), "user1 can not see f1")
	def test_f1_queryengine_perm_not_submitter(self):
		file_2_itemid = self.getFiles(2)
		self.failIf(file_2_itemid.has_key('f1'), "user2 can see f1")
	def test_f2_queryengine_perm_submitter(self):
		file_2_itemid = self.getFiles(2)
		self.failUnless(file_2_itemid.has_key('f2'), "user2 can not see f2")
	def test_f2_queryengine_perm_not_submitter_on_proposal(self):
		file_2_itemid = self.getFiles(1)
		self.failUnless(file_2_itemid.has_key('f1'), "user1 can not see f1")
	def test_f3_queryengine_perm_only_submitter(self):
		file_2_itemid = self.getFiles(1)
		self.failUnless(file_2_itemid.has_key('f3'), "user1 can not see f3")
	def test_f3_queryengine_perm_not_submitter(self):
		file_2_itemid = self.getFiles(2)
		self.failIf(file_2_itemid.has_key('f3'), "user2 can see f3")
	def test_f4_queryengine_perm_aged_submitter(self):
		file_2_itemid = self.getFiles(2)
		self.failUnless(file_2_itemid.has_key('f4'), "user2 can not see f4")
	def test_f4_queryengine_perm_aged_not_submitter_not_group(self):
		file_2_itemid = self.getFiles(1)
		self.failUnless(file_2_itemid.has_key('f4'), "user1 can see f4")
	def test_f5_queryengine_version_user1(self):
		file_2_itemid = self.getFiles(1)
		id = file_2_itemid['f5']
		self.failUnless(id == '5', "user1 got wrong version of f5 %s" %(id))
	def test_f5_queryengine_version_user2(self):
		file_2_itemid = self.getFiles(2)
		id = file_2_itemid['f5']
		self.failUnless(id == '7', "user2 got wrong version of f5 %s" %(id))
	def test_f6_queryengine_version_user1(self):
		file_2_itemid = self.getFiles(1)
		id = file_2_itemid['f6']
		self.failUnless(id == '8', "user1 got wrong version of f6 %s" %(id))
	def test_f6_queryengine_version_user2(self):
		file_2_itemid = self.getFiles(2)
		id = file_2_itemid['f6']
		self.failUnless(id == '8', "user2 got wrong version of f6 %s" %(id))
                
if __name__ == "__main__":
        unittest.main()

