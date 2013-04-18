#!/usr/bin/python

import os
import errno
import os.path

_open = open

def id2filename(id):
	s = "%x" %(id)
	d = ""
	while len(s) > 2:
		d = "%s/%s" %(d, s[-2:])
		s = s[:-2]
	if d == "":
		f = "/file.%s" %(s)
	else:
		f = "%s/%x" %(d, id)
	return f

def open_create(prefix, id, *args, **kwargs):
	filename = prefix + id2filename(id)
	retval = None
	try:
		retval = _open(filename, *args, **kwargs)
	except IOError, e:
		if e.errno == errno.ENOENT:
			dirname = filename[:filename.rindex('/')]
			try:
				os.makedirs(dirname)
			except OSError, e2:
        			if e2.errno != errno.EEXIST or not os.path.isdir(dirname):
					raise e2
			retval = _open(filename, *args, **kwargs)
		else:
			raise
	return retval

def open(prefix, id, *args, **kwargs):
	filename = prefix + id2filename(id)
	return _open(filename, *args, **kwargs)

if __name__ == '__main__':
	import sys
	print id2filename(int(sys.argv[1]))

