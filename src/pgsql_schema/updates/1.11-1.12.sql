BEGIN TRANSACTION;

DROP FUNCTION IF EXISTS fill_item_time_cache_by_transaction(bigint);
CREATE FUNCTION "myemsl"."fill_item_time_cache_by_transaction"(IN transaction_id int8) RETURNS "int4"
	AS $BODY$
DECLARE
	inserted_record_count int;
BEGIN
	RAISE NOTICE 'Loading file info for transaction % into item_time_cache_by_transaction table', transaction_id;
	INSERT INTO item_time_cache_by_transaction
	SELECT f.item_id,
			t.transaction,
			date_trunc('day'::text, t.stime)::date AS submit_date,
			date_trunc('day'::text, f.ctime)::date AS created_date,
			date_trunc('day'::text, f.mtime)::date AS modified_date,
			f.size AS size_in_bytes,
			t.submitter,
			gi.group_id,
			CASE
				when (g.type = 'omics.dms.instrument_id' or g.type ilike 'instrument.%') THEN 'instrument'
				when (g.type = 'EMSL User') THEN 'user'
				when (g.type = 'proposal') THEN 'proposal'
			END
			as group_type
		 FROM myemsl.transactions t
			 JOIN myemsl.files f ON f.transaction = t.transaction
			 JOIN myemsl.group_items gi ON gi.item_id = f.item_id
			 JOIN myemsl.groups g on g.group_id = gi.group_id
		 WHERE 	(g.type in(
			'omics.dms.instrument_id',
			'EMSL User',
			'proposal'
			) OR g . type ilike 'instrument%') AND t.transaction = transaction_id;
	GET DIAGNOSTICS inserted_record_count = ROW_COUNT;
	RETURN inserted_record_count;
END;
$BODY$
	LANGUAGE plpgsql
	COST 100
	CALLED ON NULL INPUT
	SECURITY DEFINER
	VOLATILE;
	
	
DROP FUNCTION IF EXISTS fill_item_cache_from_txn_table();
CREATE FUNCTION "myemsl"."fill_item_cache_from_txn_table"() RETURNS "int4"
	AS $BODY$
DECLARE
	item_entry RECORD;
	transaction_count INTEGER;
	current_transaction_count INTEGER;
	running_item_count INTEGER;
	item_row_count INTEGER;
	trans_id INTEGER;
	percent_complete INTEGER;
BEGIN
	SELECT INTO transaction_count
		COUNT("transaction")
		FROM myemsl.transactions
	WHERE "transaction" NOT IN (SELECT "transaction" FROM myemsl.item_time_cache_by_transaction);

	RAISE NOTICE 'Found % transactions for processing',transaction_count;

	FOR item_entry in SELECT "transaction"
		FROM myemsl.transactions
		WHERE "transaction" NOT IN (SELECT "transaction" FROM myemsl.item_time_cache_by_transaction)
		ORDER BY "transaction"
		LIMIT 50
	LOOP
		trans_id = item_entry.transaction;
		SELECT myemsl.fill_item_time_cache_by_transaction(trans_id) INTO item_row_count;
		RAISE NOTICE 'Processed % rows from transaction %',item_row_count,trans_id;
	END LOOP;

RETURN trans_id;

END;
	$BODY$
	LANGUAGE plpgsql
	COST 100
	CALLED ON NULL INPUT
	SECURITY INVOKER
	VOLATILE;

CREATE TABLE "myemsl"."item_time_cache_by_transaction" (
	"item_id" int4 NOT NULL,
	"transaction" int8,
	"submit_date" date,
	"create_date" date,
	"modified_date" date,
	"size_in_bytes" int8,
	"submitter" int4,
	"group_id" int4 NOT NULL,
	"group_type" text COLLATE "default"
)
WITH (OIDS=FALSE);

