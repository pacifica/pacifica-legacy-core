DROP TABLE "emsl_staff_inst";
CREATE TABLE "emsl_staff_inst" (
        "instrument_id" int4 NOT NULL,
        "person_id" int4 NOT NULL
)
WITHOUT OIDS;
ALTER TABLE "emsl_staff_inst" OWNER TO "metadata_admins";
GRANT SELECT ON "emsl_staff_inst" to "metadata_readers";

update myemsl.system set value = '1.8' where key = 'schema_version';
