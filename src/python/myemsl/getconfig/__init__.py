#!/bin/env python

import ConfigParser

class cartd:
	def __init__(self, config):
		self.config = config
		self.settings = {}
		self.intkeys = ['max_size', 'disk_size', 'expire_hours']
		self.intkeys = dict([(i, True) for i in self.intkeys])
	def __getattr__(self, attr):
		v = self.settings.get(attr)
		if v:
			return v
		try:
			if attr in self.intkeys:
				v = self.config.getint('cartd', attr)
			else:
				v = self.config.get('cartd', attr)
		except:
			if attr == 'basedir':
				v = '/srv/myemsl-cartd'
			elif attr == 'amalgam_basedir':
				v = '/srv/amalgamfs'
			elif attr == 'readydir':
				v = self.basedir + '/ready'
			elif attr == 'amalgam_readydir':
				v = self.amalgam_basedir + '/working'
			elif attr == 'pendingdir':
				v = self.basedir + '/pending'
			elif attr == 'amalgam_pendingdir':
				v = self.amalgam_basedir + '/pending'
			elif attr == 'disk_size':
				v = 200 * 1024 * 1024 * 1024 #200GB
			elif attr == 'max_size':
				v = 10 * 1024 * 1024 * 1024 #10GB
			elif attr == 'expire_hours':
				v = 24
		self.settings[attr] = v
		return v

class ingest:
	def __init__(self, config):
		self.config = config
	def __getattr__(self, attr):
		try:
			if attr == 'job_offset':
				v = self.config.getint('ingest', attr)
			else:
				v = self.config.get('ingest', attr)
		except:
			if attr == 'job_offset':
				v = 0
			else:
				raise
		return v

class notification:
	def __init__(self, config, channel):
		self.config = config
		self.channel = channel
	def __getattr__(self, attr):
		try:
			section = "notification_%s" %(self.channel)
			if attr == 'port':
				v = self.config.getint(section, attr)
			else:
				v = self.config.get(section, attr)
		except:
			try:
				if attr == 'port':
					v = self.config.getint("notification_defaults", attr)
				else:
					v = self.config.get("notification_defaults", attr)
			except:
				raise
		return v

def getconfig():
	config = ConfigParser.SafeConfigParser()
	config.read('/etc/myemsl/general.ini')
	config.cartd = cartd(config)
	config.ingest = ingest(config)
	return config

def getconfig_notification(channel):
	config = getconfig()
	config.notification = notification(config, channel)
	return config

def getconfig_secret():
	config = getconfig()
	config.read('/etc/myemsl/secret.ini')
	return config
