EXTRA_DIST = \
SourceSansPro-Black-webfont.eot \
SourceSansPro-Black-webfont.svg \
SourceSansPro-Black-webfont.ttf \
SourceSansPro-Black-webfont.woff \
SourceSansPro-BlackIt-webfont.eot \
SourceSansPro-BlackIt-webfont.svg \
SourceSansPro-BlackIt-webfont.ttf \
SourceSansPro-BlackIt-webfont.woff \
SourceSansPro-Bold-webfont.eot \
SourceSansPro-Bold-webfont.svg \
SourceSansPro-Bold-webfont.ttf \
SourceSansPro-Bold-webfont.woff \
SourceSansPro-BoldIt-webfont.eot \
SourceSansPro-BoldIt-webfont.svg \
SourceSansPro-BoldIt-webfont.ttf \
SourceSansPro-BoldIt-webfont.woff \
SourceSansPro-ExtraLight-webfont.eot \
SourceSansPro-ExtraLight-webfont.svg \
SourceSansPro-ExtraLight-webfont.ttf \
SourceSansPro-ExtraLight-webfont.woff \
SourceSansPro-ExtraLightIt-webfont.eot \
SourceSansPro-ExtraLightIt-webfont.svg \
SourceSansPro-ExtraLightIt-webfont.ttf \
SourceSansPro-ExtraLightIt-webfont.woff \
SourceSansPro-It-webfont.eot \
SourceSansPro-It-webfont.svg \
SourceSansPro-It-webfont.ttf \
SourceSansPro-It-webfont.woff \
SourceSansPro-Light-webfont.eot \
SourceSansPro-Light-webfont.svg \
SourceSansPro-Light-webfont.ttf \
SourceSansPro-Light-webfont.woff \
SourceSansPro-LightIt-webfont.eot \
SourceSansPro-LightIt-webfont.svg \
SourceSansPro-LightIt-webfont.ttf \
SourceSansPro-LightIt-webfont.woff \
SourceSansPro-Regular-webfont.eot \
SourceSansPro-Regular-webfont.svg \
SourceSansPro-Regular-webfont.ttf \
SourceSansPro-Regular-webfont.woff \
SourceSansPro-Semibold-webfont.eot \
SourceSansPro-Semibold-webfont.svg \
SourceSansPro-Semibold-webfont.ttf \
SourceSansPro-Semibold-webfont.woff \
SourceSansPro-SemiboldIt-webfont.eot \
SourceSansPro-SemiboldIt-webfont.svg \
SourceSansPro-SemiboldIt-webfont.ttf \
SourceSansPro-SemiboldIt-webfont.woff \
demo.html \
sourcesanspro.css \
stylesheet.css

SUBDIRS = 

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/sourcesanspro/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/fonts/sourcesanspro/ ; \
	done
