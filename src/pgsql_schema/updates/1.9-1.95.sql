CREATE INDEX  idx_group_types ON groups USING btree("type" ASC);
ALTER TABLE groups CLUSTER ON idx_group_types;
CREATE INDEX  idx_group_names ON groups USING btree("name" ASC);


ALTER TABLE "group_items" CLUSTER ON group_items_id_idx;
CREATE INDEX  group_items_id_idx ON "group_items" USING btree(group_id ASC);


CREATE INDEX  "idx_f_item_id" ON "files" USING btree(item_id ASC NULLS LAST);
CREATE INDEX  "idx_f_filename" ON "files" USING btree("name" ASC NULLS LAST);
CREATE INDEX  "idx_f_trans_id" ON "files" USING btree("transaction" DESC NULLS LAST);
ALTER TABLE "files" CLUSTER ON "idx_f_trans_id";


ALTER TABLE "hashsums" ALTER COLUMN "item_id" SET NOT NULL;
ALTER TABLE "hashsums" ADD PRIMARY KEY ("item_id");
CREATE INDEX  "idx_hs_hashes" ON "hashsums" USING btree(hashsum ASC);


CREATE INDEX  "idx_c_person_id_c" ON "cart" USING btree(person_id ASC);
ALTER TABLE "cart" CLUSTER ON "idx_c_person_id_c";


CREATE INDEX  "idx_ci_items" ON "cart_items" USING btree(item_id);
CREATE INDEX  "idx_ci_carts" ON "cart_items" USING btree(cart_id);
ALTER TABLE "cart_items" CLUSTER ON "idx_ci_carts";


ALTER TABLE "myemsl"."ingest_state" 
  ADD COLUMN "created" timestamptz NOT NULL DEFAULT now(),
	ADD COLUMN "updated" timestamptz NOT NULL;
	
	
CREATE INDEX  idx_is_job_id ON "ingest_state" USING btree(jobid ASC);


UPDATE "myemsl"."system" set value = '1.95' where key = 'schema_version';
