#!/usr/bin/python

import os
import sys
import errno
import urllib
import myemsl.elasticsearch
from myemsl.getconfig import getconfig
config = getconfig()
from myemsl.dbconnect import myemsldb_connect
from myemsl.brand import brand

from myemsl.logging import getLogger

logger = getLogger(__name__)

#FIXME this code is now slower then it could be. It already has all the metadata from elasticsearch, just use it instead of db calls.

def error(type, message, writer):
	if type:
		writer.write("<?xml version=\"1.0\"?><myemsl><error message=\"%s\"/></myemsl>\n" %(message))
	else:
		brand('header', writer)
		brand('middle', writer)
		writer.write("%s" %(message))
		brand('footer', writer)


def iteminfo(user, item_id, dtype, writer):
	type = None
	item_id = int(item_id)
	(code, document) = myemsl.elasticsearch.item_auth(int(user), item_id)
	if code != 200 or document == None:
		if code == 403:
			error(dtype, "Permission Denied.", writer)
		else:
			error(dtype, "Could not find item.", writer)
		return code
	sql = """
	select type from myemsl.items where item_id=%(item_id)s
	"""
	sys.stderr.write("SQL: %s\n" %(sql))
	cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
	cursor = cnx.cursor()
	cursor.execute(sql, {'item_id':item_id})
	rows = cursor.fetchall()
	for row in rows:
		type = row[0]
	if type == None or type != 'file':
		error(dtype, "Permission Denied", writer)
		return 0
	if type == 'file':
		sql = """
		select name, myemsl.files.verified, aged, submitter, eus.users.first_name, eus.users.last_name, stime, subdir, size from myemsl.files, myemsl.transactions, eus.users where item_id=%(item_id)s and myemsl.transactions.transaction = myemsl.files.transaction and eus.users.person_id = myemsl.transactions.submitter
		"""
		sys.stderr.write("SQL: %s\n" %(sql))
		cnx = myemsldb_connect(myemsl_schema_versions=['1.3'])
		cursor = cnx.cursor()
		cursor.execute(sql, {'item_id':item_id})
		rows = cursor.fetchall()
		for row in rows:
#FIXME subdirs
			subdir = row[7]
			if subdir:
				path = "%s/%s" %(row[7], row[0])
			else:
				path = row[0]
			path = urllib.quote(path)
			if dtype:
				writer.write("<?xml version=\"1.0\"?>\n<myemsl>\n")
				writer.write("   <itemid>%s</itemid>\n" %(item_id))
				writer.write("   <type>%s</type>\n" %(type))
				writer.write("   <filename>%s</filename>\n" %(row[0]))
				writer.write("   <size>%s</size>\n" %(row[8]))
				writer.write("   <verified>%s</verified>\n" %(row[1]))
				writer.write("   <aged>%s</aged>\n" %(row[2]))
				first = row[4]
				if not first:
					first = ''
				last = row[5]
				if not last:
					last = ''
				writer.write("   <submitter first=\"%s\" last=\"%s\" id=\"%s\"/>\n" %(first, last, row[3]))
				writer.write("   <stime>%s</stime>\n" %(row[6]))
				writer.write("   <checksum>\n")
			else:
        			brand('header', writer)
        			brand('middle', writer)
				writer.write("<table id=\"myemsl_iteminfo_table\">\n")
				writer.write("<tr><td>Item ID</td><td>%s</dt></tr>\n" %(item_id))
				writer.write("<tr><td>Type</td><td>%s</dt></tr>\n" %(type))
				#FIXME need to point to item server.
				writer.write("<tr><td>Filename</td><td><a href=\"/myemsl/files-basic/index.php?dir=item/%s/data/&file=%s\">%s</a></dt></tr>\n" %(item_id, path, row[0]))
				writer.write("<tr><td>Size</td><td>%s</td></tr>\n" %(row[8]))
				writer.write("<tr><td>Verified</td><td>%s</td></tr>\n" %(row[1]))
				writer.write("<tr><td>Aged</td><td>%s</td></tr>\n" %(row[2]))
				writer.write("<tr><td>Submitter</td><td>")
				if row[4]:
					writer.write("%s " %(row[4]))
				if row[5]:
					writer.write("%s " %(row[5]))
				writer.write("(%s)</td></tr>\n" %(row[3]))
				writer.write("<tr><td>Submit Time</td><td>%s</td></tr>\n" %(row[6]))
			sql = """
			select hashtype, hashsum from myemsl.hashsums where item_id=%(item_id)i
			"""
			cursor2 = cnx.cursor()
			cursor2.execute(sql, {'item_id':item_id})
			srows = cursor2.fetchall()
			for srow in srows:
				if dtype:
					tag = srow[0].lower()
					writer.write("      <%s>%s</%s>\n" %(tag, srow[1], tag))
				else:
					writer.write("<tr><td>%s</td><td>%s</td></tr>\n" %(srow[0], srow[1]))
			if dtype:
				writer.write("   </checksum>\n")
			else:
				writer.write("<tr><td id=\"myemsl_iteminfo_qr_label\">QR Code</td><td><img src=\"http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=https%%3A//my.emsl.pnl.gov/myemsl/qrs/item/%s\"></td></tr>\n" %(item_id))
			if dtype:
				writer.write("</myemsl>\n")
			else:
				writer.write("</table>\n")
       				brand('footer', writer)
	return 0

if __name__ == '__main__':
	sys.exit(iteminfo(sys.argv[1], none, sys.stdout))

