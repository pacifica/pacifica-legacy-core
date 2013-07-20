outagedir = $(libexecdir)/myemsl/outage.d
outage_SCRIPTS = 49-fmds-writer 49-rmds-writer 49-tmds-writer 49-jmds-writer 50-fmds-versionclearer 50-rmds-versionclearer 50-tmds-versionclearer 50-jmds-versionclearer 51-rmds-recoverer 51-tmds-recoverer 51-fmds-recoverer 51-jmds-recoverer 52-tmds-trustifier 52-fmds-flattener 52-jmds-joiner

pkgcronhourlydir = $(sysconfdir)/cron.hourly
pkgcronhourly_SCRIPTS = pacifica_rmds_recoverer pacifica_tmds_recoverer pacifica_fmds_recoverer pacifica_jmds_recoverer

pkgmetadatadir = $(prefix)/share/pacifica/metadata/
pkgmetadata_DATA = rmds-recoverer-service-poke.ini tmds-recoverer-service-poke.ini fmds-recoverer-service-poke.ini jmds-recoverer-service-poke.ini

EXTRA_DIST = $(outage_SCRIPTS) $(pkgmetadata_DATA) $(pkgcronhourly_SCRIPTS)
