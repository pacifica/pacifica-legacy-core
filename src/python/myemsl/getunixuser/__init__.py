#!/usr/bin/python

from myemsl.getconfig import getconfig

def get_unix_user():
	config = getconfig()
	return config.get('unix', 'user')

def main():
	print get_unix_user()

if __name__ == '__main__':
	main()

