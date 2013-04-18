#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")
sys.path.insert(0, "../src/misc")

import unittest
import hashlib
import myemsl.archive

class ArchiveRead(unittest.TestCase):
        def setUp(self):
		self.a = myemsl.archive.ArchiveReader()
	def test_extract(self):
		h = hashlib.sha1()
		self.a.open("testdata.tar")
		he = self.a.next_header()
		while he:
			d = self.a.read_data()
			while(len(d) > 0):
				h.update(d)
				d = self.a.read_data()
			file_hash = h.hexdigest()
			sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
			self.failIf(file_hash != sha1, "Data verify failed. Sha1 sums don't match. %s != %s" %(file_hash, sha1))
			he = self.a.next_header()
	def test_skip(self):
		h = hashlib.sha1()
		self.a.open("testdata2.tar")
		he = self.a.next_header()
		while he:
			name = he.pathname()
			if name != 'testdata':
				self.a.data_skip()
			else:
				d = self.a.read_data()
				while(len(d) > 0):
					h.update(d)
					d = self.a.read_data()
				file_hash = h.hexdigest()
				sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
				self.failIf(file_hash != sha1, "Data verify failed. Sha1 sums don't match. %s != %s" %(file_hash, sha1))
			he = self.a.next_header()
	def test_truncated_file(self):
		h = hashlib.sha1()
		self.a.open("testdata3.tar")
		exception_seen = False
		try:
			he = self.a.next_header()
			while he:
				d = self.a.read_data()
				while(len(d) > 0):
					h.update(d)
					d = self.a.read_data()
				file_hash = h.hexdigest()
				sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
				self.failIf(file_hash != sha1, "Data verify failed. Sha1 sums don't match. %s != %s" %(file_hash, sha1))
				he = self.a.next_header()
		except:
			exception_seen = True
		self.failIf(not exception_seen, "Truncation did not throw an error")

if __name__ == "__main__":
        unittest.main()

