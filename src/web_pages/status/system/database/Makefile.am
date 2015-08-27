EXTRA_DIST = \
index.html \
DB.php \
DB_active_rec.php \
DB_cache.php \
DB_driver.php \
DB_forge.php \
DB_result.php \
DB_utility.php

SUBDIRS = \
drivers

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/ ; \
	done
