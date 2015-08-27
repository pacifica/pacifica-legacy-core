EXTRA_DIST = \
footer.php \
globals.php \
intranet_banner.php \
leftnav.php \
modalbox_setup.php \
rightnav_search.php \
top.php \
view_footer.php \
view_footer_no_nav.php \
view_header.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/application/views/pnnl_template/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/views/pnnl_template/ ; \
	done
