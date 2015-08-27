EXTRA_DIST = \
OpenSans-Bold-webfont.eot \
OpenSans-Bold-webfont.ttf \
OpenSans-Bold-webfont.woff \
OpenSans-BoldItalic-webfont.eot \
OpenSans-BoldItalic-webfont.ttf \
OpenSans-BoldItalic-webfont.woff \
OpenSans-ExtraBold-webfont.eot \
OpenSans-ExtraBold-webfont.ttf \
OpenSans-ExtraBold-webfont.woff \
OpenSans-ExtraBoldItalic-webfont.eot \
OpenSans-ExtraBoldItalic-webfont.ttf \
OpenSans-ExtraBoldItalic-webfont.woff \
OpenSans-Italic-webfont.eot \
OpenSans-Italic-webfont.ttf \
OpenSans-Italic-webfont.woff \
OpenSans-Light-webfont.eot \
OpenSans-Light-webfont.ttf \
OpenSans-Light-webfont.woff \
OpenSans-LightItalic-webfont.eot \
OpenSans-LightItalic-webfont.ttf \
OpenSans-LightItalic-webfont.woff \
OpenSans-Regular-webfont.eot \
OpenSans-Regular-webfont.ttf \
OpenSans-Regular-webfont.woff \
OpenSans-Semibold-webfont.eot \
OpenSans-Semibold-webfont.ttf \
OpenSans-Semibold-webfont.woff \
OpenSans-SemiboldItalic-webfont.eot \
OpenSans-SemiboldItalic-webfont.ttf \
OpenSans-SemiboldItalic-webfont.woff \
demo.html \
open-sans-fontfacekit.zip \
opensans.css \
stylesheet.css

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/opensans/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/opensans/ ; \
	done
