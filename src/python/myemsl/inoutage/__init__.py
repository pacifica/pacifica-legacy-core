#!/usr/bin/python

import os
import sys
import errno

def in_outage(try_list):
	res = True
	try:
		stat = os.stat('/dev/shm/myemsl/inited')
		if stat.st_uid == 0:
			res = False
	except OSError, e:
		if e.errno != errno.ENOENT and e.errno != errno.EACCES:
			raise
	if not res:
		try_list = ["/dev/shm/myemsl/outage/%s" %(i) for i in try_list]
		for file in try_list:
			try:
				stat = os.stat(file)
				if stat.st_uid == 0:
					res = True
					break
			except OSError, e:
				if e.errno != errno.ENOENT and e.errno != errno.EACCES:
					raise
	return res

if __name__ == '__main__':
	sys.exit(in_outage(["storage", "myemsl"]))
