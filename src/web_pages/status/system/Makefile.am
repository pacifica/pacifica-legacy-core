EXTRA_DIST = \
index.html

SUBDIRS = \
core \
database \
fonts \
helpers \
language \
libraries

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/ ; \
	done
