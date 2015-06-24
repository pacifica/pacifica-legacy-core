bin_PROGRAMS = myemsl_mkstagedir

pkgmyemslcgi_PROGRAMS = finish preallocate status

INCLUDES = $(GLIB_CFLAGS) $(EXTRA_CFLAGS) -DSVNVER=\"`$(top_srcdir)/svnver.sh $(top_srcdir)`\" -DSVNBRANCH=\"`$(top_srcdir)/svnbranch.sh $(top_srcdir)`\"

myemsl_mkstagedir_SOURCES = myemsl_mkstagedir.c
myemsl_mkstagedir_LDFLAGS = $(GLIB_LIBS)

preallocate_SOURCES = preallocate.c
preallocate_LDFLAGS = $(GLIB_LIBS)

finish_SOURCES = finish.c
finish_LDFLAGS = $(GLIB_LIBS)

status_SOURCES = status.c
status_LDFLAGS = $(GLIB_LIBS)

install-exec-hook:
	chmod u+s $(DESTDIR)$(bindir)/myemsl_mkstagedir
	$(mkdir_p) $(DESTDIR)$(localstatedir)/www/myemsl/staging
