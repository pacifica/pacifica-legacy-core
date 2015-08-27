EXTRA_DIST = \
index.html \
sqlite_driver.php \
sqlite_forge.php \
sqlite_result.php \
sqlite_utility.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/sqlite/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/sqlite/ ; \
	done
