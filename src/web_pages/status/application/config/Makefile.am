EXTRA_DIST = \
autoload.php \
config.php \
constants.php \
database.php \
doctypes.php \
foreign_chars.php \
hooks.php \
migration.php \
mimes.php \
profiler.php \
routes.php \
smileys.php \
user_agents.php

SUBDIRS = \
database \
production

install-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/application/config/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/application/config/ ; \
	done
