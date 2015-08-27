EXTRA_DIST = \
index.html \
jquery-ui.css \
jquery-ui.js \
jquery-ui.min.css \
jquery-ui.min.js \
jquery-ui.structure.css \
jquery-ui.structure.min.css \
jquery-ui.theme.css \
jquery-ui.theme.min.css

SUBDIRS = \
external \
images

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-ui/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-ui/ ; \
	done
