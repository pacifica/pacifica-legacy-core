EXTRA_DIST = \
index.html \
oci8_driver.php \
oci8_forge.php \
oci8_result.php \
oci8_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/oci8/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/oci8/ ; \
	done
