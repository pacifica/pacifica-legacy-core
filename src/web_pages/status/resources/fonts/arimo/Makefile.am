EXTRA_DIST = \
Arimo-Bold-webfont.eot \
Arimo-Bold-webfont.svg \
Arimo-Bold-webfont.ttf \
Arimo-Bold-webfont.woff \
Arimo-BoldItalic-webfont.eot \
Arimo-BoldItalic-webfont.svg \
Arimo-BoldItalic-webfont.ttf \
Arimo-BoldItalic-webfont.woff \
Arimo-Italic-webfont.eot \
Arimo-Italic-webfont.svg \
Arimo-Italic-webfont.ttf \
Arimo-Italic-webfont.woff \
Arimo-Regular-webfont.eot \
Arimo-Regular-webfont.svg \
Arimo-Regular-webfont.ttf \
Arimo-Regular-webfont.woff \
arimo.css

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/ ; \
	done
