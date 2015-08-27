EXTRA_DIST = \
jquery-1.11.2.js \
jquery-1.11.2.min.js \
jquery-1.11.2.min.map \
jquery-1.9.1.js \
jquery-1.9.1.min.js \
jquery.min.map

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery/ ; \
	done
