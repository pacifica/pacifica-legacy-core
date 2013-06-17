SUBDIRS = receivers

pkginitd_SCRIPTS = notification-service
sbin_SCRIPTS = emsl-notify

pkgexecdir = $(libexecdir)/pacifica/notification
pkgexec_SCRIPTS = init receiver writer recoverer versionclearer_init writer_init recoverer_init

EXTRA_DIST = email.sh filelist.xslt hadoop.sh start.sh filestream \
             hostname.sh test.sh expresso.sh hadoop_copy.py nwchem.sh \
             $(pkginitd_SCRIPTS) $(sbin_SCRIPTS) $(pkgexec_SCRIPTS)
