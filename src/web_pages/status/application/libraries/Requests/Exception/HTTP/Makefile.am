EXTRA_DIST = \
400.php \
401.php \
402.php \
403.php \
404.php \
405.php \
406.php \
407.php \
408.php \
409.php \
410.php \
411.php \
412.php \
413.php \
414.php \
415.php \
416.php \
417.php \
418.php \
428.php \
429.php \
431.php \
500.php \
501.php \
502.php \
503.php \
504.php \
505.php \
511.php \
Unknown.php

SUBDIRS =

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Exception/HTTP/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/libraries/Requests/Exception/HTTP/ ; \
	done
