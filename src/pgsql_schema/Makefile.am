pkgpgsql_DATA = eus_auth.sql eus.sql myemsl.sql myemsl_users.sql myemsl_authz.sql \
                updates/1.10-1.11.sql updates/1.7-1.8.sql updates/1.8-1.9.sql \
                updates/1.9-1.10.sql

EXTRA_DIST = dbcreate.sh.in $(pkgpgsql_DATA)

pkgmyemsl_SCRIPTS = dbcreate.sh

$(pkgmyemsl_SCRIPTS):
	sed 's:@LOCATION@:$(pkgpgsqldir):g' $(@).in > $(@)

clean-generic:
	$(RM) $(pkgmyemsl_SCRIPTS)

