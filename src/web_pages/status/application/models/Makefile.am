EXTRA_DIST = \
cart_model.php \
eus_model.php \
index.html \
myemsl_model.php \
navigation_info_model.php \
status_model.php \
user_operations_model.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/application/models/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/models/ ; \
	done
