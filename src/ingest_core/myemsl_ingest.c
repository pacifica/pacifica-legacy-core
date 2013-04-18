#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <glib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>

int main(int argc, char *argv[])
{
	struct passwd *pwent;
	gchar *username = NULL;
	gchar *bundle = NULL;
	gchar *statefd = NULL;
	GOptionEntry entries[] =
	{
		{ "username", 'u', 0, G_OPTION_ARG_STRING, &username, "MyEMSL Username", "U" },
		{ "bundle", 'b', 0, G_OPTION_ARG_STRING, &bundle, "Bundle to process", "B" },
		{ "statefd", 's', 0, G_OPTION_ARG_STRING, &statefd, "State File Descriptor", "S" },
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

	context = g_option_context_new("- MyEMSL Ingestor");
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
	if(!bundle)
	{
		fprintf(stderr, "You must specify a bundle with the --bundle option.\n");
		exit(-1);
	}
	pwent = getpwnam(unixuser);
	if(!pwent)
	{
		fprintf(stderr, "Failed to get uid for the myemsl user.\n");
		exit(-1);
	}
	res = stat(bundle, &statbuf);
	if(res)
	{
		fprintf(stderr, "Failed to stat file. %d\n", res);
		exit(-1);
	}
	if(statbuf.st_uid != realuid)
	{
		fprintf(stderr, "You do not own that file. Bailing.\n");
		exit(-1);
	}
	res = chmod(bundle, S_IRUSR);
	if(res)
	{
		fprintf(stderr, "Failed to chmod submited file to MyEMSL.\n");
		exit(-1);
	}
	res = chown(bundle, pwent->pw_uid, pwent->pw_gid);
	if(res)
	{
		fprintf(stderr, "Failed to chown submited file to MyEMSL.\n");
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
	newargv[0] = "/usr/bin/python";
	newargv[1] = "-m";
	newargv[2] = "myemsl/catchall";
	newargv[3] = "/usr/libexec/myemsl/ingest/ingest_vni";
	newargv[4] = "--username";
	newargv[5] = username;
	newargv[6] = "--bundle";
	newargv[7] = bundle;
	newargv[8] = "--statefd";
	newargv[9] = statefd ? statefd:"1";
	newargv[10] = NULL;
	res = execvp(newargv[0], newargv);
	if(res)
	{
		fprintf(stderr, "Failed to exec %s. Error: %d.\n", newargv[0], res);
		exit(-1);
	}
	return 0;
}
