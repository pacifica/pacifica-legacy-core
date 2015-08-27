EXTRA_DIST = \
files_156858.json \
ingest_states_group_156858.json \
instrument_group_list.json \
transactions_156858.json

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/json_files/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/json_files/ ; \
	done
