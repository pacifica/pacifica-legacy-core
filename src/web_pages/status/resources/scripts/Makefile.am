EXTRA_DIST = \
emsl_mgmt_view.js \
generic-finder.js \
moment.min.js \
myemsl_file_download.js \
single_item_view.js \
status_common.js \
utility_functions.js

SUBDIRS = \
fancytree \
jquery \
jquery-cookie \
jquery-crypt \
jquery-dateFormat \
jquery-ui \
select2 \
spinner

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/ ; \
	done
