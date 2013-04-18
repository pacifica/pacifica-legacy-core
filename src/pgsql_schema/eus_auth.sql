SET search_path = myemsl, pg_catalog;

DROP TABLE "eus_auth";
CREATE TABLE "eus_auth" (
        "user_name" varchar(30),
        "user_passwd" varchar(32),
	"session_id" varchar(256),
	"time" TIMESTAMP WITHOUT TIME ZONE default now()
)
WITHOUT OIDS;
ALTER TABLE "eus_auth" OWNER TO "metadata_admins";
GRANT SELECT ON "eus_auth" to "metadata_readers";

