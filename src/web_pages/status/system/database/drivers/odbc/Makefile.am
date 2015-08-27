EXTRA_DIST = \
index.html \
odbc_driver.php \
odbc_forge.php \
odbc_result.php \
odbc_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/odbc/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/odbc/ ; \
	done
