INCLUDES = $(FUSE_CFLAGS) $(GLIB_CFLAGS) $(EXTRA_CFLAGS) -DSVNVER=\"`$(top_srcdir)/svnver.sh $(top_srcdir)`\" -DSVNBRANCH=\"`$(top_srcdir)/svnbranch.sh $(top_srcdir)`\"

lib_LTLIBRARIES = libfusemod_myemslauth.la

libfusemod_myemslauth_la_SOURCES = myemslauth.c
libfusemod_myemslauth_la_LDFLAGS = -module $(FUSE_LIBS)
