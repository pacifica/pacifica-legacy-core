def brand(type, writer):
	incfile = open("/var/www/myemsl/brand/brand_%s.inc" %(type), 'r')
	writer.write(incfile.read())
	incfile.close()
