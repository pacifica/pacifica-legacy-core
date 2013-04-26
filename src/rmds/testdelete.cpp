#include <string.h>

#include "common.h"

int main(int argc, char *argv[])
{
	int res = 0;
	rados_ioctx_t io;
	int err;
	rados_t cluster;
	common_setup(argv[0], cluster, io);
	err = rados_remove(io, "1");
	if(err < 0)
	{
		fprintf(stderr, "%s: cannot delete key %s: %s\n", argv[0], "1", strerror(-err));
		res = 1;
	}
	common_cleanup(argv[0], cluster, io);
	return res;
}
