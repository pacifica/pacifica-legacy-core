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

install-am:
	for i in $(SUBDIRS) ; do \
	  mkdir -p $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/$$i ; \
	done ; \
	for i in $(EXTRA_DIST) ; do \
	  install -m 0644 $$i $(DESTDIR)/${pkgmyemslstatusdir}/system/database/drivers/ ; \
	done
