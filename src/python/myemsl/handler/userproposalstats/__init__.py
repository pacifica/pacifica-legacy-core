from mod_python import apache, util
import urllib
import datetime
import simplejson as json
from myemsl.token import rfc3339parse

from myemsl.service import userproposalstats
import myemsl.util

from myemsl.logging import getLogger
logger = getLogger(__name__)

def handler(req):
	req.content_type = "application/json; charset=UTF-8"
	code = apache.OK
	if req.method == "POST":
		input = json.load(req)
		if 'start' not in input or 'end' not in input:
			return apache.HTTP_BAD_REQUEST
		start = rfc3339parse.parse_date(input['start'])
		end = rfc3339parse.parse_date(input['end'])
		if type(start) == datetime.date:
			start = datetime.datetime.combine(start, datetime.datetime.min.time())
		if type(end) == datetime.date:
			end = datetime.datetime.combine(end, datetime.datetime.min.time())
		doc = []
		def cb(personid, items):
			doc.append({'pid': personid, 'p': items})
		userproposalstats.log_items_to_person_proposals(start, end, cb)
		json.dump(doc, req)
	else:
		return apache.HTTP_NOT_IMPLEMENTED
	return apache.OK
