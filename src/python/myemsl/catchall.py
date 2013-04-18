#!/usr/bin/python

def main():
	import sys, os, os.path
	if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
		print "usage: catchall.py scriptfile [arg] ..."
		sys.exit(2)

	mainpyfile =  sys.argv[1]     # Get script filename
	if not os.path.exists(mainpyfile):
		print 'Error:', mainpyfile, 'does not exist'
		sys.exit(1)
	for i in range(0, len(sys.argv)):
		if sys.argv[i] == '-j':
			try:
				jobid = sys.argv[i+1]
			except:
				jobid = "-1"
		if sys.argv[i][:7] == "--jobid":
			if len(sys.argv[i][9:]):
				jobid = sys.argv[i][9:]
			else:
				try:
					jobid = sys.argv[i+1]
				except:
					jobid = "/tmp/foo"

	del sys.argv[0]         # Hide "catchall.py" from argument list

	# Replace catchall's dir with script's dir in front of module search path.
	sys.path[0] = os.path.dirname(mainpyfile)

	import __main__
	__main__.__dict__.clear()
	__main__.__dict__.update({"__name__"    : "__main__",
	                          "__file__"    : mainpyfile,
	                         })
	globals = __main__.__dict__
	locals = globals
	try:
		exec 'execfile( "%s")' % mainpyfile in globals, locals
	except Exception, ex:
		import traceback
		from StringIO import StringIO
		import sys
		import urllib
		exc_type, exc_value, exc_traceback = sys.exc_info()
		if str(exc_type) == "exceptions.SystemExit":
			sys.exit(0)
		tbdata = StringIO()
		traceback.print_exception(exc_type, exc_value, exc_traceback,
		              limit=10, file=tbdata)
		tbdata.seek(0)
		data = tbdata.read()
		(type, value, traceback) = sys.exc_info()
		import myemsl.ingest
		myemsl.ingest.update_state(jobid, 0, "ERROR", "%s\n%s\n%s\n%s\n"%(str(type), str(value), str(traceback), urllib.quote(data, safe="")))


if __name__ == '__main__':
	main()
