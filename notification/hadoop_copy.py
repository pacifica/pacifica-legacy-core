#!/usr/bin/env python

import sys
import os
import subprocess

def file_operation(obj, file):
	"""Simple hello world style python file operation
	Prints the file name and the object passed as the first argument
	"""
	toFile = ""
	fromFile = file
	if file[:len(obj["path"])] == obj["path"]:
		toFile = file[len(obj["path"]):]
	else:
		toFile = file
	toFile = obj["dest_path"]+toFile
	print "fromFile %s" %(fromFile)
	print "toFile %s" %(toFile)
	#tmp = subprocess.Popen("/usr/bin/ssh %s@%s '/bin/bash -l -c \"hadoop fs -copyFromLocal - %s\"'"%(obj["username"], obj["hostname"], toFile.replace(" ", "\ ")), shell=True, stdin=open(fromFile, "r"))
	tmp = subprocess.Popen("/usr/bin/ssh %s@%s '/bin/bash -l -c \"cat > %s\"'"%(obj["username"], obj["hostname"], toFile.replace(" ", "\ ")), shell=True, stdin=open(fromFile, "r"))
	tmp.wait()
	return 1

def dir_operation(obj, dir):
	"""Simple hello world style python directory operation
	Prints the directory name and the object passed as the first argument
	"""
	print dir
	if dir[:len(obj["path"])] == obj["path"]:
		dir = dir[len(obj["path"]):]
	dir = obj["dest_path"]+dir
	#tmp = subprocess.Popen("/usr/bin/ssh %s@%s '/bin/bash -l -c \"hadoop fs -mkdir %s\"'"%(obj["username"], obj["hostname"], dir.replace(" ", "\ ")), shell=True)
	tmp = subprocess.Popen("/usr/bin/ssh %s@%s '/bin/bash -l -c \"mkdir %s\"'"%(obj["username"], obj["hostname"], dir.replace(" ", "\ ")), shell=True)
	tmp.wait()
	return 1

def python_fsc_register():
	"""Implement this function so the python worker module can pick up on
	which functions you want to use for doing the file and directory 
	operations and you can pass along an object to return as well.

	Also prints sys.argv to show you what the argument list is.
	"""
	print sys.argv
	myglobals = {}
	myglobals["username"]=sys.argv[2]
	myglobals["hostname"]=sys.argv[3]
	myglobals["path"]=sys.argv[4]
	myglobals["dest_path"]=sys.argv[5]
	return (myglobals, file_operation, dir_operation)

def python_fsc_destroy(data):
	print "Destroy"
	return
