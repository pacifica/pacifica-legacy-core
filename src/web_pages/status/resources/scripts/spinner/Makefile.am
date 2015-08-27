EXTRA_DIST = \
spin.min.js

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/spinner/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/spinner/ ; \
	done
