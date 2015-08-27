EXTRA_DIST = \
myemsl_status_site_info.sqlite

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/application/config/database/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/config/database/ ; \
	done
