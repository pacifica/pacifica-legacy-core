#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <glib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[])
{
	char *remote_user;
	char *state;
	char *document_root;
	char *path_info;
	char *at;
	char *str;
	int res;
	int status;
	char *newargv[16];
	char buf[128];
	char hostname[128];
	gchar **dirs;
	pid_t pid;
	document_root = getenv("DOCUMENT_ROOT");
	remote_user = getenv("REMOTE_USER");
	path_info = getenv("PATH_INFO");
	if(!path_info)
	{
		printf("Error: Failed to get PATH_INFO\n");
		return 0;
	}
	if(!remote_user)
	{
		printf("Error: Failed to get REMOTE_USER\n");
		return 0;
	}
	if(!document_root)
	{
		printf("Error: Failed to get DOCUMENT_ROOT\n");
		return 0;
	}
	dirs = g_strsplit(path_info, "/", 0);
	if(!dirs)
	{
		printf("Error: Failed to split PATH_INFO\n");
		return 0;
	}
	if(g_strv_length(dirs) < 2)
	{
		printf("Error: Path too short\n");
		return 0;
	}
//FIXME ! Kerberos hack.
	at = strchr(remote_user, '@');
	if(at)
	{
		*at = '\0';
	}
	if(g_strv_length(dirs) == 3)
		at = dirs[2];
	else
		at = "html";
	printf("Content-Type: text/%s; charset=us-ascii\n\n", at);
	fflush(stdout);
	
	sprintf(buf, "/tmp/state.%s", dirs[1]);	
	if(access(buf, R_OK) == 0)
	{
		sprintf(buf, "/tmp/state");
	}
	else
	{
		res = gethostname(hostname, 128);
		sprintf(buf, "/srv/myemsl-ingest/%s/state/%s/state", remote_user, hostname);
	}

	newargv[0] = "myemsl_status";
	newargv[1] = "--username";
	newargv[2] = remote_user;
	newargv[3] = "--jobid";
	newargv[4] = dirs[1];
	newargv[5] = "--format",
	newargv[6] = at;
	newargv[9] = NULL;
//	printf("%s %s %s %s %s %s %s %s %s\n", newargv[0], newargv[1], newargv[2], newargv[3], newargv[4], newargv[5], newargv[6], newargv[7], newargv[8]);
//	fprintf(stderr, "%d\n", getuid());

	pid = fork();
	if(pid < 0)
	{
		printf("Error: Failed to fork");
		return 0;
	}
	if(pid == 0)
	{
		execvp(newargv[0], newargv);
		return -1;
	}
	res = wait(&status);
	if(res != pid)
	{
		printf("Error: Unknown child exited.\n");
	}
	else
	{
		if(!WIFEXITED(status))
		{
			printf("Error: Failed to exit normally. %d\n", status);
		}
		else
		{
			if(WEXITSTATUS(status) != 0)
				printf("Error: Failed to run. %d\n", WEXITSTATUS(status));
		}
	}
	return 0;
}
