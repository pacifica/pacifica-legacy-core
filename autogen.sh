#!/bin/sh
libtoolize &&
aclocal -I m4 &&
automake --add-missing --copy &&
autoconf --force &&
./configure $*
