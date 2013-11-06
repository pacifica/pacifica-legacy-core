from mod_python import apache, util

import os
import errno
import xattr
import datetime

import myemsl.id2filename
from myemsl.dbconnect import myemsldb_connect
from myemsl.logging import getLogger
from myemsl.getconfig import getconfig
from pymongo import Connection
import pymongo
config = getconfig()

logger = getLogger(__name__)

def process(item, filename, req):
	"""Actually process the request."""
	request_data = util.FieldStorage(req, keep_blank_values=True)
	get_levels = request_data.getfirst("levels")
	if get_levels != None:
		try:
			x = xattr.getxattr(filename, "user.levels")
		except:
			x = "1"
		req.headers_out['X-MyEMSL-Levels'] = x
		total = "2"
		try:
			total = str(config.getint('sumcheck', 'levels_needed'))
		except:
			pass
		req.headers_out['X-MyEMSL-Levels-Total'] = total
	get_locked = request_data.getfirst("locked")
	if get_locked == "":
		x = ""
		try:
			x = xattr.getxattr(filename, 'user.disk_stage_status')
			if x == "1":
				x = "true"
			else:
				x = "false"
		except:
			x = "true"
		req.headers_out['X-MyEMSL-Locked'] = x
		if x == "false":
			return apache.HTTP_SERVICE_UNAVAILABLE
	logger.debug("Returning: %s" %(filename))
	req.headers_out['X-SENDFILE'] = filename
	req.headers_out['Content-Disposition'] = 'attachment'
	logentry = {
	  'd': datetime.datetime.now(),
	  'i': item
	}
	try:
		logentry['p'] = int(req.user)
	except:
		pass
	return apache.OK

#FIXME split this into handler and service.
#FIXME this is specific to the MyEMSL 1, old way of doing things. Make this better in 2.0
def handler(req):
	"""Find the requested item and process the request. It will look in the new archive location and fall back to asking the database where the old location is and use that if it doesn't exist. This behavior should only exist until migration to 2.0 layout is complete."""
	prefix = "/srv/myemsl-item/"
	path = req.unparsed_uri.split('/', 6)
	item = int(path[5])
	try:
		filename = "%s/bundle/%s" %(prefix, myemsl.id2filename.id2filename(item))
		os.stat(filename)
		return process(item, filename, req)
	except OSError, e:
		if e.errno != errno.ENOENT:
			raise
	sql = """
	select name, subdir, f.transaction, submitter from myemsl.files as f, myemsl.transactions as t where item_id = %(item_id)s and f.transaction = t.transaction
	"""
	logger.debug("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'item_id':item})
	rows = cursor.fetchall()
	for row in rows:
		filename = "%s%s/bundle/%s/%s/%s" %(prefix, row[3], row[2], row[1], row[0])
		return process(item, filename, req)
	return apache.FNF
