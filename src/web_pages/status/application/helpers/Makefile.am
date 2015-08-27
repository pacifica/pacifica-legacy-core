EXTRA_DIST = \
file_info_helper.php \
item_helper.php \
myemsl_helper.php \
network_helper.php \
opwhse_search_helper.php \
time_helper.php \
user_helper.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/helpers/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/helpers/ ; \
	done
