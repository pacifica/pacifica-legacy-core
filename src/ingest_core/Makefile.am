bin_PROGRAMS = myemsl_ingest myemsl_status
bin_SCRIPTS = myemsl_bundler

ingestdir = $(libexecdir)/myemsl/ingest
ingest_SCRIPTS = ingest_vni ingest_job status_vni

SUBDIRS = xslt

pkgcrondaily_SCRIPTS = myemsl-client.cron

INCLUDES = $(GLIB_CFLAGS) $(EXTRA_CFLAGS) -DSVNVER=\"`$(top_srcdir)/svnver.sh $(top_srcdir)`\" -DSVNBRANCH=\"`$(top_srcdir)/svnbranch.sh $(top_srcdir)`\"

mountdir = $(libexecdir)/myemsl/mount.d
mount_SCRIPTS = 25-ingest

outagedir = $(libexecdir)/myemsl/outage.d
outage_SCRIPTS = 50-slurm

EXTRA_DIST = 25-ingest $(bin_SCRIPTS) $(ingest_SCRIPTS) $(pkgcrondaily_SCRIPTS) $(outage_SCRIPTS)

myemsl_status_SOURCES = myemsl_status.c
myemsl_status_LDFLAGS = $(GLIB_LIBS)

myemsl_ingest_SOURCES = myemsl_ingest.c
myemsl_ingest_LDFLAGS = $(GLIB_LIBS)

install-exec-hook:
	chmod u+s $(DESTDIR)$(bindir)/myemsl_ingest
	chmod u+s $(DESTDIR)$(bindir)/myemsl_status
