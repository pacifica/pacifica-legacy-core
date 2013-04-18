#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")
sys.path.insert(0, "../src/misc")

import unittest
import tempfile
import shutil
import myemsl.util

class Util(unittest.TestCase):
        def setUp(self):
		self.tmpdir = tempfile.mkdtemp()
		print self.tmpdir
	def tearDown(self):
		shutil.rmtree(self.tmpdir)
	def test_try_open_create(self):
		file = myemsl.util.try_open_create("%s/foo/bar/baz/wark.txt" %(self.tmpdir))
		file.write("Test")
		file.close()

if __name__ == "__main__":
        unittest.main()

