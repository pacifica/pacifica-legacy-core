CREATE DATABASE myemsl_metadata;

CREATE SCHEMA myemsl;
ALTER SCHEMA myemsl OWNER TO metadata_admins;
SET search_path = myemsl, eus, pg_catalog;

DROP TABLE IF EXISTS "groups";
CREATE TABLE "groups" (
	"group_id" SERIAL PRIMARY KEY,
	"name" varchar(128),
	"type" varchar(64)
)
WITHOUT OIDS;
ALTER TABLE "groups" ADD CONSTRAINT name_type UNIQUE (name, type);
ALTER TABLE "groups" OWNER TO "metadata_admins";
GRANT SELECT ON "groups" to "metadata_readers";

DROP TABLE IF EXISTS "subgroups";
CREATE TABLE "subgroups" (
	"parent_id" int references groups(group_id),
	"child_id" int references groups(group_id)
--	"view_items" boolean not null,
--	"read_items" boolean not null,
--	"add_subgroup" boolean not null,
--	"add_item_only" boolean not null,
--	"add_actions_with_items" boolean not null,
--	"add_users" boolean not null,
--	"manage_permissions" boolean not null
)
WITHOUT OIDS;
ALTER TABLE "subgroups" ADD CONSTRAINT parent_child_id UNIQUE (parent_id, child_id);
ALTER TABLE "subgroups" OWNER TO "metadata_admins";
GRANT SELECT ON "subgroups" to "metadata_readers";

DROP TABLE IF EXISTS "group_perm_users";
CREATE TABLE "group_perm_users" (
	"group_id" int references groups(group_id),
	"person_id" int references eus.users(person_id),
	"type" text,
	"view_items" boolean not null,
	"read_items" boolean not null,
	"add_subgroup" boolean not null,
	"add_item_only" boolean not null,
	"add_actions_with_items" boolean not null,
	"manage_permissions" boolean not null
)
WITHOUT OIDS;
ALTER TABLE "group_perm_users" ADD CONSTRAINT parent_child_id UNIQUE (parent_id, child_id);
ALTER TABLE "group_perm_users" OWNER TO "metadata_admins";
GRANT SELECT ON "group_perm_users" to "metadata_readers";

DROP TABLE IF EXISTS "group_perm_groups";
CREATE TABLE "group_perm_groups" (
	"group_id" int references groups(group_id),
	"name" text,
	"type" text,
	"view_items" boolean not null,
	"read_items" boolean not null,
	"add_subgroup" boolean not null,
	"add_item_only" boolean not null,
	"add_actions_with_items" boolean not null,
	"add_users" boolean not null,
	"manage_permissions" boolean not null
)
WITHOUT OIDS;
ALTER TABLE "group_perm_groups" OWNER TO "metadata_admins";
GRANT SELECT ON "group_perm_groups" to "metadata_readers";

DROP TABLE IF EXISTS "items";
CREATE TABLE "items" (
	"item_id" SERIAL PRIMARY KEY,
	"transaction" int,
	"type" varchar(64)
)
WITHOUT OIDS;
ALTER TABLE "items" OWNER TO "metadata_admins";
GRANT SELECT ON "items" to "metadata_readers";

DROP TABLE IF EXISTS "group_items";
CREATE TABLE "group_items" (
	"group_id" INT references groups(group_id),
	"item_id" INT references items(item_id)
)
WITHOUT OIDS;
ALTER TABLE "group_items" OWNER TO "metadata_admins";
GRANT SELECT ON "group_items" to "metadata_readers";
CREATE INDEX item_id_idx ON group_items USING btree (item_id);

DROP TABLE IF EXISTS "actions";
CREATE TABLE "actions" (
	"action_id" SERIAL PRIMARY KEY,
	"type" varchar(64)
)
WITHOUT OIDS;
ALTER TABLE "actions" OWNER TO "metadata_admins";
GRANT SELECT ON "actions" to "metadata_readers";

