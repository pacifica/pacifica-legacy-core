EXTRA_DIST = \
expected_inputs_spec.js \
format_date_spec.js \
format_parse_date_spec.js \
format_pretty_date_spec.js \
issues_spec.js

SUBDIRS = \
vendor

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/test/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/test/ ; \
	done
