EXTRA_DIST = \
dateFormat.js \
dateFormat.min.js \
jquery-dateFormat.js \
jquery-dateFormat.min.js

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/dist/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/dist/ ; \
	done