DROP TABLE IF EXISTS "action_input_items";
CREATE TABLE "action_input_items" (
	"action_id" INT references actions(action_id),
	"item_id" INT references items(item_id)
)
WITHOUT OIDS;
ALTER TABLE "action_input_items" ADD CONSTRAINT action_input_items_id UNIQUE (action_id, item_id);
ALTER TABLE "action_input_items" OWNER TO "metadata_admins";
GRANT SELECT ON "action_input_items" to "metadata_readers";

DROP TABLE IF EXISTS "action_output_items";
CREATE TABLE "action_output_items" (
	"action_id" INT references actions(action_id),
	"item_id" INT references items(item_id)
)
WITHOUT OIDS;
ALTER TABLE "action_output_items" ADD CONSTRAINT action_output_items_id UNIQUE (action_id, item_id);
ALTER TABLE "action_output_items" OWNER TO "metadata_admins";
GRANT SELECT ON "action_output_items" to "metadata_readers";

DROP TABLE IF EXISTS "transactions";
CREATE TABLE "transactions" (
	"transaction" bigserial PRIMARY KEY,
	"submitter" int references eus.users(person_id),
	"stime" TIMESTAMP WITHOUT TIME ZONE,
	"verified" boolean not null default false
)
WITHOUT OIDS;
ALTER TABLE "transactions" OWNER TO "metadata_admins";
GRANT SELECT ON "transactions" to "metadata_readers";
CREATE UNIQUE INDEX transaction_idx ON transactions USING btree (transaction);
CREATE INDEX submitter_idx ON transactions USING btree (submitter);

DROP TABLE IF EXISTS "files";
CREATE TABLE "files" (
	"name" text,
	"subdir" text,
	"transaction" bigint references transactions(transaction),
	"ctime" TIMESTAMP WITHOUT TIME ZONE,
	"vtime" TIMESTAMP WITHOUT TIME ZONE default null,
	"verified" boolean not null default false,
	"aged" boolean not null default false,
	"size" bigint default null,
	item_id int references items(item_id)
)
WITHOUT OIDS;
ALTER TABLE "files" ADD CONSTRAINT itemid_unique UNIQUE (item_id);
ALTER TABLE "files" ADD CONSTRAINT filename_unique UNIQUE (name, subdir, transaction);
ALTER TABLE "files" OWNER TO "metadata_admins";
GRANT SELECT ON "files" to "metadata_readers";

DROP TABLE IF EXISTS "hashsums";
CREATE TABLE hashsums (
        item_id BIGINT REFERENCES files(item_id),
        hashtime TIMESTAMP WITHOUT TIME ZONE,
        hashsum TEXT,
	hashtype TEXT
)
WITHOUT OIDS;
ALTER TABLE "hashsums" ADD CONSTRAINT hashsum_hash_unique UNIQUE (item_id, hashtype);
ALTER TABLE "hashsums" OWNER TO "metadata_admins";
GRANT SELECT ON "hashsums" to "metadata_readers";

DROP TABLE IF EXISTS "dirs";
CREATE TABLE "dirs" (
	"name" text,
	"subdir" text
)
WITHOUT OIDS;
ALTER TABLE "dirs" ADD CONSTRAINT dirs_unique UNIQUE (name, subdir);
ALTER TABLE "dirs" OWNER TO "metadata_admins";
GRANT SELECT ON "dirs" to "metadata_readers";

DROP TABLE IF EXISTS "qrs_history";
CREATE TABLE "qrs_history" (
	"person_id" int references eus.users(person_id),
	"type" text,
	"id" int,
	"time" TIMESTAMP WITHOUT TIME ZONE default now()
)
WITHOUT OIDS;
ALTER TABLE "qrs_history" OWNER TO "metadata_admins";
GRANT SELECT ON "qrs_history" to "metadata_readers";

CREATE TYPE cart_state AS ENUM ('ingest', 'submitted', 'admin', 'admin_notified', 'downloading', 'amalgam', 'email', 'download_expiring', 'expiring', 'expired');

