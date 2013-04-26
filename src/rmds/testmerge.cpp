#include <string>
#include <json.h>

#include "common.h"

typedef struct {
	FILE *out;
	char *progname;
	json_object *json;
	long version;
} callback_data;

static int _getdata(long version, writedata_cb writedata, void *wdcbd, void *user_data)
{
	callback_data *cbd = (callback_data*)user_data;
	const char *data;
	json_object_object_add(cbd->json, "version", json_object_new_int64(version));
	data = json_object_to_json_string_ext(cbd->json, JSON_C_TO_STRING_PLAIN);
	writedata(wdcbd, data, strlen(data));
	return 0;
}

void _document(const char *data, unsigned long size, long version, void *user_data)
{
	callback_data *cbd = (callback_data*)user_data;
	cbd->json = json_tokener_parse(data);
	cbd->version = version;
}

void _error(const char *data, void *user_data)
{
	callback_data *cbd = (callback_data*)user_data;
	fprintf(stderr, "%s: %s\n", cbd->progname, data);
}

int main(int argc, char *argv[])
{
	int err;
	int res = 0;
	char key[] = "1";
	rados_t cluster;
	rados_ioctx_t io;
	callback_data cbd;
	cbd.out = stdout;
	cbd.progname = argv[0];
	common_setup(argv[0], cluster, io);
	err = atomic_read_cb(io, key, 1, _document, _error, &cbd);
	if(err < 0)
	{
		return err;
	}
	if(!cbd.json)
	{
		fprintf(stderr, "%s: failed to get json document from key %s\n", argv[0], key);
		return -1;
	}
	err = atomic_write_cb(io, key, _getdata, &cbd, cbd.version, NULL);
	if(err < 0)
	{
		fprintf(stderr, "%s: failed to perform op on key %s. %s\n", argv[0], key, strerror(-err));
		res = 1;
	}
	if(cbd.json)
	{
		json_object_put(cbd.json);
	}
	common_cleanup(argv[0], cluster, io);
	return res;
}
