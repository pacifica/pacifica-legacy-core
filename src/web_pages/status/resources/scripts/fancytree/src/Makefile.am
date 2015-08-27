EXTRA_DIST = \
jquery.fancytree.childcounter.js \
jquery.fancytree.clones.js \
jquery.fancytree.columnview.js \
jquery.fancytree.debug.js \
jquery.fancytree.dnd.js \
jquery.fancytree.edit.js \
jquery.fancytree.filter.js \
jquery.fancytree.glyph.js \
jquery.fancytree.gridnav.js \
jquery.fancytree.js \
jquery.fancytree.menu.js \
jquery.fancytree.persist.js \
jquery.fancytree.table.js \
jquery.fancytree.themeroller.js \
jquery.fancytree.wide.js

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/src/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/fancytree/src/ ; \
	done
