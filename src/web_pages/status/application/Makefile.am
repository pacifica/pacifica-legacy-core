EXTRA_DIST = \
index.html

SUBDIRS = \
config \
controllers \
core \
errors \
helpers \
hooks \
language \
libraries \
models \
third_party \
views

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/ ; \
	done
