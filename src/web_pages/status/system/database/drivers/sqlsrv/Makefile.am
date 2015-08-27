EXTRA_DIST = \
index.html \
sqlsrv_driver.php \
sqlsrv_forge.php \
sqlsrv_result.php \
sqlsrv_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/sqlsrv/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/sqlsrv/ ; \
	done
