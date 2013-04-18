#!/usr/bin/python

import _myemsl_archive

class ArchiveException(Exception):
	pass

class ArchiveEntry:
	def __init__(self):
		self._ae = _myemsl_archive.archive_entry_new()
		if self._ae == None:
			raise ArchiveException("Failed to create archive entry")
class ArchiveReader:
	def __init__(self):
		self._a = _myemsl_archive.archive_read_new()
		if self._a == None:
			raise ArchiveException("Failed to create archive")
		self._ae = ArchiveEntry()
		self.support_compression_all()
		self.support_format_all()

	def next_header(self):
		res = _myemsl_archive.archive_read_next_header2(self._a, self._ae._ae)
		if res == _myemsl_archive.ARCHIVE_EOF:
			return None
		if res != _myemsl_archive.ARCHIVE_OK:
			raise ArchiveException("next_header failed. %s", res)
		return self._ae

	def read_data(self, bs=10240):
		(e, d) = _myemsl_archive.myemsl_archive_read_data(self._a, bs)
		if e != 0:
			raise ArchiveException("Failed to read data")
		return d

	def open(self, filename, bs=10240):
		r = _myemsl_archive.archive_read_open_filename(self._a, filename, bs)
		if r != _myemsl_archive.ARCHIVE_OK:
			raise ArchiveException("Failed to open archive file %s" %(filename))
		return self

def init():
	syms = dir(_myemsl_archive)
	afuncs = [i[len('archvie_read_'):] for i in syms if i.startswith('archive_read_support')] + ['data_skip']
	for sym in afuncs:
		func = getattr(_myemsl_archive, 'archive_read_' + sym)
		def new_func(func):
			return lambda self: func(self._a)
		setattr(ArchiveReader, sym, new_func(func))
	aefuncs = ['size', 'pathname']
	for sym in aefuncs:
		func = getattr(_myemsl_archive, 'archive_entry_' + sym)
		def new_func(func):
			return lambda self: func(self._ae)
		setattr(ArchiveEntry, sym, new_func(func))

init()
