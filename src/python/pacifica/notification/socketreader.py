import os
import sys
import errno
import fcntl
import struct

#FIXME taken from pacifica/notification/writer.py. Port it back to use this code.
class SocketReader:
	def __init__(self, socketname, cb):
		try:
    			os.mkfifo(socketname)
		except OSError, e:
			if e.errno != errno.EEXIST:
				raise
		self.socket = os.open(socketname, os.O_RDONLY | os.O_NONBLOCK)
		self.socket_write = os.open(socketname, os.O_WRONLY | os.O_NONBLOCK)
		fl = fcntl.fcntl(self.socket, fcntl.F_GETFL)
		fcntl.fcntl(self.socket, fcntl.F_SETFL, fl & (~os.O_NONBLOCK))
		self.cb = cb
	def run(self):
		#512 atomic read is min garanteed by posix. This number is provided by select.PIPE_BUF only in python >= 2.7. :(
		PIPE_BUF = 512
		while(True):
			data = os.read(self.socket, PIPE_BUF)
			if len(data) % 16 != 0:
				sys.stderr.write("Bad read from pipe. Size is not right! %s\n" %(len(data)))
				return -1
			f = "<%sq" %(len(data) / 8)
			unpacked = struct.unpack(f, data)
			s = [(unpacked[i*2], unpacked[i*2+1]) for i in range(0, len(unpacked)/2)]
			for (i, v) in s:
				self.cb(i, v)

def main():
	def cb(i, v):
		print i, v
	s = SocketReader(sys.argv[1], cb)
	s.run()

if __name__ == '__main__':
	main()
