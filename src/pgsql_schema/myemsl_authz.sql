CREATE SCHEMA myemsl;
SET search_path = myemsl, pg_catalog;

DROP TABLE "permission_group";
CREATE TABLE "permission_group" (
	"permission_group_id" serial PRIMARY KEY,
	"type" text,
	"name" text
)
WITHOUT OIDS;
ALTER TABLE "permission_group" ADD CONSTRAINT type_name UNIQUE (type, name);
ALTER TABLE "permission_group" OWNER TO "metadata_admins";
GRANT SELECT ON "permission_group" to "metadata_readers";

DROP TABLE "permission_group_members";
CREATE TABLE "permission_group_members" (
	"permission_group_id" int references permission_group(permission_group_id),
	"person_id" int references eus.users(person_id)
)
WITHOUT OIDS;
ALTER TABLE "permission_group_members" ADD CONSTRAINT permission_group_members_con UNIQUE (permission_group_id, person_id);
ALTER TABLE "permission_group_members" OWNER TO "metadata_admins";
GRANT SELECT ON "permission_group_members" to "metadata_readers";

DROP TABLE "permission_set";
CREATE TABLE "permission_set" (
	"permission_set_id" serial PRIMARY KEY
)
WITHOUT OIDS;
ALTER TABLE "permission_set" OWNER TO "metadata_admins";
GRANT SELECT ON "permission_set" to "metadata_readers";

DROP TABLE "permission_set_perms";
CREATE TABLE "permission_set_perms" (
	"permission_set_id" integer references permission_set(permission_set_id),
	"permission" text
)
WITHOUT OIDS;
ALTER TABLE "permission_set_perms" ADD CONSTRAINT permission_set_members_con UNIQUE (permission_set_id, permission);
ALTER TABLE "permission_set_perms" OWNER TO "metadata_admins";
GRANT SELECT ON "permission_set_perms" to "metadata_readers";

DROP TABLE "permissions";
CREATE TABLE "permissions" (
	"permission_set_id" int references permission_set(permission_set_id),
	"permission_group_id" int references permission_group(permission_group_id),
	"permission_class" text
)
WITHOUT OIDS;
ALTER TABLE "permissions" ADD CONSTRAINT one_set_per_group_class UNIQUE (permission_set_id, permission_group_id, permission_class);
ALTER TABLE "permissions" ADD CONSTRAINT group_class UNIQUE (permission_group_id, permission_class);
ALTER TABLE "permissions" OWNER TO "metadata_admins";
GRANT SELECT ON "permissions" to "metadata_readers";

