#!/usr/bin/python

import sys
import urllib
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
import simplejson as json

from myemsl.logging import getLogger

logger = getLogger(__name__)

#FIXME make max predicate desc configurable.
def predicate(user, path, type, data, writer, chunk_size=4096, max_predicate_desc=1024*1024):
	user = int(user)
	if type != 'PUT' and type != "POST":
        	logger.debug("Bad type %s\n" %(type))
	else:
		desc = ""
		while True:
        		d = data.read(chunk_size)
        		if not d:
            			break
			desc += d
        	logger.debug("Got |%s|\n" %(str(desc)))
		try:
			res = json.loads(desc)
			print res.keys()
			if 'description' in res and 'short' in res['description'] and res['description']['short'].strip() != "" and 'long' in res['description'] and res['description']['long'].strip() != "":
				sql = """
				insert into myemsl.local_predicate(person_id, "desc") values(%(person_id)i, %(desc)s)
				"""
        			logger.debug("SQL: %s\n" %(sql))
#FIXME version
				cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
				cursor = cnx.cursor()
				cursor.execute(sql, {'person_id':user, 'desc':desc})
				cnx.commit()
			else:
        			logger.debug("Bad document\n");
		except Exception, e:
        		logger.debug("Bad document %s\n" %(e));
	
	return 0

if __name__ == '__main__':
	sys.exit(predicate(int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.stdin, sys.stdout))

