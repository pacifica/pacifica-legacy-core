BEGIN TRANSACTION;

-- ----------------------------
--  View structure for v_instrument_groupings
-- ----------------------------
DROP VIEW IF EXISTS "eus"."v_instrument_groupings";
CREATE VIEW "eus"."v_instrument_groupings" AS  SELECT
        CASE
            WHEN (strpos((i.instrument_name)::text, ':'::text) > 0) THEN rtrim(substr((i.instrument_name)::text, 1, strpos((i.instrument_name)::text, ':'::text)), ':'::text)
            ELSE 'Miscellaneous'::text
        END AS instrument_grouping,
        CASE
            WHEN (strpos((i.instrument_name)::text, ':'::text) > 0) THEN (ltrim(substr((i.instrument_name)::text, strpos((i.instrument_name)::text, ':'::text)), ' :'::text))::character varying
            ELSE i.instrument_name
        END AS instrument_name,
    i.instrument_id,
        CASE
            WHEN (strpos((i.name_short)::text, ':'::text) > 0) THEN (ltrim(substr((i.name_short)::text, strpos((i.name_short)::text, ':'::text)), ' :'::text))::character varying
            ELSE i.name_short
        END AS name_short
   FROM "eus"."instruments" i
  WHERE (i.active_sw = 'Y'::bpchar)
  ORDER BY
        CASE
            WHEN (strpos((i.instrument_name)::text, ':'::text) > 0) THEN rtrim(substr((i.instrument_name)::text, 1, strpos((i.instrument_name)::text, ':'::text)), ':'::text)
            ELSE 'Miscellaneous'::text
        END,
        CASE
            WHEN (strpos((i.instrument_name)::text, ':'::text) > 0) THEN (ltrim(substr((i.instrument_name)::text, strpos((i.instrument_name)::text, ':'::text)), ' :'::text))::character varying
            ELSE i.instrument_name
        END;

-- ----------------------------
--  View structure for v_instrument_search
-- ----------------------------
DROP VIEW IF EXISTS "eus"."v_instrument_search";
CREATE VIEW "eus"."v_instrument_search" AS  SELECT ig.instrument_id AS id,
    ((((('['::text || COALESCE(ig.instrument_grouping, 'None'::text)) || ' / ID:'::text) || ig.instrument_id) || '] '::text) || (ig.instrument_name)::text) AS display_name,
    lower(((((((COALESCE(ig.instrument_grouping, 'None'::text) || '|'::text) || ig.instrument_id) || '|'::text) || (ig.instrument_name)::text) || '|'::text) || (ig.name_short)::text)) AS search_field,
    ((COALESCE(ig.instrument_grouping, 'None'::text) || '|'::text) || (ig.instrument_name)::text) AS order_field,
    COALESCE(ig.instrument_grouping, 'None'::text) AS category,
    COALESCE(ig.name_short, ig.instrument_name) AS abbreviation
   FROM "eus"."v_instrument_groupings" ig;

-- ----------------------------
--  View structure for v_proposal_search
-- ----------------------------
DROP VIEW IF EXISTS "eus"."v_proposal_search";
CREATE VIEW "eus"."v_proposal_search" AS  SELECT p.proposal_id AS id,
    ((('[Proposal '::text || (p.proposal_id)::text) || '] '::text) || (COALESCE(p.title, '<Title Unspecified>'::character varying))::text) AS display_name,
    lower(((p.proposal_id)::text ||
        CASE
            WHEN (p.title IS NOT NULL) THEN ('|'::text || (p.title)::text)
            ELSE ''::text
        END)) AS search_field,
    COALESCE(p.title, '<Proposal Title Unspecified>'::character varying) AS order_field,
    COALESCE((date_part('year'::text, p.actual_end_date))::text, 'Unknown'::text) AS category,
    ('Proposal #'::text || (p.proposal_id)::text) AS abbreviation
   FROM "eus"."proposals" p;

-- ----------------------------
--  View structure for v_user_search
-- ----------------------------
DROP VIEW IF EXISTS "eus"."v_user_search";
CREATE VIEW "eus"."v_user_search" AS  SELECT u.person_id AS id,
    ((((((('[EUS ID '::text || u.person_id) || '] '::text) ||
        CASE
            WHEN (u.first_name IS NOT NULL) THEN ((u.first_name)::text || ' '::text)
            ELSE ''::text
        END) ||
        CASE
            WHEN (u.last_name IS NOT NULL) THEN ((u.last_name)::text || ' '::text)
            ELSE ''::text
        END) || '&lt;'::text) || (u.email_address)::text) || '&gt;'::text) AS display_name,
    lower(((((u.person_id || '|'::text) ||
        CASE
            WHEN (u.first_name IS NOT NULL) THEN ((u.first_name)::text || ' '::text)
            ELSE ''::text
        END) ||
        CASE
            WHEN (u.last_name IS NOT NULL) THEN ((u.last_name)::text || ' '::text)
            ELSE ''::text
        END) || (u.email_address)::text)) AS search_field,
    ((
        CASE
            WHEN (u.last_name IS NOT NULL) THEN ((u.last_name)::text || ' '::text)
            ELSE ''::text
        END ||
        CASE
            WHEN (u.first_name IS NOT NULL) THEN ((u.first_name)::text || ' '::text)
            ELSE ''::text
        END) || (u.email_address)::text) AS order_field,
    COALESCE("left"(upper((u.last_name)::text), 1), "left"(upper((u.email_address)::text), 1)) AS category,
        CASE
            WHEN ((u.first_name IS NULL) AND (u.last_name IS NULL)) THEN (u.email_address)::text
            ELSE (
            CASE
                WHEN (u.first_name IS NOT NULL) THEN ((u.first_name)::text || ' '::text)
                ELSE ''::text
            END || (
            CASE
                WHEN (u.last_name IS NOT NULL) THEN u.last_name
                ELSE ''::character varying
            END)::text)
        END AS abbreviation
		FROM "eus"."users" u;
		
UPDATE "myemsl"."system" SET "value" = '1.13' WHERE "key" = 'schema_version';
		
COMMIT;