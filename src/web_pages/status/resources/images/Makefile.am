EXTRA_DIST = \
Cassette-44px_skewed.png \
Cassette-black-32px_skewed.png \
Cassette-black-44px.png \
cassette-check-combo.png \
disclosure_sprite.gif \
disclosure_sprite.png \
disclosure_sprite@2x.png \
disclosure_sprite@3x.png \
document-16.png \
doe_seal_plus_name.png \
doe_seal_plus_name@2x.png \
empty_folder_32.png \
footer_tagline.png \
footer_tagline@2x.png \
intranet_bg.png \
intranet_bg@2x.png \
intranet_nav_bg.png \
orange_folder-16.png \
orange_folder-22.png \
orange_folder-64.png \
pnnl_logo_battelle.png \
pnnl_logo_battelle@2x.png \
reveal_arrow_down.png \
reveal_arrow_up.png \
s.gif \
spinner-16x16_green.gif \
spinner-32x32.gif \
spinner-32x32_black.gif \
spinner-32x32_green.gif

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/ ; \
	done
