EXTRA_DIST = \
cart_list_insert.html \
emsl_mgmt_view.php \
index.html \
single_item_view.php \
status_breadcrumb_insert_view.html \
status_error_page.html \
upload_item_view.html \
upload_item_view_backup.html \
welcome_message.php

SUBDIRS = \
pnnl_template

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/views/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/views/ ; \
	done
