bin_PROGRAMS = myemsl_nagios_rmtrans

INCLUDES = $(GLIB_CFLAGS) $(EXTRA_CFLAGS) -DSVNVER=\"`$(top_srcdir)/svnver.sh $(top_srcdir)`\" -DSVNBRANCH=\"`$(top_srcdir)/svnbranch.sh $(top_srcdir)`\"

myemsl_nagios_rmtrans_SOURCES = myemsl_nagios_rmtrans.c
myemsl_nagios_rmtrans_LDFLAGS = $(GLIB_LIBS)

mountdir = $(libexecdir)/myemsl/mount.d
mount_SCRIPTS = 50-nagios

nagdir = $(libdir)/nagios/plugins
nag_DATA = check_myemsl_upload check_myemsl_upload_status

nagdatadir = $(prefix)/lib/myemsl/nagios
nagdata_DATA = nagios_test.tar

install-exec-hook:
	chmod u+s $(DESTDIR)$(bindir)/myemsl_nagios_rmtrans

EXTRA_DIST = check_myemsl_upload check_myemsl_upload_status nagios_test.tar 50-nagios
