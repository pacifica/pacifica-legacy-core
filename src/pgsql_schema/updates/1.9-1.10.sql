CREATE INDEX  idx_group_types ON "myemsl"."groups" USING btree("type" ASC);
ALTER TABLE "myemsl"."groups" CLUSTER ON idx_group_types;
CREATE INDEX  idx_group_names ON "myemsl"."groups" USING btree("name" ASC);


CREATE INDEX  group_items_id_idx ON "myemsl"."group_items" USING btree(group_id ASC);
ALTER TABLE "myemsl"."group_items" CLUSTER ON group_items_id_idx;


CREATE INDEX  "idx_f_item_id" ON "myemsl"."files" USING btree(item_id ASC NULLS LAST);
CREATE INDEX  "idx_f_filename" ON "myemsl"."files" USING btree("name" ASC NULLS LAST);
CREATE INDEX  "idx_f_trans_id" ON "myemsl"."files" USING btree("transaction" DESC NULLS LAST);
ALTER TABLE "myemsl"."files" CLUSTER ON "idx_f_trans_id";


ALTER TABLE "myemsl"."hashsums" ALTER COLUMN "item_id" SET NOT NULL;
ALTER TABLE "myemsl"."hashsums" ADD PRIMARY KEY ("item_id");
CREATE INDEX  "idx_hs_hashes" ON "myemsl"."hashsums" USING btree(hashsum ASC);


CREATE INDEX  "idx_c_person_id_c" ON "myemsl"."cart" USING btree(person_id ASC);
ALTER TABLE "myemsl"."cart" CLUSTER ON "idx_c_person_id_c";


CREATE INDEX  "idx_ci_items" ON "myemsl"."cart_items" USING btree(item_id);
CREATE INDEX  "idx_ci_carts" ON "myemsl"."cart_items" USING btree(cart_id);
ALTER TABLE "myemsl"."cart_items" CLUSTER ON "idx_ci_carts";


ALTER TABLE "myemsl"."ingest_state" 
  ADD COLUMN "created" timestamptz NOT NULL DEFAULT now(),
	ADD COLUMN "updated" timestamptz NOT NULL;
	
	
CREATE INDEX  idx_is_job_id ON "myemsl"."ingest_state" USING btree(jobid ASC);

ALTER TABLE "myemsl"."files"
  ADD COLUMN "mtime" TIMESTAMP WITHOUT TIME ZONE;

UPDATE "myemsl"."system" set value = '1.10' where key = 'schema_version';
