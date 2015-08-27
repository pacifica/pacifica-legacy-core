EXTRA_DIST = \
jquery.cookie.js

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-cookie/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-cookie/ ; \
	done
