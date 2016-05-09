DROP TABLE "eus"."proposal_pocs";
CREATE TABLE "eus"."proposal_pocs" (
        "proposal_poc_id int4 NOT NULL,
        "poc_employee_id" varchar(10) NOT NULL,
        "proposal_id" varchar(10) NOT NULL,
        "last_change_date" timestamptz NOT NULL DEFAULT now()
)
WITHOUT OIDS;

CREATE INDEX emsl_proposal_pocs_i_idx on "eus"."proposal_pocs" using btree(proposal_poc_id);
CREATE INDEX emsl_proposal_pocs_e_idx on "eus"."proposal_pocs" using btree(poc_employee_id);
CREATE INDEX emsl_proposal_pocs_p_idx on "eus"."proposal_pocs" using btree(proposal_id);

ALTER TABLE "eus"."proposal_pocs" OWNER TO "metadata_admins";
GRANT SELECT ON "eus"."proposal_pocs" to "metadata_readers";

UPDATE "myemsl"."system" set value = '1.11' where key = 'schema_version';
