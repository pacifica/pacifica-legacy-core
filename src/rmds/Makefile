all: testdelete testread testmerge testcreate index.fcgi

JSON_CFLAGS=`pkg-config --cflags json`
JSON_LIBS=`pkg-config --libs json`

CFLAGS=-g -O0 -Wall -Werror

common.o: common.cpp common.h
	g++ -std=c++0x ${CFLAGS} -c common.cpp

testdelete.o: testdelete.cpp common.h
	g++ ${CFLAGS} -c testdelete.cpp

testdelete: testdelete.o common.o
	g++ -o testdelete testdelete.o common.o -lrados

testread.o: testread.cpp common.h
	g++ -std=c++0x ${CFLAGS} -c testread.cpp

testread: testread.o common.o
	g++ -o testread testread.o common.o -lrados

testmerge.o: testmerge.cpp common.h
	g++ -std=c++0x ${CFLAGS} ${JSON_CFLAGS} -c testmerge.cpp

testmerge: testmerge.o common.o
	g++ ${JSON_LIBS} -o testmerge testmerge.o common.o -lrados

testcreate.o: testcreate.cpp common.h
	g++ ${CFLAGS} -c testcreate.cpp

testcreate: testcreate.o common.o
	g++ -o testcreate testcreate.o common.o -lrados

fcgi.o: fcgi.c
	gcc ${JSON_CFLAGS} -o fcgi.o -c fcgi.c

index.fcgi: fcgi.o
	g++ ${JSON_LIBS} -o index.fcgi fcgi.o -lfcgi

clean:
	rm -f common.o testdelete.o testdelete testread.o testread testmerge testmerge.o testcreate testcreate.o fcgi.o index.fcgi
