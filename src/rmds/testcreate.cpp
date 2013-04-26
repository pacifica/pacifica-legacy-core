#include <string>

#include "common.h"

int main(int argc, char *argv[])
{
	int err;
	int res = 0;
	long version = 1;
	char key[] = "1";
	char data[] = "{\"hello_thingy\":\"b\"}";
	rados_t cluster;
	rados_ioctx_t io;
	common_setup(argv[0], cluster, io);
	err = atomic_create_data(io, key, data, strlen(data), version);
	if(err < 0)
	{
		fprintf(stderr, "%s: failed to perform op on key %s. %s\n", argv[0], key, strerror(-err));
		res = 1;
	}
	common_cleanup(argv[0], cluster, io);
	return res;
}
