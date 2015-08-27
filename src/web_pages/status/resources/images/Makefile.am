EXTRA_DIST = \
Cassette-44px_skewed.png \
Cassette-black-32px_skewed.png \
Cassette-black-44px.png \
ajax-loader.gif \
cancel_button_capture.png \
cassette-check-combo.png \
dc_sprites.png \
disclosure_sprite.gif \
disclosure_sprite.png \
disclosure_sprite@2x.png \
disclosure_sprite@3x.png \
document-16.png \
doe_seal_plus_name.png \
doe_seal_plus_name@2x.png \
down_arrow.png \
empty_folder_32.png \
emsl-doe_combined.png \
emsl-doe_combined@2x.png \
emsl-doe_combined@3x.png \
emsl_logo_white.png \
emsl_logo_white@2x.png \
emsl_logo_white@3x.png \
emsl_logo_white_new.png \
emsl_logo_white_new@2x.png \
emsl_logo_white_new@3x.png \
emsl_ticket_tracking_main_sm@2x.jpg \
emsl_white_notag.psd \
fader_block.png \
footer_tagline.png \
footer_tagline@2x.png \
intranet_bg.png \
intranet_bg@2x.png \
intranet_bg_l.png \
intranet_bg_l@2x.png \
intranet_bg_l@3x.png \
intranet_nav_bg.png \
menu-angle.png \
orange_folder-16.png \
orange_folder-22.png \
orange_folder-64.png \
pnnl_logo_battelle.jpg \
pnnl_logo_battelle.png \
pnnl_logo_battelle@2x.png \
pnnl_logo_battelle_2015.png \
pnnl_logo_battelle_2015@2x.png \
pnnl_logo_battelle_2015@3x.png \
pnnl_logo_battelle_alt_2015.png \
pnnl_logo_battelle_alt_2015@2x.png \
pnnl_logo_battelle_alt_2015@3x.png \
pnnl_swoosh.png \
pnnl_swoosh@2x.png \
pnnl_swoosh_2015.png \
pnnl_swoosh_2015@2x.png \
pnnl_swoosh_2015@3x.png \
reveal_arrow_down.png \
reveal_arrow_up.png \
s.gif \
search_button@2x.png \
search_button@3x.png \
spinner-16x16_green.gif \
spinner-32x32.gif \
spinner-32x32_black.gif \
spinner-32x32_green.gif

SUBDIRS = \
social

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslresourcesdir}/resources/images/ ; \
	done
