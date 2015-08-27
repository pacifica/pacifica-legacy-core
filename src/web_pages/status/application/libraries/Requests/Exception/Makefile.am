EXTRA_DIST = \
HTTP.php

SUBDIRS = \
HTTP

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Exception/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Exception/ ; \
	done
