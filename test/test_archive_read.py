#!/usr/bin/python

import sys

sys.path.insert(0, "../src/python")
sys.path.insert(0, "../src/misc")

import unittest
import hashlib
import _myemsl_archive as archive

class ArchiveRead(unittest.TestCase):
        def setUp(self):
		self.ae = archive.archive_entry_new()
		self.a = archive.archive_read_new()
		archive.archive_read_support_compression_all(self.a)
		archive.archive_read_support_format_all(self.a)
	def tearDown(self):
		r = archive.archive_read_close(self.a)
		if r != archive.ARCHIVE_OK:
			raise Exception("Failed to shutdown")
			archive.archive_read_finish(self.a)
	def test_extract(self):
		h = hashlib.sha1()
		r = archive.archive_read_open_filename(self.a, "testdata.tar", 10240)
		self.failIf(r != archive.ARCHIVE_OK, "Failed to open testdata.tar")
		while (archive.archive_read_next_header2(self.a, self.ae) == archive.ARCHIVE_OK):
			(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
			self.failIf(e != 0, "Failure during data read %s" %(e))
			while(len(d) > 0):
				h.update(d)
				(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
				self.failIf(e != 0, "Failure during data read %s" %(e))
			file_hash = h.hexdigest()
			sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
			self.failIf(file_hash != sha1, "Data verify failed. Sha1 sums don't match. %s != %s" %(file_hash, sha1))
	def test_skip(self):
		h = hashlib.sha1()
		r = archive.archive_read_open_filename(self.a, "testdata2.tar", 10240)
		self.failIf(r != archive.ARCHIVE_OK, "Failed to open testdata2.tar")
		while (archive.archive_read_next_header2(self.a, self.ae) == archive.ARCHIVE_OK):
			name = archive.archive_entry_pathname(self.ae)
			if name != 'testdata':
				archive.archive_read_data_skip(self.a)
				continue
			(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
			self.failIf(e != 0, "Failure during data read %s" %(e))
			while(len(d) > 0):
				h.update(d)
				(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
				self.failIf(e != 0, "Failure during data read %s" %(e))
			file_hash = h.hexdigest()
			sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
			self.failIf(file_hash != sha1, "Data verify failed. Sha1 sums don't match. %s != %s" %(file_hash, sha1))
	def test_truncated_file(self):
		h = hashlib.sha1()
		r = archive.archive_read_open_filename(self.a, "testdata3.tar", 10240)
		self.failIf(r != archive.ARCHIVE_OK, "Failed to open testdata3.tar")
		while (archive.archive_read_next_header2(self.a, self.ae) == archive.ARCHIVE_OK):
			(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
			while(e == 0 and len(d) > 0):
				h.update(d)
				(e, d) = archive.myemsl_archive_read_data(self.a, 10240)
			file_hash = h.hexdigest()
			sha1 = '51c15743ad61d2ceb55a05efb073d73fc9a759cb'
			self.failIf(file_hash == sha1, "Data verify failed. Sha1 sums match. %s != %s" %(file_hash, sha1))
			self.failIf(e == 0, "Error did not show up.")

if __name__ == "__main__":
        unittest.main()

