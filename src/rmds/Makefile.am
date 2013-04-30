webfcgidir = $(pkgmyemslwebrootdir)/fcgi-bin
webfcgi_PROGRAMS = rmds.fcgi

noinst_PROGRAMS = testdelete testread testmerge testcreate env.fcgi

lib_LTLIBRARIES = libpacifica_rmds.la

libpacifica_rmds_la_SOURCES = common.cpp
libpacifica_rmds_la_LDFLAGS = $(JSON_LIBS) $(LIBRADOS_LIBS)
libpacifica_rmds_la_CXXFLAGS = -std=c++0x

INCLUDES = $(JSON_CFLAGS)

testdelete_SOURCES = testdelete.cpp common.h
testdelete_LDADD = libpacifica_rmds.la

testread_SOURCES = testread.cpp common.h
testread_LDADD = libpacifica_rmds.la

testcreate_SOURCES = testcreate.cpp common.h
testcreate_LDADD = libpacifica_rmds.la

testmerge_SOURCES = testmerge.cpp common.h
testmerge_LDADD = libpacifica_rmds.la

rmds_fcgi_SOURCES = rmds.cpp common.h
rmds_fcgi_LDADD = libpacifica_rmds.la $(FCGI_LIBS)

env_fcgi_SOURCES = env.c
env_fcgi_LDADD = $(FCGI_LIBS) $(JSON_LIBS)
