EXTRA_DIST = \
index.html \
Benchmark.php \
CodeIgniter.php \
Common.php \
Config.php \
Controller.php \
Exceptions.php \
Hooks.php \
Input.php \
Lang.php \
Loader.php \
Model.php \
Output.php \
Router.php \
Security.php \
URI.php \
Utf8.php

SUBDIRS =

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/core/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/core/ ; \
	done
