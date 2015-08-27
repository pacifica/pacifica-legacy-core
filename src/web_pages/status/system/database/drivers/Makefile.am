EXTRA_DIST = \
index.html

SUBDIRS = \
cubrid \
mssql \
mysql \
mysqli \
oci8 \
odbc \
pdo \
postgre \
sqlite \
sqlsrv

installdirs-am:
	for i in $(SUBDIRS) ; do \
	  $(mkinstalldirs) $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/$$i ; \
	done
install-am:
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/ ; \
	done
