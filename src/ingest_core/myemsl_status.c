#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <glib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <string.h>

int main(int argc, char *argv[])
{
	struct passwd *pwent;
	gchar *username = NULL;
	gchar *jobid = NULL;
	gchar *format = NULL;
	gchar *state = NULL;
	GOptionEntry entries[] =
	{
		{ "username", 'u', 0, G_OPTION_ARG_STRING, &username, "MyEMSL Username", "U" },
		{ "jobid", 'j', 0, G_OPTION_ARG_STRING, &jobid, "Job ID to query", "J" },
		{ "format", 'f', 0, G_OPTION_ARG_STRING, &format, "Format Output", NULL },
		{ NULL }
	};
	GError *error = NULL;
	GOptionContext *context;
	struct stat statbuf;
	int res;
	char *newargv[16];
	uid_t realuid = getuid();
	gchar *unixuser;
	GKeyFile *keyfile = g_key_file_new();
	g_key_file_load_from_file(keyfile, "/etc/myemsl/general.ini", G_KEY_FILE_NONE, NULL);
	unixuser = g_key_file_get_string(keyfile, "unix", "user", NULL);
	if(!unixuser)
	{
		fprintf(stderr, "Failed to get myemsl user\n");
		exit(-1);
	}

	context = g_option_context_new("- MyEMSL Status");
	g_option_context_add_main_entries(context, entries, NULL);
	if(!g_option_context_parse(context, &argc, &argv, &error))
	{
		fprintf(stderr, "option parsing failed: %s\n", error->message);
		exit(-1);
	}
	pwent = getpwuid(realuid);
	if(!pwent)
	{
		fprintf(stderr, "Failed to get your passwd entry.\n");
		exit(-1);
	}
	if(username)
	{
		if(strcmp(pwent->pw_name, "apache"))
		{
			fprintf(stderr, "Only the apache user can specify user.\n");
			exit(-1);
		}
	}
	else
	{
		username = g_strdup(pwent->pw_name);
		if(!username)
		{
			fprintf(stderr, "Could not get calling user's name.\n");
			exit(-1);
		}
	}
	if(!jobid)
	{
		fprintf(stderr, "You must specify a jobid with the --jobid option.\n");
		exit(-1);
	}
	pwent = getpwnam(unixuser);
	if(!pwent)
	{
		fprintf(stderr, "Failed to get uid for the myemsl user.\n");
		exit(-1);
	}
	res = setregid(pwent->pw_gid, pwent->pw_gid);
	if(res)
	{
		fprintf(stderr, "Failed to switch gid.\n");
		exit(-1);
	}
	res = setreuid(pwent->pw_uid, pwent->pw_uid);
	if(res)
	{
		fprintf(stderr, "Failed to switch uid.\n");
		exit(-1);
	}
	newargv[0] = "/usr/libexec/myemsl/ingest/status_vni";
	newargv[1] = "--username";
	newargv[2] = username;
	newargv[3] = "--jobid";
	newargv[4] = jobid;
	newargv[5] = newargv[6] = newargv[7] = newargv[8] = NULL;
	if(format)
	{
		newargv[5] = "--format";
		newargv[6] = format;
	}
	newargv[9] = NULL;
	res = execvp(newargv[0], newargv);
	if(res)
	{
		fprintf(stderr, "Failed to exec %s. Error: %d.\n", newargv[0], res);
		exit(-1);
	}
	return 0;
}
