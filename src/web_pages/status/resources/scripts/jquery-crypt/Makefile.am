EXTRA_DIST = \
jquery.crypt.js

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-crypt/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-crypt/ ; \
	done
