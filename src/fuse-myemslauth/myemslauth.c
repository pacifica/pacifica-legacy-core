/*
  fuse myemsl auth module: Authorize myemsl users.
  Copyright (C) 2007  Miklos Szeredi <miklos@szeredi.hu>
  Copyright (C) 2011  Kevin Fox <Kevin.Fox@pnnl.gov>

  This program can be distributed under the terms of the GNU LGPLv2.
  See the file COPYING.LIB
*/

#define FUSE_USE_VERSION 26

#include <fuse.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>

typedef struct
{
	int depth;
	struct fuse_fs *next;
} myemslauth_data;

static myemslauth_data *myemslauth_get(void)
{
	return fuse_get_context()->private_data;
}

static int myemsl_validate(const char *name, int len)
{
	uid_t uid = fuse_get_context()->uid;
	return (uid == 0 || uid == 48)? 0: -EACCES;
}

static int myemslauth_authpath(myemslauth_data *d, const char *path, int getattr)
{
	const char *tmppath;
	int i;
	int res;
	for(; *path == '/'; path++);
	for(i = d->depth - 1; i > 0; i--)
	{
		tmppath = strchr(path, '/');
		if(!tmppath)
		{
			break;
		}
		path = tmppath + 1;
	}
	printf("Depth %d i %d Path %s\n", d->depth, i, path);
	tmppath = strchr(path, '/');
	if(i == 0 && (!getattr || tmppath))
	{
		if(!tmppath)
		{
			tmppath = path + strlen(path);
		}
		if(tmppath == path)
		{
			return 0;
		}
		printf("Entry: ");
		fwrite(path, tmppath - path, 1, stdout);
		printf("\n");
		return myemsl_validate(path, tmppath - path);
	}
	return 0;
}

static int myemslauth_getattr(const char *path, struct stat *stbuf)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 1);
	if(!res)
	{
		res = fuse_fs_getattr(d->next, path, stbuf);
	}
	return res;
}

static int myemslauth_fgetattr(const char *path, struct stat *stbuf, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_fgetattr(d->next, path, stbuf, fi);
	}
	return res;
}

static int myemslauth_access(const char *path, int mask)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_access(d->next, path, mask);
	}
	return res;
}

static int myemslauth_readlink(const char *path, char *buf, size_t size)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_readlink(d->next, path, buf, size);
	}
	return res;
}

static int myemslauth_opendir(const char *path, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_opendir(d->next, path, fi);
	}
	return res;
}

static int myemslauth_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_readdir(d->next, path, buf, filler, offset, fi);
	}
	return res;
}

static int myemslauth_releasedir(const char *path, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_releasedir(d->next, path, fi);
	}
	return res;
}

static int myemslauth_mknod(const char *path, mode_t mode, dev_t rdev)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_mknod(d->next, path, mode, rdev);
	}
	return res;
}

static int myemslauth_mkdir(const char *path, mode_t mode)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_mkdir(d->next, path, mode);
	}
	return res;
}

static int myemslauth_unlink(const char *path)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_unlink(d->next, path);
	}
	return res;
}

static int myemslauth_rmdir(const char *path)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_rmdir(d->next, path);
	}
	return res;
}

static int myemslauth_symlink(const char *from, const char *path)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_symlink(d->next, from, path);
	}
	return res;
}

static int myemslauth_rename(const char *from, const char *to)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, from, 0);
	if(!res)
	{
		res = myemslauth_authpath(d, to, 0);
		if(!res)
		{
			res = fuse_fs_rename(d->next, from, to);
		}
	}
	return res;
}

static int myemslauth_link(const char *from, const char *to)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, from, 0);
	if(!res)
	{
		res = myemslauth_authpath(d, to, 0);
		if(!res)
		{
			res = fuse_fs_link(d->next, from, to);
		}
	}
	return res;
}

static int myemslauth_chmod(const char *path, mode_t mode)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_chmod(d->next, path, mode);
	}
	return res;
}

static int myemslauth_chown(const char *path, uid_t uid, gid_t gid)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_chown(d->next, path, uid, gid);
	}
	return res;
}

static int myemslauth_truncate(const char *path, off_t size)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_truncate(d->next, path, size);
	}
	return res;
}

static int myemslauth_ftruncate(const char *path, off_t size, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_ftruncate(d->next, path, size, fi);
	}
	return res;
}

static int myemslauth_utimens(const char *path, const struct timespec ts[2])
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_utimens(d->next, path, ts);
	}
	return res;
}

static int myemslauth_create(const char *path, mode_t mode, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_create(d->next, path, mode, fi);
	}
	return res;
}

static int myemslauth_open(const char *path, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_open(d->next, path, fi);
	}
	return res;
}

static int myemslauth_read(const char *path, char *buf, size_t size, off_t offset, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_read(d->next, path, buf, size, offset, fi);
	}
	return res;
}

static int myemslauth_write(const char *path, const char *buf, size_t size, off_t offset, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_write(d->next, path, buf, size, offset, fi);
	}
	return res;
}

static int myemslauth_statfs(const char *path, struct statvfs *stbuf)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_statfs(d->next, path, stbuf);
	}
	return res;
}

static int myemslauth_flush(const char *path, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_flush(d->next, path, fi);
	}
	return res;
}

static int myemslauth_release(const char *path, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_release(d->next, path, fi);
	}
	return res;
}

