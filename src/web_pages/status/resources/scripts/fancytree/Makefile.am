EXTRA_DIST = \
jquery.fancytree-all.js \
jquery.fancytree-all.min.js \
jquery.fancytree.js \
jquery.fancytree.min.js

SUBDIRS = \
skin-awesome \
skin-bootstrap \
skin-bootstrap-n \
skin-lion \
skin-themeroller \
skin-vista \
skin-win7 \
skin-win8 \
skin-win8-n \
skin-win8-xxl \
skin-xp \
src

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/ ; \
	done
