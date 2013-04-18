from getalias import *
from createalias import *
from createindex import *
from deleteindex import *
from createuserfilter import *
from jsondumper import *
from bulkaction import *
from jsonentry import *
from schema import *
from StringIO import StringIO

import pycurl
import myemsl.getconfig

import simplejson as json

config = myemsl.getconfig.getconfig()

class chunkit:
        def __init__(self, callback, count):
                self.a = []
                self.callback = callback
                self.count = count
        def flush(self):
                self.callback(self.a)
                self.a = []
        def add(self, element):
                if len(self.a) >= self.count:
                        self.flush()
                self.a.append(element)

class bulkupload:
        def __init__(self, index, type="simple"):
                self.index = index
                self.type = type
        def callback(self, elements):
                new_elements = []
                for e in elements:
                        new_elements.append({"index":{"_type":self.type, "_id": e.entry['_id']}})
                        new_elements.append(e.entry)
                res = bulk_action(self.index, new_elements)
                for e in elements:
			e.done(res == 200)

#FIXME most of this code looks just like elasticsearch service's code (Since copied from. consider generalizing that code)
def item_get(item_id):
	user_tries = 2
	while user_tries > 0:
		server = config.get('elasticsearch', 'server')
		writebody = StringIO()
		curl = pycurl.Curl()
		curl.setopt(pycurl.FOLLOWLOCATION, 1)
		curl.setopt(pycurl.MAXREDIRS, 5)
		curl.setopt(pycurl.SSL_VERIFYPEER, config.get('webservice', 'ssl_verify_peer') != 'False')
		curl.setopt(pycurl.SSL_VERIFYHOST, config.get('webservice', 'ssl_verify_host') != 'False')
		url = server
		if url[-1:] != '/':
			url += '/'
#FIXME unhardcode these...
		url += "%s/%s/%i" %('myemsl_current_simple_items', 'simple_items', item_id)
		curl.setopt(curl.URL, url)
		curl.setopt(curl.WRITEFUNCTION, writebody.write)
		curl.perform()
		code = curl.getinfo(pycurl.HTTP_CODE)
		curl.close()
		if code != 404:
			writebody.seek(0)
			j = json.load(writebody)
			if not j.get('_source'):
				return 500, None
			return code, j['_source']
		user_tries -= 1
		return 404, None

def item_auth(user_id, item_id):
	(code, document) = item_get(item_id)
	if code != 404:
		if not document:
			return 500, document
		if not document.get('aged'):
			return 500, document
		if not document.get('users'):
			return 500, document
		if document['aged'] != 'false' or user_id in document['users']:
			return 200, document
		return 403, document
	return 500, document