CREATE INDEX  "idx_ing_person" ON "myemsl"."ingest_state" USING btree(person_id "pg_catalog"."int4_ops" ASC NULLS LAST);
CREATE INDEX  "idx_ing_trans_id" ON "myemsl"."ingest_state" USING btree(trans_id "pg_catalog"."int8_ops" ASC NULLS LAST);
CREATE INDEX  "idx_ing_trans_id_sub" ON "myemsl"."ingest_state" USING btree(trans_id "pg_catalog"."int8_ops" ASC NULLS LAST, person_id "pg_catalog"."int4_ops" ASC NULLS LAST);
CREATE INDEX  "idx_group_id_name" ON "myemsl"."groups" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST, "name" COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST);
CREATE INDEX  "idx_group_id_type" ON "myemsl"."groups" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST, "type" COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST);
CREATE INDEX  "idx_group_name_type" ON "myemsl"."groups" USING btree("name" COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST, "type" COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST);
CREATE INDEX  "gi_idx_item_group" ON "myemsl"."group_items" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST, item_id "pg_catalog"."int4_ops" ASC NULLS LAST);
CREATE INDEX  "idx_f_ctime" ON "myemsl"."files" USING btree(ctime "pg_catalog"."timestamp_ops" ASC NULLS LAST);
CREATE INDEX  "idx_f_ctime_desc" ON "myemsl"."files" USING btree(ctime "pg_catalog"."timestamp_ops" DESC NULLS LAST);
CREATE UNIQUE INDEX  "idx_f_ctime_item_id" ON "myemsl"."files" USING btree(ctime "pg_catalog"."timestamp_ops" ASC NULLS LAST, item_id "pg_catalog"."int4_ops" ASC NULLS LAST);
CREATE INDEX  "t_stime_idx" ON "myemsl"."transactions" USING btree(stime "pg_catalog"."timestamp_ops" ASC NULLS LAST);

ALTER TABLE "myemsl"."item_time_cache_by_transaction" ADD PRIMARY KEY ("item_id", "group_id") NOT DEFERRABLE INITIALLY IMMEDIATE;

CREATE INDEX  "idx_item_time_cache_cdate" ON "myemsl"."item_time_cache_by_transaction" USING btree(create_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_item_time_cache_group_id" ON "myemsl"."item_time_cache_by_transaction" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST);
ALTER TABLE "myemsl"."item_time_cache_by_transaction" CLUSTER ON "idx_item_time_cache_group_id";
CREATE INDEX  "idx_item_time_cache_mdate" ON "myemsl"."item_time_cache_by_transaction" USING btree(modified_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_item_time_cache_sdate" ON "myemsl"."item_time_cache_by_transaction" USING btree(submit_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_item_time_cache_txn" ON "myemsl"."item_time_cache_by_transaction" USING btree("transaction" "pg_catalog"."int8_ops" ASC NULLS LAST);
CREATE INDEX  "idx_mtime_group_id" ON "myemsl"."item_time_cache_by_transaction" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST, modified_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_mtime_transaction" ON "myemsl"."item_time_cache_by_transaction" USING btree("transaction" "pg_catalog"."int8_ops" ASC NULLS LAST, modified_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_stime_group_id" ON "myemsl"."item_time_cache_by_transaction" USING btree(group_id "pg_catalog"."int4_ops" ASC NULLS LAST, modified_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_stime_transaction" ON "myemsl"."item_time_cache_by_transaction" USING btree("transaction" "pg_catalog"."int8_ops" ASC NULLS LAST, submit_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_submitter" ON "myemsl"."item_time_cache_by_transaction" USING btree(submitter "pg_catalog"."int4_ops" ASC NULLS LAST);
CREATE INDEX  "idx_submitter_mtime" ON "myemsl"."item_time_cache_by_transaction" USING btree(submitter "pg_catalog"."int4_ops" ASC NULLS LAST, modified_date "pg_catalog"."date_ops" ASC NULLS LAST);
CREATE INDEX  "idx_submitter_stime" ON "myemsl"."item_time_cache_by_transaction" USING btree(submitter "pg_catalog"."int4_ops" ASC NULLS LAST, submit_date "pg_catalog"."date_ops" ASC NULLS LAST);
UPDATE "myemsl"."system" set value = '1.12' where key = 'schema_version';

ALTER TABLE "eus"."users" ADD "emsl_employee" character varying(1);

COMMIT;
