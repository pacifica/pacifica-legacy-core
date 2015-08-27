EXTRA_DIST = \
index.html \
pdo_driver.php \
pdo_forge.php \
pdo_result.php \
pdo_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/pdo/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/pdo/ ; \
	done
