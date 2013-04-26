#include <rados/librados.hpp>
#include <string>

#include "common.h"

typedef struct {
	FILE *out;
	char *progname;
} callback_data;

void _document(const char *data, unsigned long size, long version, void *user_data)
{
	callback_data *cbd = (callback_data*)user_data;
	fwrite(data, size, 1, cbd->out);
	fprintf(cbd->out, "\nVersion: %ld\n", version);
}

void _error(const char *data, void *user_data)
{
	callback_data *cbd = (callback_data*)user_data;
	fprintf(stderr, "%s: %s\n", cbd->progname, data);
}

int main(int argc, char *argv[])
{
	int res = 0;
	rados_t cluster;
	rados_ioctx_t io;
	callback_data cbd;
	cbd.out = stdout;
	cbd.progname = argv[0];
	common_setup(argv[0], cluster, io);
	res = atomic_read_cb(io, "1", 1, _document, _error, &cbd);
	common_cleanup(argv[0], cluster, io);
	return res;
}
