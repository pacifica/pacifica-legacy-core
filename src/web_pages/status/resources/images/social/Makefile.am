EXTRA_DIST = \
facebook.png \
facebook.psd \
facebook@2x.png \
facebook@3x.png \
facebook_256.png \
flickr.png \
flickr.psd \
flickr@2x.png \
flickr@3x.png \
flickr_256.png \
googleplus.png \
googleplus.psd \
googleplus@2x.png \
googleplus@3x.png \
googleplus_256.png \
linkedin.png \
linkedin.psd \
linkedin@2x.png \
linkedin@3x.png \
linkedin_256.png \
social_sprites.png \
social_sprites@2x.png \
social_sprites@3x.png \
twitter.png \
twitter.psd \
twitter@2x.png \
twitter@3x.png \
twitter_256.png \
youtube.png \
youtube.psd \
youtube@2x.png \
youtube@3x.png \
youtube_256.png

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/social/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/social/ ; \
	done
