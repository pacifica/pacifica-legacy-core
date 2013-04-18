#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")

import unittest
import ConfigParser
from myemsl import getpermission
from myemsl import dbconnect

class QueryEngine(unittest.TestCase):
        def setUp(self):
		config = ConfigParser.SafeConfigParser()
		config.read('myemsl_testdb.ini')
		self.config = config
	def test_get_permission_bool_true(self):
		retval = getpermission.get_permission_bool(1, 'instrument.test', 'p', config=self.config)
		self.failUnless(retval, "get permission bool true test failed")
	def test_get_permission_bool_false_permission(self):
		retval = getpermission.get_permission_bool(1, 'instrument.test', 'o', config=self.config)
		self.failIf(retval, "get permission bool false permission test failed")
	def test_get_permission_bool_false_user(self):
		retval = getpermission.get_permission_bool(2, 'instrument.test', 'p', config=self.config)
		self.failIf(retval, "get permission bool false user test failed")
	def test_get_permission_bool_false_class(self):
		retval = getpermission.get_permission_bool(1, 'instrument.test2', 'p', config=self.config)
		self.failIf(retval, "get permission bool false class test failed")

if __name__ == "__main__":
        unittest.main()