static int myemslauth_fsync(const char *path, int isdatasync, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_fsync(d->next, path, isdatasync, fi);
	}
	return res;
}

static int myemslauth_fsyncdir(const char *path, int isdatasync, struct fuse_file_info *fi)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_fsyncdir(d->next, path, isdatasync, fi);
	}
	return res;
}

static int myemslauth_setxattr(const char *path, const char *name, const char *value, size_t size, int flags)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_setxattr(d->next, path, name, value, size, flags);
	}
	return res;
}

static int myemslauth_getxattr(const char *path, const char *name, char *value, size_t size)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_getxattr(d->next, path, name, value, size);
	}
	return res;
}

static int myemslauth_listxattr(const char *path, char *list, size_t size)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_listxattr(d->next, path, list, size);
	}
	return res;
}

static int myemslauth_removexattr(const char *path, const char *name)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_removexattr(d->next, path, name);
	}
	return res;
}

static int myemslauth_lock(const char *path, struct fuse_file_info *fi, int cmd, struct flock *lock)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_lock(d->next, path, fi, cmd, lock);
	}
	return res;
}

static int myemslauth_bmap(const char *path, size_t blocksize, uint64_t *idx)
{
	myemslauth_data *d = myemslauth_get();
	int res = myemslauth_authpath(d, path, 0);
	if(!res)
	{
		res = fuse_fs_bmap(d->next, path, blocksize, idx);
	}
	return res;
}

static void *myemslauth_init(struct fuse_conn_info *conn)
{
	myemslauth_data *d = myemslauth_get();
	fuse_fs_init(d->next, conn);
	return d;
}

static void myemslauth_destroy(void *data)
{
	myemslauth_data *d = data;
	fuse_fs_destroy(d->next);
	free(d);
}

static struct fuse_operations myemslauth_oper = {
	.destroy	= myemslauth_destroy,
	.init		= myemslauth_init,
	.getattr	= myemslauth_getattr,
	.fgetattr	= myemslauth_fgetattr,
	.access		= myemslauth_access,
	.readlink	= myemslauth_readlink,
	.opendir	= myemslauth_opendir,
	.readdir	= myemslauth_readdir,
	.releasedir	= myemslauth_releasedir,
	.mknod		= myemslauth_mknod,
	.mkdir		= myemslauth_mkdir,
	.symlink	= myemslauth_symlink,
	.unlink		= myemslauth_unlink,
	.rmdir		= myemslauth_rmdir,
	.rename		= myemslauth_rename,
	.link		= myemslauth_link,
	.chmod		= myemslauth_chmod,
	.chown		= myemslauth_chown,
	.truncate	= myemslauth_truncate,
	.ftruncate	= myemslauth_ftruncate,
	.utimens	= myemslauth_utimens,
	.create		= myemslauth_create,
	.open		= myemslauth_open,
	.read		= myemslauth_read,
	.write		= myemslauth_write,
	.statfs		= myemslauth_statfs,
	.flush		= myemslauth_flush,
	.release	= myemslauth_release,
	.fsync		= myemslauth_fsync,
	.fsyncdir	= myemslauth_fsyncdir,
	.setxattr	= myemslauth_setxattr,
	.getxattr	= myemslauth_getxattr,
	.listxattr	= myemslauth_listxattr,
	.removexattr	= myemslauth_removexattr,
	.lock		= myemslauth_lock,
	.bmap		= myemslauth_bmap,
#ifdef WITH_FUSE_NULLPATH
	.flag_nullpath_ok = 1,
#endif
};

static struct fuse_opt myemslauth_opts[] = {
	FUSE_OPT_KEY("-h", 0),
	FUSE_OPT_KEY("--help", 0),
	{ "myemslauth_depth=%d", offsetof(myemslauth_data, depth), 0 },
	FUSE_OPT_END
};

static void myemslauth_help(void)
{
	fprintf(stderr,
"    -o myemslauth_depth=N	    The position in the path to protect.\n");
}

static int myemslauth_opt_proc(void *data, const char *arg, int key, struct fuse_args *outargs)
{
	(void) data;
	(void) arg;
	(void) outargs;
	if(!key)
	{
		myemslauth_help();
		return -1;
	}
	return 1;
}

static struct fuse_fs *myemslauth_new(struct fuse_args *args, struct fuse_fs *next[])
{
	struct fuse_fs *fs;
	myemslauth_data *d;
	d = calloc(1, sizeof(myemslauth_data));
	if(d == NULL)
	{
		fprintf(stderr, "fuse-myemslauth: memory allocation failed\n");
		return NULL;
	}
	if(fuse_opt_parse(args, d, myemslauth_opts, myemslauth_opt_proc) == -1)
	{
		free(d);
		return NULL;
	}
	if(!next[0] || next[1])
	{
		fprintf(stderr, "fuse-myemslauth: exactly one next filesystem required\n");
		free(d);
		return NULL;
	}
	if(d->depth < 1)
	{
		fprintf(stderr, "fuse-myemslauth: 'myemslauth_depth' must be 1 or greater\n");
		free(d);
		return NULL;
	}
	d->next = next[0];
	fs = fuse_fs_new(&myemslauth_oper, sizeof(myemslauth_oper), d);
	if(!fs)
	{
		free(d);
	}
	return fs;
}

FUSE_REGISTER_MODULE(myemslauth, myemslauth_new);
