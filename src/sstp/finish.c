#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <glib.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>

int main(int argc, char *argv[])
{
	char *remote_user;
	char *document_root;
	char *path_info;
	char *server_name;
	char *script_name;
	char *server_port;
	char *at;
	char *str;
	int res;
	int status;
	int pipefd[2];
	FILE *childinput;
	int jobid;
	char *newargv[16];
	gchar *bundle;
	gchar **dirs;
	pid_t pid;
	printf("Content-Type: text/plain; charset=us-ascii\n\n");
	fflush(stdout);
	document_root = getenv("DOCUMENT_ROOT");
	remote_user = getenv("REMOTE_USER");
	path_info = getenv("PATH_INFO");
	server_name = getenv("SERVER_NAME");
	script_name = getenv("SCRIPT_NAME");
	server_port = getenv("SERVER_PORT");
	if(!server_port)
	{
		printf("Error: SERVER_PORT undefined: are you really running this in a web server?\n");
		return 0;
	}
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
	if(!server_name)
	{
		printf("Error: Failed to get SERVER_NAME\n");
		return 0;
	}
	if(!script_name)
	{
		printf("Error: Failed to get SCRIPT_NAME\n");
		return 0;
	}
	dirs = g_strsplit(path_info, "/", 0);
	if(!dirs)
	{
		printf("Error: Failed to split PATH_INFO\n");
		return 0;
	}
	if(g_strv_length(dirs) < 4)
	{
		printf("Error: Path too short\n");
		return 0;
	}
	if(strcmp(dirs[3], remote_user))
	{
		printf("Error: You do not have permission to access that directory\n");
		return 0;
	}
//FIXME MADS WORKAROUND
//	bundle = g_strdup_printf("%s%s", document_root, path_info);
	bundle = g_strdup_printf("%s/%s", document_root, path_info);
	if(!bundle)
	{
		printf("Error: Failed to allocate string\n");
		return 0;
	}
//FIXME ! Kerberos hack.
	at = strchr(remote_user, '@');
	if(at)
	{
		*at = '\0';
	}
	newargv[0] = "myemsl_ingest";
	newargv[1] = "--username";
	newargv[2] = remote_user;
	newargv[3] = "--bundle";
	newargv[4] = bundle;
	newargv[5] = "--statefd";
	newargv[6] = "0";
	newargv[7] = NULL;
//	printf("%s %s %s %s %s\n", newargv[0], newargv[1], newargv[2], newargv[3], newargv[4], newargv[5]);
//	fprintf(stderr, "%d\n", getuid());
	if(pipe(pipefd) == -1)
	{
		printf("Error: Creating pipe");
		return 0;
	}
	pid = fork();
	if(pid < 0)
	{
		printf("Error: Failed to fork");
		return 0;
	}
	if(pid == 0)
	{
		char f[10];
		sprintf(f, "%d", pipefd[1]);
		close(pipefd[0]);
		newargv[6] = f;
		execvp(newargv[0], newargv);
		return -1;
	}
	close(pipefd[1]);
	childinput = fdopen(pipefd[0], "r");
	res = fscanf(childinput, "%d", &jobid);
	if(res != 1)
	{
		printf("Error: can't get the child status\n");
		fflush(stdout);
	}
	fclose(childinput);
	res = wait(&status);
	if(res != pid)
	{
		printf("Error: Unknown child exited.\n");
		fflush(stdout);
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
			else
			{
				if(!strcmp(server_port, "80"))
					printf("Status: http://%s%s/status/%d\n", server_name, dirname(script_name), jobid);
				else
					printf("Status: https://%s%s/status/%d\n", server_name, dirname(script_name), jobid);
				printf("Accepted\n");
			}
		}
	}
	g_free(bundle);
	return 0;
}
