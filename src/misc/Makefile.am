ulmdir = $(libexecdir)/myemsl
ulm_SCRIPTS = itemauthgenkeys itemtokengen servergenkeys

dist-hook:
	rm -f $(distdir)/_myemsl_archive.py

programdir = $(libexecdir)/pacifica
program_PROGRAMS = daemonize2

daemonize2_SOURCES = daemonize.c

BUILT_SOURCES = archive-python.c _myemsl_archive.py
CLEANFILES = $(BUILT_SOURCES)
SWIG_SOURCES = archive.i

python_PYTHON = _myemsl_archive.py
pyexec_LTLIBRARIES = __myemsl_archive.la
__myemsl_archive_la_SOURCES = $(SWIG_SOURCES)
nodist__myemsl_archive_la_SOURCES = archive-python.c
__myemsl_archive_la_CPPFLAGS = $(PYTHON_CPPFLAGS) -I$(srcdir)
__myemsl_archive_la_LDFLAGS = -module
__myemsl_archive_la_LIBADD = -larchive

if DO_DIST_ONLY
archive-python.c:
	touch archive-python.c
	touch _myemsl_archive.py
else
archive-python.c: $(SWIG_SOURCES)
	$(SWIG) -python -I$(srcdir) -I/usr/include -o $@ $<
endif

_myemsl_archive.py: archive-python.c

EXTRA_DIST = $(ulm_SCRIPTS)
