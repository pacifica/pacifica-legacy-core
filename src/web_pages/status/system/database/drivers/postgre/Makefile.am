EXTRA_DIST = \
index.html \
postgre_driver.php \
postgre_forge.php \
postgre_result.php \
postgre_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/postgre/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/postgre/ ; \
	done
