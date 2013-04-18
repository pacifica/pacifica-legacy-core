#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <glib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>

int main(int argc, char *argv[])
{
	struct passwd *pwent;
	struct group *grpent;
	gchar *location;
	gchar *username = NULL;
	GOptionEntry entries[] =
	{
		{ "username", 'u', 0, G_OPTION_ARG_STRING, &username, "MyEMSL Username", "U" },
		{ NULL }
	};
	GError *error = NULL;
	GOptionContext *context;
	struct stat statbuf;
	int res;
	char *newargv[6];
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
	context = g_option_context_new("- MyEMSL mkstagedir");
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
	if(!username)
	{
		fprintf(stderr, "You must specify a username to create\n");
		exit(-1);
	}
	if(strcmp(pwent->pw_name, "apache"))
	{
		fprintf(stderr, "Only the apache user can use this tool.\n");
		exit(-1);
	}
	grpent = getgrnam(unixuser);
	if(!grpent)
	{
		fprintf(stderr, "Failed to get gid for the myemsl user.\n");
		exit(-1);
	}
	location = g_strdup_printf("%s/%s", "/var/www/myemsl/staging", username);
	if(!location)
	{
		fprintf(stderr, "Failed to allocate memory for location.\n");
		exit(-1);
	}
	res = mkdir(location, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP);
	if(res)
	{
		fprintf(stderr, "Failed to mkdir %s.\n", location);
		exit(-1);
	}
	res = chmod(location, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP);
	if(res)
	{
		fprintf(stderr, "Failed to chmod %s.\n", location);
		exit(-1);
	}
	res = chown(location, pwent->pw_uid, grpent->gr_gid);
	if(res)
	{
		fprintf(stderr, "Failed to chown.\n");
		exit(-1);
	}
	return 0;
}
