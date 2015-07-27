AC_INIT([myemsl],[2.1.99],[Kevin.Fox@pnl.gov])
AM_INIT_AUTOMAKE([tar-ustar])
AC_CONFIG_SRCDIR([configure.ac])

AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE

AC_PROG_CC
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_LIBTOOL
AC_PROG_CXX

AC_ARG_ENABLE([dist-only],
        AS_HELP_STRING([--enable-dist-only],[Don't check requirements. Only for building releases.]),
        [
                do_dist_only=yes;
		export GLIB_CFLAGS="-I.";
		export GLIB_LIBS="-L.";
	],do_dist_only=no)
AM_CONDITIONAL(DO_DIST_ONLY, test x"$do_dist_only" = "xyes")

if [[ x"$do_dist_only" != "xyes" ]]; then

AM_PATH_PYTHON

AX_PKG_SWIG(1.3.0, [], [ AC_MSG_ERROR([SWIG is required to build..]) ])
AX_SWIG_PYTHON

PKG_CHECK_MODULES([FUSE],[fuse >= 2.7.0])
PKG_CHECK_MODULES([GLIB],[glib-2.0])

AC_ARG_WITH([rmds], AS_HELP_STRING([--with-rmds], [Build with the Raw MDS]))

AS_IF([test "x$with_rmds" = "xyes"], [
	PKG_CHECK_MODULES([JSON],[json])
	AC_CHECK_HEADER(fcgiapp.h, , [AC_MSG_ERROR([Couldn't find fcgiapp.h...you must install fcgi])])
	AC_CHECK_HEADER(rados/librados.h, , [AC_MSG_ERROR([Could not find librados. Please install ceph])])
	LIBRADOS_CFLAGS=""
	LIBRADOS_LIBS="-lrados"
	FCGI_CFLAGS=""
	FCGI_LIBS="-lfcgi"
	AC_SUBST(LIBRADOS_CFLAGS)
	AC_SUBST(LIBRADOS_LIBS)
	AC_SUBST(FCGI_CFLAGS)
	AC_SUBST(FCGI_LIBS)
	AC_PROG_CXX
])

PACKAGE_NAME=AC_PACKAGE_NAME
AC_SUBST(PACKAGE_NAME)

AC_ARG_WITH(python, AS_HELP_STRING([--with-python=FULLPATH], [use specific python given]), PYTHON="$withval", PYTHON="python")
AC_CHECK_PROG([PYTHON], $PYTHON, , python)
PYTHON_CPPFLAGS=-I`$PYTHON -c 'import distutils.sysconfig ; print distutils.sysconfig.get_config_var("INCLUDEDIR")+"/python"+distutils.sysconfig.get_config_var("VERSION")'`
PYTHON_CFLAGS=`$PYTHON -c 'import distutils.sysconfig ; print distutils.sysconfig.get_config_var("CFLAGS")'`
PYTHON_LDFLAGS=`$PYTHON -c 'import distutils.sysconfig ; print distutils.sysconfig.get_config_var("LIBS")+" -lpython"+distutils.sysconfig.get_config_var("VERSION")'`
PYTHON_VERSION=`$PYTHON -c 'import distutils.sysconfig ; print distutils.sysconfig.get_config_var("VERSION")'`

AC_SUBST(PYTHON_CFLAGS)
AC_SUBST(PYTHON_CPPFLAGS)
AC_SUBST(PYTHON_LDFLAGS)

PYTHON_LIBDIR="\"$libdir/python$PYTHON_VERSION/site-packages\""
AC_DEFINE_UNQUOTED(PYTHON_LIBDIR, $PYTHON_LIBDIR, [local python module specific dir.])

TMPCFLAGS="$CFLAGS"
CFLAGS+=" $FUSE_CFLAGS"
AC_CHECK_MEMBERS([struct fuse_operations.flag_nullpath_ok], [NULLPATH=1;WITH_FUSE_NULLPATH=" -DWITH_FUSE_NULLPATH"], [NULLPATH=0;WITH_FUSE_NULLPATH=""], [
#define FUSE_USE_VERSION 26
#include<fuse.h>
])
CFLAGS="$TMPCFLAGS $WITH_FUSE_NULLPATH"
AC_SUBST(NULLPATH)

fi
AM_CONDITIONAL([WITH_RMDS], [test "x$with_rmds" != "x"])

#
# config directories in /etc we care about
#
pkgcrondailydir=${sysconfdir}/cron.daily
AC_SUBST(pkgcrondailydir)
pkgcronhourlydir=${sysconfdir}/cron.hourly
AC_SUBST(pkgcronhourlydir)
pkgmyemslconfdir=${sysconfdir}/myemsl
AC_SUBST(pkgmyemslconfdir)
pkghttpconfdir=${sysconfdir}/httpd/conf.d
AC_SUBST(pkghttpconfdir)
pkginitddir=${sysconfdir}/init.d
AC_SUBST(pkginitddir)


#
# myemsl data files out in lib/myemsl
#
pkgmyemsldir=${prefix}/lib/myemsl
AC_SUBST(pkgmyemsldir)
pkgapachedir=${pkgmyemsldir}/apache
AC_SUBST(pkgapachedir)
pkgmyemslwebdir=${pkgapachedir}/myemsl.d
AC_SUBST(pkgmyemslwebdir)
pkgmyemsloutagedsstpdir=${pkgapachedir}/outage.d/sstp.d
AC_SUBST(pkgmyemsloutagedsstpdir)
pkgmyemslssldir=${pkgapachedir}/myemsl-ssl.d
AC_SUBST(pkgmyemslssldir)
pkgmyemsloutagedir=${pkgapachedir}/outage.d
AC_SUBST(pkgmyemsloutagedir)
pkgpgsqldir=${pkgmyemsldir}/pgsql_schema
AC_SUBST(pkgpgsqldir)
pkgwsgidir=${pkgmyemsldir}/wsgi-scripts
AC_SUBST(pkgwsgidir)

#
# www data files out in web root
#
pkgmyemslwebrootdir=${localstatedir}/www/myemsl
AC_SUBST(pkgmyemslwebrootdir)
pkgmyemslstagingdir=${pkgmyemslwebrootdir}/staging
AC_SUBST(pkgmyemslstagingdir)
pkgmyemsleusdir=${pkgmyemslwebrootdir}/eus
AC_SUBST(pkgmyemsleusdir)
pkgmyemsltestauthdir=${pkgmyemslwebrootdir}/testauth
AC_SUBST(pkgmyemsltestauthdir)
pkgmyemslnopersoniddir=${pkgmyemslwebrootdir}/error/nopersonid
AC_SUBST(pkgmyemslnopersoniddir)
pkgmyemslsampleingestdir=${pkgmyemslwebrootdir}/sample-ingest
AC_SUBST(pkgmyemslsampleingestdir)
pkgmyemslresourcesdir=${localstatedir}/www
AC_SUBST(pkgmyemslresourcesdir)
pkgmyemslstatusdir=${pkgmyemslwebrootdir}/status
AC_SUBST(pkgmyemslstatusdir)
pkgmyemslcgidir=${pkgmyemslwebrootdir}/cgi-bin
AC_SUBST(pkgmyemslcgidir)
pkgmyemslpreferencesdir=${pkgmyemslwebrootdir}/preferences
AC_SUBST(pkgmyemslpreferencesdir)
pkgmyemslpreferencesscriptsdir=${pkgmyemslwebrootdir}/preferences/scripts
AC_SUBST(pkgmyemslpreferencesscriptsdir)
pkgmyemslsimplesearchdir=${pkgmyemslwebrootdir}/search/simple
AC_SUBST(pkgmyemslsimplesearchdir)
pkgmyemslproposalfinderdir=${pkgmyemslwebrootdir}/proposal-finder
AC_SUBST(pkgmyemslproposalfinderdir)
pkgmyemslstaticdatadir=${pkgmyemslwebrootdir}/static
AC_SUBST(pkgmyemslstaticdatadir)
pkgmyemslwebapidir=${pkgmyemslwebrootdir}/api
AC_SUBST(pkgmyemslwebapidir)

AC_OUTPUT([
		Makefile
		src/Makefile
		src/web_pages/Makefile
		src/web_pages/error/Makefile
		src/web_pages/error/nopersonid/Makefile
		src/web_pages/sample-ingest/Makefile
		src/web_pages/preferences/Makefile
		src/web_pages/preferences/scripts/Makefile
		src/web_pages/search/Makefile
		src/web_pages/search/simple/Makefile
		src/web_pages/status/Makefile
		src/web_pages/static/Makefile
		src/web_pages/static/1/Makefile
		src/web_pages/static/1/icons/Makefile
		src/web_pages/api/Makefile
		src/web_pages/api/1/Makefile
		src/web_pages/api/1/elasticsearch/Makefile
		src/web_pages/admin/Makefile
		src/web_pages/admin/cart/Makefile
		src/web_pages/admin/switchuser/Makefile
		src/web_pages/proposal-finder/Makefile
		src/web_pages/publication/Makefile
		src/web_pages/test/Makefile
		src/web_pages/test/browser/Makefile
		src/web_pages/test/widgets/Makefile
		src/ingest_core/Makefile
		src/ingest_core/xslt/Makefile
		src/sstp/Makefile
		src/sumcheck/Makefile
		src/core/Makefile
		src/nagios/Makefile
		src/python/Makefile
		src/python/setup.py
		src/apache/Makefile
		src/apache/conf.d/Makefile
		src/apache/myemsl.d/Makefile
		src/apache/outage.d/Makefile
		src/apache/outage.d/sstp.d/Makefile
		src/apache/testauth/Makefile
		src/pgsql_schema/Makefile
		src/wsgi/Makefile
		src/notification/Makefile
		src/notification/receivers/Makefile
		src/metadata/Makefile
		src/cartd/Makefile
		src/examples/Makefile
		src/devel/Makefile
		src/misc/Makefile
		src/libexec/Makefile
		src/libexec/mount.d/Makefile
		src/elasticsearch/Makefile
		src/fuse-myemslauth/Makefile
		src/rmds/Makefile
		src/conf/Makefile
		docs/Makefile
		docs/format/Makefile
		docs/plugins/Makefile
		docs/protocols/Makefile
		docs/webapi/Makefile
		man/Makefile
		man/man1/Makefile
		man/man3/Makefile
		test/Makefile
		conf/Makefile
		pacifica.spec
])
