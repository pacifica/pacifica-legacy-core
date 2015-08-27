EXTRA_DIST = \
index.html \
mysqli_driver.php \
mysqli_forge.php \
mysqli_result.php \
mysqli_utility.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mysqli/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/mysqli/ ; \
	done
