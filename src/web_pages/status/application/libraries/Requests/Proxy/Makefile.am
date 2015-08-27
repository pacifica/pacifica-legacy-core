EXTRA_DIST = \
HTTP.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Proxy/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Proxy/ ; \
	done
