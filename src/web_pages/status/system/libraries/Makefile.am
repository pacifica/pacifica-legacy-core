EXTRA_DIST = \
index.html \
Calendar.php \
Cart.php \
Driver.php \
Email.php \
Encrypt.php \
Form_validation.php \
Ftp.php \
Image_lib.php \
Javascript.php \
Log.php \
Migration.php \
Pagination.php \
Parser.php \
Profiler.php \
Session.php \
Sha1.php \
Table.php \
Trackback.php \
Typography.php \
Unit_test.php \
Upload.php \
User_agent.php \
Xmlrpc.php \
Xmlrpcs.php \
Zip.php

SUBDIRS = \
javascript

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/libraries/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/libraries/ ; \
	done
