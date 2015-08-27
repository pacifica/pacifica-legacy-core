#!/bin/sh
case `uname` in Darwin*) glibtoolize --copy ;;
  *) libtoolize --copy ;; esac &&
aclocal -I m4 &&
automake --add-missing --copy --gnu &&
autoconf --force &&
./configure $*
