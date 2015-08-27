EXTRA_DIST = \
README.md \
php_myemsl.ini \
index.php \
prototype.js \
refresh.js \
status_block_wide.png \
status_style.css

SUBDIRS = application system resources

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/ ; \
	done ; \
	$(mkinstalldirs) $(DESTDIR)/${sysconfdir}/php.d ; \
	$(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources ; \
	install -m 0644 php_myemsl.ini $(DESTDIR)/${sysconfdir}/php.d/
