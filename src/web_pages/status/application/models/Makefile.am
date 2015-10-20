EXTRA_DIST = \
api_model.php \
cart_model.php \
eus_model.php \
myemsl_model.php \
navigation_info_model.php \
status_model.php \
user_operations_model.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/models/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/models/ ; \
	done
