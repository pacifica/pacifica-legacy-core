EXTRA_DIST = \
Auth.php \
Cookie.php \
Exception.php \
Hooker.php \
Hooks.php \
IDNAEncoder.php \
IPv6.php \
IRI.php \
Proxy.php \
Response.php \
SSL.php \
Session.php \
Transport.php

SUBDIRS = \
Auth \
Cookie \
Exception \
Proxy \
Response \
Transport \
Utility

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/ ; \
	done
