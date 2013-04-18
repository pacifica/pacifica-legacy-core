import importlib
config = importlib.import_module('logging.config')
logging = importlib.import_module('logging')

inited = False

def configLogger(configfile):
	global inited
	config.fileConfig("/etc/myemsl/logging.%s.conf" %(configfile))
	inited = True

def getLogger(*args, **kwargs):
	global inited
	if not inited:
		config.fileConfig("/etc/myemsl/logging.conf")
		inited = True
	return logging.getLogger(*args, **kwargs)
