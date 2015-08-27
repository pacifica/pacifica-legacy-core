EXTRA_DIST = \
index.html

SUBDIRS = \
english

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/language/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/language/ ; \
	done
