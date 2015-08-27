EXTRA_DIST = \
index.html \
calendar_lang.php \
date_lang.php \
db_lang.php \
email_lang.php \
form_validation_lang.php \
ftp_lang.php \
imglib_lang.php \
migration_lang.php \
number_lang.php \
profiler_lang.php \
unit_test_lang.php \
upload_lang.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/language/english/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/language/english/ ; \
	done
