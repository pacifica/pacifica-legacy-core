EXTRA_DIST = \
icons.gif \
loading.gif \
ui.fancytree.css \
ui.fancytree.less \
ui.fancytree.min.css

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-win7/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-win7/ ; \
	done
