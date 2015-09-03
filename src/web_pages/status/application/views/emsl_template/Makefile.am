EXTRA_DIST = \
globals.php \
intranet_banner.php \
top.php \
view_footer.php \
view_footer_short.php \
view_footer_old.php \
view_header.php

SUBDIRS = 

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/views/emsl_template/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/views/emsl_template/ ; \
	done
