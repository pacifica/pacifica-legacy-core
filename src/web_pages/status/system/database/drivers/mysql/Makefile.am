EXTRA_DIST = \
index.html \
mysql_driver.php \
mysql_forge.php \
mysql_result.php \
mysql_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mysql/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mysql/ ; \
	done
