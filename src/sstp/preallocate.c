#include <stdio.h>
#include <stdlib.h>
#include <glib.h>
#include <string.h>
#include <errno.h>
#include <grp.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#define SUBDIRROOT "../myemsl/staging"
#define SUBDIR "myemsl/staging"

//FIXME umask

int main(int argc, char *argv[])
{
	char *server_name;
	char *document_root;
	char *remote_user;
	char *str_size;
	char *query_string;
	gchar *unixuser;
	gchar *location;
	gchar **query = NULL;
	char tmp_location[] = "MYEMSL_XXXXXX";
	int res;
	int fd;
	int i;
//FIXME is long big enough?
	long size = 0;
	struct group *grp;
	struct stat stbuf;
	GKeyFile *keyfile = g_key_file_new();
	g_key_file_load_from_file(keyfile, "/etc/myemsl/general.ini", G_KEY_FILE_NONE, NULL);
	unixuser = g_key_file_get_string(keyfile, "unix", "user", NULL);
	printf("Content-Type: text/plain; charset=us-ascii\n\n");
	if(!unixuser)
	{
		printf("Error: Failed to get myemsl user\n");
		exit(0);
	}
	document_root = getenv("DOCUMENT_ROOT");
	remote_user = getenv("REMOTE_USER");
	query_string = getenv("QUERY_STRING");
	server_name = getenv("SERVER_NAME");
	grp = getgrnam(unixuser);
	if(!grp)
	{
		printf("Error: Failed to get myemsl group\n");
		exit(0);
	}
	if(remote_user && document_root && server_name)
	{
		if(query_string)
		{
			query = g_strsplit(query_string, "&", 0);
			if(query)
			{
				for(i = 0; query[i]; i++)
				{
					if(!strncmp(query[i], "size=", strlen("size=")))
					{
						size = atol(query[i] + strlen("size="));
						if(size < 0)
							size = 0;
					}
				}
				g_strfreev(query);
			}
			else
			{
				printf("Error: Failed split query string\n");
			}
		}
		else
		{
			printf("Error: Failed to get query string\n");
		}
		location = g_strdup_printf("%s/%s/%s", document_root, SUBDIRROOT, remote_user);
		if(location)
		{
//FIXME how to get myemsl user access here.
			res = stat(location, &stbuf);
			if(res)
			{
				gchar *tmpstr = g_strdup_printf("myemsl_mkstagedir --username %s", remote_user);
				if(!tmpstr)
				{
					fprintf(stderr, "Failed to allocate string\n");
					exit(-1);
				}
//FIXME Potential issue with contents of REMOTE_USER make sure the value of that string doesn't
//      have shell injections in it. Since this is comming from apache we aren't caring.
//				printf("Calling %s\n", tmpstr);
				res = system(tmpstr);
				if(res)
				{
					fprintf(stderr, "Failed to make stage directory\n");
					exit(-1);
				}
			}
			res = chdir(location);
			if(!res)
			{
				fd = mkstemp(tmp_location);
				if(fd >= 0)
				{
					res = 0;
					if(size > 0)
						res = ftruncate(fd, size);
					if(!res)
					{
						printf("Server: %s\n", server_name);
						printf("Location: /%s/%s/%s\n", SUBDIR, remote_user, tmp_location);
					}
					else
					{
						printf("Error: Failed to truncate to size. %d %d\n", res, errno);
					}
					close(fd);
				}
				else
				{
					printf("Error: Failed to mkstemp. %d\n", res);
				}
			}
			else
			{
				printf("Error: Failed to chdir to user directory. %d. %s\n", res, location);
			}
			g_free(location);
		}

	}
	else
	{
		printf("Error: REMOTE_USER, DOCUMENT_ROOT, or SERVER_NAME not defined\n");
	}
	return 0;
}
