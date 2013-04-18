ulmdir = $(libexecdir)/myemsl
ulm_SCRIPTS = itemauthgenkeys itemtokengen servergenkeys

BUILT_SOURCES = archive-python.c _myemsl_archive.py
CLEANFILES = $(BUILT_SOURCES)
SWIG_SOURCES = archive.i

python_PYTHON = _myemsl_archive.py
pyexec_LTLIBRARIES = __myemsl_archive.la
__myemsl_archive_la_SOURCES = archive-python.c $(SWIG_SOURCES)
__myemsl_archive_la_CPPFLAGS = $(PYTHON_CPPFLAGS) -I$(srcdir)
__myemsl_archive_la_LDFLAGS = -module
__myemsl_archive_la_LIBADD = -larchive

archive-python.c: $(SWIG_SOURCES)
	$(SWIG) -python -I$(srcdir) -I/usr/include -o $@ $<

_myemsl_archive.py: archive-python.c

EXTRA_DIST = $(ulm_SCRIPTS)
