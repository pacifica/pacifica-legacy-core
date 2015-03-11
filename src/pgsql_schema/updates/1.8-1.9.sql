DROP TABLE "eus"."emsl_staff_inst";
CREATE TABLE "eus"."emsl_staff_inst" (
        "instrument_id" int4 NOT NULL,
        "person_id" int4 NOT NULL
)
WITHOUT OIDS;

CREATE INDEX emsl_staff_inst_i_idx on "eus"."emsl_staff_inst" using btree(instrument_id);
CREATE INDEX emsl_staff_inst_p_idx on "eus"."emsl_staff_inst" using btree(person_id);

ALTER TABLE "eus"."emsl_staff_inst" OWNER TO "metadata_admins";
GRANT SELECT ON "eus"."emsl_staff_inst" to "metadata_readers";

update myemsl.system set value = '1.8' where key = 'schema_version';
