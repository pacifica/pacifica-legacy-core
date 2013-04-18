#!/usr/bin/env python

import sys
import PAM
from getpass import getpass

class BasicPAMAuth:
	def __init__(self, service, username, password, debug=False):
		self.username = username
		self.password = password
		self.service = service
		self.pw_used = False
		self.debug = debug
		self.auth = PAM.pam()
		self.auth.start(service)
		self.auth.set_item(PAM.PAM_USER, username)
		self.auth.set_item(PAM.PAM_CONV, self._conv)
		try:
			self.auth.authenticate()
#FIXME Understand this better
#			self.auth.acct_mgmt()
			self.authenticated = True
		except PAM.error, resp:
			if debug:
				print resp
			self.authenticated = False
		except Error, resp:
			if debug:
				print resp
			self.authenticated = False
	def _conv(self, auth, queries): #, user_data):
		if self.debug:
			print len(queries)
		response = []
		for i in range(len(queries)):
			(query, type) = queries[i]
			if type == PAM.PAM_PROMPT_ECHO_ON:
				if self.debug:
					print query
				response.append(('', 0))
			elif type == PAM.PAM_PROMPT_ECHO_OFF:
				if self.debug:
					print query
				if self.pw_used:
					response.append(('', 0))
				else:
					response.append((self.password, 0))
					self.pw_used = True
			elif type == PAM.PAM_PROMPT_ERROR_MSG or type == PAM.PAM_PROMPT_TEXT_INFO:
				if self.debug:
					print query
				response.append(('', 0))
			else:
				return None
		return response

def main():
	service = 'myemsl'
	username = sys.argv[1]
	password = getpass("Password:")

	auth = BasicPAMAuth(service, username, password, debug=True)
	print auth.authenticated

if __name__ == '__main__':
	main()
