#!/usr/bin/python

import os,sys
import array
import myemsl.id2filename
from myemsl.dbconnect import myemsldb_connect
from myemsl.getconfig import getconfig_secret
CONFIG = getconfig_secret()

"""
Logic for transitioning the data from old to new item server format.

 1. get all items from a user
 2. check the old file name and new file name and log it
 3. log the move
"""

if __name__ == '__main__':
  sql = """
select
  name,
  subdir,
  f.transaction,
  submitter,
  item_id
from
  myemsl.files as f,
  myemsl.transactions as t
where
  f.transaction = t.transaction and
  t.submitter = %(submitter)s
"""
  cnx = myemsldb_connect(myemsl_schema_versions=['1.0'])
  cursor = cnx.cursor()
  cursor.execute(sql, {'submitter':sys.argv[1]})
  rows = cursor.fetchall()
  for row in rows:
    itemid = row[4]
    prefix = "/srv/myemsl-ingest"
    newfilename = "%s/bundle/%s"%(prefix, myemsl.id2filename.id2filename(itemid))
    oldfilename = "%s/%s/bundle/%s/%s/%s" %(prefix, row[3], row[2], row[1], row[0])
    if os.access(newfilename, os.F_OK):
      print "(%s)(%s) new file exists"%(newfilename, oldfilename)
    elif os.access(oldfilename, os.F_OK):
      print "(%s)(%s) old file exists"%(newfilename, oldfilename)
    else:
      print "(%s)(%s) neither exists"%(newfilename, oldfilename)
    if os.access(oldfilename, os.F_OK) and os.access(newfilename, os.F_OK):
      print "both exist"
    if os.access(oldfilename, os.F_OK) and not os.access(newfilename, os.F_OK):
      print "copying file"
      d = os.path.dirname(newfilename)
      dirs = []
      while not os.path.isdir(d):
        dirs.append(d)
        d = os.path.dirname(d)
      for d in reversed(dirs):
        # switch this on and off
        os.mkdir(d, mode=0755)
        print "(%s) created dir"%(d)
      # switch this on and off
      from shutil import copy
      tries=0
      while tries < 9:
        try:
          copy(oldfilename, newfilename)
        except IOError, ex:
          from time import sleep
          from math import pow
          sleep(int(pow(2, tries)))
          tries += 1
          print "failed %d" %(tries)
      if tries >= 9:
        raise IOError("tried 10 or more times to copy files (%s, %s)"%(oldfilename, newfilename))
    def walker(arg, dirname, fnames):
      """
      Check to see if there are any files left.
      """
      for f in fnames:
        if not os.path.isdir(dirname+"/"+f):
          arg["hasfile"] = 1
      arg["dirs"].append(dirname)
    bundledir = "%s/%s/bundle/%s"%(prefix, row[3], row[2])
    data = {"hasfile":0, "dirs":[]}
    os.path.walk(bundledir, walker, data)
    if data["hasfile"] == 0:
      for d in reversed(data["dirs"]):
        #os.rmdir(d)
        print "(%s) removing dir"%(d)
      
