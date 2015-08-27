EXTRA_DIST = \
icons.gif \
loading.gif \
ui.fancytree.css \
ui.fancytree.less \
ui.fancytree.min.css

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-vista/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-vista/ ; \
	done
