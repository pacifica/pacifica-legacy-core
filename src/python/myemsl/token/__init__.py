#!/usr/bin/python

import simplejson as json
import datetime

import rfc3339parse
import rfc3339enc
import minify_json

import sign
import time
import verify

def simple_items_token_gen(items, duration=60 * 60, person_id=None):
#FIXME read in from config.
	uuid = 'huYNwptYEeGzDAAmucepzw';
	js = {'s':rfc3339enc.rfc3339(time.time()), 'd':duration, 'u':uuid, 'i':items, 'o':0}
	if person_id != None and person_id != "":
		js['p'] = person_id
	stok = token_gen(js, '')
	return stok

def token_gen(pub, priv):
	if priv == None:
		priv = ''
	if len(priv) > 0:
		pub['o'] = len(priv)
	else:
		try:
			del pub['o']
		except:
			pass
	jss = minify_json.json_minify(json.dumps(pub))
	td = jss[1:-1]
	sig = sign.sign(td + priv)
	tok = "%s%s%s%s" %(len(td), td, priv, sig)
	return tok.encode('base64').replace('\n', '').replace('=', '')

def token_parse(stok):
	stoklen = len(stok)
	pad = ['', '===', '==', '='][stoklen % 4]
	tok2 = (stok + pad).decode('base64')
	i = 0
	while i < len(tok2) and tok2[i] >= '0' and tok2[i] <= '9':
		i += 1
	end = int(tok2[0:i]) + i
	jtok = json.loads("{%s}" %(tok2[i:end]))
	o = 0
	if jtok.has_key('o'):
		o = jtok['o']
	vdata = tok2[i:end + o]
	sig = tok2[end + o:]
	if not verify.verify(vdata, sig):
		raise Exception("Verification failed.")
	if o > 0:
		return jtok, tok2[end: end + o]
	return jtok, None

def token_validate_time(pub, secs_before_valid=5*60, secs_valid_max=60*60*6):
	dt = rfc3339parse.parse_datetime(pub['s'])
	now = rfc3339parse.now()
	if (dt - datetime.timedelta(seconds=secs_before_valid)) > now:
		return False
	if now > (dt + datetime.timedelta(seconds=pub['d'])):
		return False
	return True
