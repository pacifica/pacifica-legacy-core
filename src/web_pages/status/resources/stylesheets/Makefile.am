EXTRA_DIST = \
bread_crumbs.css \
file_directory_styling.css \
local.css \
status.css \
status_style.css \
status_block_wide.png

SUBDIRS = \
shared

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/stylesheets/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/stylesheets/ ; \
	done
