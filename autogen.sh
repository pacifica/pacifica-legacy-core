#!/bin/sh
libtoolize &&
aclocal -I m4 &&
automake --add-missing --copy --dist-ustar &&
autoconf --force &&
./configure $*
