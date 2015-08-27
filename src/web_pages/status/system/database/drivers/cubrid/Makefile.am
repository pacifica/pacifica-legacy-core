EXTRA_DIST = \
cubrid_driver.php \
cubrid_forge.php \
cubrid_result.php \
cubrid_utility.php \
index.html

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/cubrid/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/cubrid/ ; \
	done
