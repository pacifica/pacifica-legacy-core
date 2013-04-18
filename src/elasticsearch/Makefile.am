etcsecuritylimitsddir = $(sysconfdir)/security/limits.d
etcsecuritylimitsd_DATA = 99-elasticsearch.conf

pkgdata_DATA = elasticsearch-service-poke.ini

initddir = $(sysconfdir)/init.d
initd_SCRIPTS = myemsl_elasticsearch

pkgcronhourlydir = $(sysconfdir)/cron.hourly
pkgcronhourly_SCRIPTS = myemsl_elasticsearch_sync

bin_SCRIPTS = myemsl_elasticsearch_sync

pkgexecdir = $(libexecdir)/myemsl
pkgexec_SCRIPTS = elasticsearch_sync

pkgfallbackdatadir = $(localstatedir)/lib/myemsl
pkgfallbackdata_DATA = dms.json

EXTRA_DIST = 99-elasticsearch.conf $(pkgdata_DATA) $(initd_SCRIPTS) $(pkgcronhourly_SCRIPTS) $(pkgexec_SCRIPTS) $(pkgfallbackdata_DATA)
