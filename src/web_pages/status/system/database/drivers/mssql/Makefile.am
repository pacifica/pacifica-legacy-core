EXTRA_DIST = \
index.html \
mssql_driver.php \
mssql_forge.php \
mssql_result.php \
mssql_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mssql/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mssql/ ; \
	done