DROP TABLE IF EXISTS "cart";
CREATE TABLE "cart" (
	"cart_id" SERIAL PRIMARY KEY,
	"person_id" int references eus.users(person_id),
	"submit_time" TIMESTAMP WITHOUT TIME ZONE default NULL,
	"last_mtime" TIMESTAMP WITHOUT TIME ZONE default now(),
	"email_address" text,
	"state" cart_state default 'ingest' not NULL,
	"set_no" BIGINT,
	"last_email" TIMESTAMP WITHOUT TIME ZONE default NULL,
	"size" BIGINT default NULL,
	"items" INT default NULL,
	"quota" boolean not null default false
)
WITHOUT OIDS;
ALTER TABLE "cart" OWNER TO "metadata_admins";
GRANT SELECT ON "cart" to "metadata_readers";

DROP TABLE IF EXISTS "cart_items";
CREATE TABLE "cart_items" (
	"cart_id" int references myemsl.cart(cart_id),
	"item_id" bigint references myemsl.items(item_id),
	"retries" int default 0,
	"last_try" TIMESTAMP WITHOUT TIME ZONE default NULL
)
WITHOUT OIDS;
ALTER TABLE cart_items ADD CONSTRAINT cart_item_unique UNIQUE (cart_id, item_id);
ALTER TABLE "cart_items" OWNER TO "metadata_admins";
GRANT SELECT ON "cart_items" to "metadata_readers";

DROP TABLE IF EXISTS "system";
CREATE TABLE "system" (
	"key" text PRIMARY KEY,
	"value" text
)
WITHOUT OIDS;
ALTER TABLE "system" OWNER TO "metadata_admins";
GRANT SELECT ON "system" to "metadata_readers";
insert into system(key, value) values('schema_version', '1.7');


DROP TABLE IF EXISTS "notification";
CREATE TABLE "notification" (
	"person_id" integer references eus.users(person_id) on delete cascade, 
	"proposal_id" character varying(10) references eus.proposals(proposal_id) on delete cascade
)
WITHOUT OIDS;
ALTER TABLE "notification" OWNER TO "metadata_admins";
GRANT SELECT ON "notification" to "metadata_readers";

CREATE TYPE ingest_status AS ENUM ('SUCCESS', 'UNKNOWN', 'ERROR');

DROP TABLE IF EXISTS "ingest_state";
CREATE TABLE "ingest_state" (
	"host" character varying(64),
	"jobid" bigint,
	"trans_id" bigint default NULL,
	"person_id" integer references eus.users(person_id) on delete cascade,
	"step" integer default 0,
	"message" text default NULL,
	"status" ingest_status default 'UNKNOWN'
)
WITHOUT OIDS;
ALTER TABLE "ingest_state" OWNER TO "metadata_admins";
GRANT SELECT ON "ingest_state" to "metadata_readers";
CREATE INDEX transaction_idx on ingest_state using btree(trans_id);
CREATE INDEX jobhost_idx on ingest_state using btree(host, jobid);

CREATE SEQUENCE predicate_id_seq;

DROP TABLE IF EXISTS "local_predicate";
CREATE TABLE "local_predicate" (
	"id" BIGINT DEFAULT NEXTVAL('predicate_id_seq'),
	"desc" text default NULL,
	"ver" integer default 1,
	"person_id" integer references eus.users(person_id) on delete cascade
)
WITHOUT OIDS;
ALTER TABLE "local_predicate" OWNER TO "metadata_admins";
GRANT SELECT ON "local_predicate" to "metadata_readers";
ALTER TABLE "local_predicate" ADD CONSTRAINT local_predicate_uniq UNIQUE (id, ver);

DROP TABLE IF EXISTS "reprocessors";
CREATE TABLE "reprocessors" (
	"name" character varying(64),
        "person_id" integer references eus.users(person_id) on delete cascade,
	"definition" xml default NULL
)
WITHOUT OIDS;
ALTER TABLE "reprocessors" OWNER TO "metadata_admins";
GRANT SELECT ON "reprocessors" to "metadata_readers";
ALTER TABLE "reprocessors" ADD CONSTRAINT reprocessor_key UNIQUE (name, person_id);

