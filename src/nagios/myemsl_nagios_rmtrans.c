#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <glib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <string.h>
#include <errno.h>

int main(int argc, char *argv[])
{
	int i;
	struct stat buf;
	struct passwd *pwent;
	gchar *tmpstr = NULL;
	gchar *mnt = "/srv/myemsl-nagios";
	gchar *transaction = NULL;
	GOptionEntry entries[] =
	{
		{ "transaction", 't', 0, G_OPTION_ARG_STRING, &transaction, "Transaction to remove", "T" },
		{ NULL }
	};
	GError *error = NULL;
	GOptionContext *context;
	int res;
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
	context = g_option_context_new("- MyEMSL Nagios Remove Transaction");
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
	if(strcmp(pwent->pw_name, "apache"))
	{
		fprintf(stderr, "Only the apache user can use this.\n");
		exit(-1);
	}
	if(!transaction)
	{
		fprintf(stderr, "You must specify a transaction with the --transaction option.\n");
		exit(-1);
	}
	pwent = getpwnam(unixuser);
	if(!pwent)
	{
		fprintf(stderr, "Failed to get uid for the myemsl user.\n");
		exit(-1);
	}
	for(i = 0; i < strlen(transaction); i++)
	{
		if(!(transaction[i] >= '0' && transaction[i] <= '9'))
		{
			fprintf(stderr, "Invalid transaction specified.\n");
			exit(-1);
		}
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
	tmpstr = g_strdup_printf("%s/bundle/%s/Nagios Test.txt", mnt, transaction);
	if(!tmpstr)
	{
		fprintf(stderr, "Failed to malloc.\n");
		exit(-1);
	}
	res = unlink(tmpstr);
	g_free(tmpstr);
	tmpstr = g_strdup_printf("%s/bundle/%s/metadata.txt", mnt, transaction);
	if(!tmpstr)
	{
		fprintf(stderr, "Failed to malloc.\n");
		exit(-1);
	}
	res = unlink(tmpstr);
	g_free(tmpstr);
	tmpstr = g_strdup_printf("%s/bundle/%s", mnt, transaction);
	if(!tmpstr)
	{
		fprintf(stderr, "Failed to malloc.\n");
		exit(-1);
	}
	res = rmdir(tmpstr);
	if(res != 0)
	{
		if(errno == ENOENT)
		{
			g_free(tmpstr);
			tmpstr = g_strdup_printf("%s/bundle", mnt);
			if(!tmpstr)
			{
				fprintf(stderr, "Failed to malloc.\n");
				exit(-1);
			}
			res = lstat(tmpstr, &buf);
		}
		if(res != 0)
		{
			fprintf(stderr, "Failed to removedir.\n");
		}
	}
	g_free(tmpstr);
	return res;
}
