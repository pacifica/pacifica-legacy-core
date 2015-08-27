EXTRA_DIST = \
dateFormat.js \
dateFormat.min.js \
jquery-dateFormat.js \
jquery-dateFormat.min.js

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/dist/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/dist/ ; \
	done
