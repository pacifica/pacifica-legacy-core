EXTRA_DIST = \
Gruntfile.js \
MIT-LICENSE.txt \
README.rdoc \
bower.json \
composer.json \
dateFormat.js \
dateFormat.min.js \
jquery-dateFormat.js \
jquery-dateFormat.min.js \
package.json

SUBDIRS = \
dist \
src \
test

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/scripts/jquery-dateFormat/ ; \
	done
