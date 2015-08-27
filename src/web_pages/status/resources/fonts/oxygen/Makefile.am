EXTRA_DIST = \
Oxygen-Bold-webfont.eot \
Oxygen-Bold-webfont.svg \
Oxygen-Bold-webfont.ttf \
Oxygen-Bold-webfont.woff \
Oxygen-BoldItalic-webfont.eot \
Oxygen-BoldItalic-webfont.svg \
Oxygen-BoldItalic-webfont.ttf \
Oxygen-BoldItalic-webfont.woff \
Oxygen-Italic-webfont.eot \
Oxygen-Italic-webfont.svg \
Oxygen-Italic-webfont.ttf \
Oxygen-Italic-webfont.woff \
Oxygen-webfont.eot \
Oxygen-webfont.svg \
Oxygen-webfont.ttf \
Oxygen-webfont.woff \
demo.html \
oxygen.css \
stylesheet.css

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/oxygen/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/oxygen/ ; \
	done
