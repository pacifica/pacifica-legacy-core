#!/bin/sh
libtoolize &&
aclocal -I m4 &&
automake --add-missing --copy --gnu &&
autoconf --force &&
./configure $*
