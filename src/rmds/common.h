#include <stdio.h>
#include <stdlib.h>
#include <rados/librados.h>

#define VERSION_TAG "version"
#define POOLNAME "testpool"

typedef enum
{
      READ_ERROR_TYPE_OK = 0, READ_ERROR_TYPE_FNF = 1, READ_ERROR_TYPE_CHANGED = 2, READ_ERROR_TYPE_OTHER = 3
} read_error_type;

typedef void (*document_cb)(const char *data, unsigned long size, long version, void *user_data);
typedef void (*error_cb)(const char *data, void *user_data);
typedef void (*writedata_cb)(void *wdcbd, const char *data, unsigned long size);
typedef int (*getdata_cb)(long version, writedata_cb writedata, void *wdcbd, void *user_data);

long version_encode(long version);
long version_decode(long version);
int version_get(rados_ioctx_t io, const char *key, long *version);
int common_setup(const char *progname, rados_t &cluster, rados_ioctx_t &io);
int common_cleanup(const char *progname, rados_t &cluster, rados_ioctx_t &io);
int atomic_write_cb(rados_ioctx_t io, const char *key, getdata_cb getdata, void *user_data, long version_in, long *version_out);
int atomic_write_data(rados_ioctx_t io, const char *key, const char *data, unsigned long size, long version_in, long *version_out);
int atomic_create_data(rados_ioctx_t io, const char *key, const char *data, unsigned long size, long version_in);
read_error_type atomic_read_cb(rados_ioctx_t io, const char *key, unsigned long buffsize, document_cb document, error_cb error, void *user_data);
