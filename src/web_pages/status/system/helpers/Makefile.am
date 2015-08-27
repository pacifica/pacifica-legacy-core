EXTRA_DIST = \
index.html \
array_helper.php \
captcha_helper.php \
cookie_helper.php \
date_helper.php \
directory_helper.php \
download_helper.php \
email_helper.php \
file_helper.php \
form_helper.php \
html_helper.php \
inflector_helper.php \
language_helper.php \
number_helper.php \
path_helper.php \
security_helper.php \
smiley_helper.php \
string_helper.php \
text_helper.php \
typography_helper.php \
url_helper.php \
xml_helper.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/helpers/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/helpers/ ; \
	done
