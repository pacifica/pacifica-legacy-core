import os
import os.path
import errno
import fcntl

def readlines_nonblocking(fd, rest=""):
	flags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
	eof = False
	alldata = rest
	while True:
		data = ""
		try:
			data = os.read(fd, 1024)
			if len(data) == 0:
				eof = True
				break
		except OSError, e:
			if e.errno != errno.EAGAIN:
				fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)
				raise
			else:
				break
		except:
			fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)
			raise
		alldata += data
	lines = []
	if len(alldata) == 0:
		return {'lines': lines, 'rest': alldata, 'eof': eof}
	if alldata[len(alldata) - 1] != '\n':
		idx = alldata.rfind('\n')
		if idx != -1:
			lines = alldata[:idx].split('\n')
			rest = alldata[idx + 1:]
		else:
			rest = alldata
	else:
		lines = alldata[:len(alldata) - 1].split('\n')
		rest = ''
	fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)
	return {'lines': lines, 'rest': rest, 'eof': eof}

def try_remove(filename):
	try:
		os.remove(filename)
	except OSError, e:
		if e.errno != errno.ENOENT:
			raise

def try_mkdir(dir, priv=False, mode=None):
	try:
		if priv:
			os.makedirs(dir, 0700)
		else:
			if mode != None:
				os.makedirs(dir, mode)
			else:
				os.makedirs(dir)
	except OSError, e:
		if e.errno != errno.EEXIST:
			raise

def string_to_bool(str):
	return not str.lower() in ("no", "false", "f", "0", "n")

def try_open_create(filename, priv=False, dirmode=None):
	try:
		res = open(filename, 'w')
	except IOError, e:
		if e.errno != errno.ENOENT:
			raise
		try_mkdir(os.path.dirname(filename), priv=priv, mode=dirmode)
		res = open(filename, 'w')
	return res
		
