EXTRA_DIST = \
emsl_chrome.css \
emsl_style.css \
upload_style.css \
bread_crumbs.css \
file_directory_styling.css \
local.css \
status.css \
status_style.css \
status_block_wide.png

SUBDIRS = \
shared

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/stylesheets/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/stylesheets/ ; \
	done
