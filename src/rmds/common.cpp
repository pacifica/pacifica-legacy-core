#include <rados/librados.hpp>
#include <endian.h>

#include "common.h"

using librados::ObjectReadOperation;
using librados::ObjectWriteOperation;
using librados::IoCtx;
using ceph::bufferlist;

long version_encode(long version)
{
	return (long)htole64((uint64_t)version);
}

long version_decode(long version)
{
	return (long)le64toh((uint64_t)version);
}

int version_get(rados_ioctx_t io, const char *key, long *version)
{
	long enversion;
	int err;
	err = rados_getxattr(io, key, VERSION_TAG, (char*)&enversion, sizeof(long));
	*version = version_decode(enversion);
	return 0;
}

int common_setup(char *progname, rados_t &cluster, rados_ioctx_t &io)
{
	int err;
	char poolname[] = "testpool";
	err = rados_create(&cluster, NULL);
	if(err < 0)
	{
		fprintf(stderr, "%s: cannot get a cluster handle: %s\n", progname, strerror(-err));
		return 1;
	}
	err = rados_conf_read_file(cluster, "/etc/ceph/ceph.conf");
	if(err < 0)
	{
		fprintf(stderr, "%s: cannot read config file: %s\n", progname, strerror(-err));
		return 1;
	}
	err = rados_connect(cluster);
	if(err < 0)
	{
		fprintf(stderr, "%s: cannot connect to cluster: %s\n", progname, strerror(-err));
		return 1;
	}
	err = rados_ioctx_create(cluster, poolname, &io);
	if(err < 0)
	{
		fprintf(stderr, "%s: cannot open rados pool %s: %s\n", progname, poolname, strerror(-err));
		rados_shutdown(cluster);
		return 1;
	}
	return 0;
}

int common_cleanup(char *progname, rados_t &cluster, rados_ioctx_t &io)
{
	rados_ioctx_destroy(io);
	rados_shutdown(cluster);
	return 0;
}

static void _writedata(void *wdcbd, const char *data, unsigned long size)
{
	bufferlist *bl2 = (bufferlist*)wdcbd;
	bl2->append(data, size);
}

int _atomic_write(rados_ioctx_t io, const char *key, const char *data, unsigned long size, long version_in, long *version_out, int create, getdata_cb getdata, void *user_data)
{
	int err;
	IoCtx ioctx;
	bufferlist bl;
	bufferlist bl2;
	bufferlist bl3;
	long version = version_in;
	long enversion = version_encode(version_in);
	ObjectWriteOperation op;
	IoCtx::from_rados_ioctx_t(io, ioctx);
	if(create)
	{
		op.create(1);
	}
	else
	{
		bl.append((char*)&enversion, sizeof(long));
		op.cmpxattr(VERSION_TAG, LIBRADOS_CMPXATTR_OP_EQ, bl);
		version++;
	}

	if(data)
	{
		bl2.append(data, size);
	}
	else if(getdata)
	{
		err = getdata(version, _writedata, &bl2, user_data);
		if(err)
		{
			return err;
		}
	}

	enversion = version_encode(version);
	op.write_full(bl2);
	bl3.append((char*)&enversion, sizeof(long));
	op.setxattr(VERSION_TAG, bl3);
	err = ioctx.operate(key, &op);
	if(version_out)
	{
		*version_out = version;
	}
	return err;
}

int atomic_write_cb(rados_ioctx_t io, const char *key, getdata_cb getdata, void *user_data, long version_in, long *version_out)
{
	return _atomic_write(io, key, NULL, 0, version_in, version_out, 0, getdata, user_data);
}

int atomic_write_data(rados_ioctx_t io, const char *key, const char *data, unsigned long size, long version_in, long *version_out)
{
	return _atomic_write(io, key, data, size, version_in, version_out, 0, NULL, NULL);
}

int atomic_create_data(rados_ioctx_t io, const char *key, const char *data, unsigned long size, long version_in)
{
	return _atomic_write(io, key, data, size, version_in, NULL, 1, NULL, NULL);
}

int atomic_read_cb(rados_ioctx_t io, const char *key, unsigned long buffsize, document_cb document, error_cb error, void *user_data)
{
	int res;
	int err;
	int read_err;
	int getxattr_err;
	int version_inited = 0;
	unsigned int size;
	off_t offset = 0;
	long version;
	long version_prev;
	char *tbuffer;
	bufferlist bl;
	bufferlist bl2;
	bufferlist::iterator bli;
	IoCtx ioctx;
	IoCtx::from_rados_ioctx_t(io, ioctx);
	ObjectReadOperation rop;
	std::string document_str = "";
	std::string error_str = "";
	res = 0;
	while(1)
	{
		rop.getxattr("version", &bl, &getxattr_err);
		rop.read(offset, buffsize, &bl2, &read_err);
		err = ioctx.operate(key, &rop, NULL);
		if(err < 0)
		{
			error_str.append("cannot operate on key ").append(key).append(": ").append(strerror(-err));
			res = 1;
			break;
		}
		if(getxattr_err < 0)
		{
			error_str.append("cannot read from xattr from key ").append(key).append(": ").append(strerror(-getxattr_err));
			res = 1;
			break;
		}
		if(bl.length() != sizeof(version))
		{
			error_str.append("xattr not the right size for key ").append(key).append(": ").append(std::to_string(static_cast<long long>(bl.length())));
			res = 1;
			break;
		}
		bli = bl.begin();
		bli.copy(sizeof(version), (char*)&version);
		if(version_inited == 0)
		{
			version_prev = version;
			version_inited = 1;
		}
		else if(version != version_prev)
		{
			error_str.append("version changed while reading key ").append(key).append(": ").append(std::to_string(static_cast<long long>(version_decode(version_prev)))).append(" != ").append(std::to_string(static_cast<long long>(version_decode(version))));
			res = 1;
			break;
		}
		if(read_err < 0)
		{
			error_str.append("cannot read from key ").append(key).append(": ").append(strerror(-read_err));
			res = 1;
			break;
		}
		else if(bl2.length() == 0)
		{
			break;
		}
		size = bl2.length();
		tbuffer = bl2.c_str();
		document_str.append(tbuffer, size);
		offset += size;
		bl.clear();
		bl2.clear();
		if(size < buffsize)
		{
			break;
		}
	}
	if(res == 0)
	{
		document_str.append("\0");
		document(document_str.c_str(), offset, version, user_data);
	}
	else
	{
		error(error_str.c_str(), user_data);
	}
	return res;
}
