#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <malloc.h>
#include <pwd.h>
#include <sys/types.h>

int myemsl_switch_process_user(const char *user)
{
	char *tmpptr;
	struct passwd *pwent;
	int res;
	pwent = getpwnam(user);
	if(!pwent)
	{
		return -3;
	}
	res = setregid(pwent->pw_gid, pwent->pw_gid);
	if(res)
	{
		return -4;
	}
	res = setreuid(pwent->pw_uid, pwent->pw_uid);
	if(res)
	{
		return -5;
	}
	return 0;
}

void usage()
{
	fprintf(stderr, "You must specify -u user -p pidfile.\n");
	exit(-1);
}

int main(int argc, char *argv[])
{
	FILE *fd;
	int res;
	if(argc != 5)
	{
		usage();
	}
	if(strcmp(argv[1], "-u"))
	{
		usage();
	}
	if(strcmp(argv[3], "-p"))
	{
		usage();
	}
	fd = fopen(argv[4], "w");
	if(!fd)
	{
		fprintf(stderr, "Failed to open pid file.\n");
		exit(-1);
	}
	res = myemsl_switch_process_user(argv[2]);
	if(res < 0)
	{
		return res;
	}
	res = daemon(0, 0);
	if(res == -1)
	{
		fprintf(stderr, "Failed to daemonize. %d\n", errno);
		exit(-1);
	}
	fprintf(fd, "%d\n", getpid());
	fclose(fd);
	res = execl("/usr/libexec/myemsl/cartd_child", (char *)NULL);
	return res;
}
