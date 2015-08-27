EXTRA_DIST = \
icons-rtl.gif \
icons.gif \
loading.gif \
ui.fancytree.css \
ui.fancytree.less \
ui.fancytree.min.css \
vline-rtl.gif \
vline.gif

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-xp/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/skin-xp/ ; \
	done
