pkglibexecdir = $(libexecdir)/myemsl
pkglibexec_SCRIPTS = cart_process2 cartd_child cartd_worker
pkglibexec_PROGRAMS = cartd

pkgdata_DATA =  cartd-service-poke.ini

mountdir = $(libexecdir)/myemsl/mount.d
mount_SCRIPTS = 75-amalgam

outagedir = $(libexecdir)/myemsl/outage.d
outage_SCRIPTS = 50-cartd

pkgcronhourlydir = $(sysconfdir)/cron.hourly
pkgcronhourly_SCRIPTS = myemsl_cart_process

EXTRA_DIST = $(pkglibexec_SCRIPTS) $(pkgdata_DATA) $(mount_SCRIPTS) $(outage_SCRIPTS) $(pkgcronhourly_SCRIPTS)

INCLUDES = $(EXTRA_CFLAGS) -DSVNVER=\"`$(top_srcdir)/svnver.sh $(top_srcdir)`\" -DSVNBRANCH=\"`$(top_srcdir)/svnbranch.sh $(top_srcdir)`\"

cartd_SOURCES = main.c
cartd_LDFLAGS = $(EXTRA_LIBS)
