/*
 Navicat Premium Data Transfer

 Source Server         : MyEMSL
 Source Server Type    : PostgreSQL
 Source Server Version : 80122
 Source Host           : n5.emsl.pnl.gov
 Source Database       : myemsl_metadata
 Source Schema         : eus

 Target Server Type    : PostgreSQL
 Target Server Version : 80122
 File Encoding         : utf-8

 Date: 01/28/2011 11:56:09 AM
*/

-- ----------------------------
--  Table structure for "users"
-- ----------------------------
DROP TABLE "users";
CREATE TABLE "users" (
	"person_id" int4 NOT NULL,
	"network_id" varchar(96),
	"first_name" varchar(64),
	"last_name" varchar(64),
	"email_address" varchar(64),
	"last_change_date" timestamptz NOT NULL DEFAULT now()
)
WITHOUT OIDS;
ALTER TABLE "users" OWNER TO "metadata_admins";
GRANT SELECT ON "users" to "metadata_readers";

-- ----------------------------
--  Table structure for "instruments"
-- ----------------------------
DROP TABLE "instruments";
CREATE TABLE "instruments" (
	"instrument_id" int4 NOT NULL,
	"instrument_name" varchar NOT NULL,
	"last_change_date" timestamptz NOT NULL DEFAULT now(),
	"name_short" varchar(100),
	"eus_display_name" varchar
)
WITHOUT OIDS;
ALTER TABLE "instruments" OWNER TO "metadata_admins";
GRANT SELECT ON "instruments" to "metadata_readers";

-- ----------------------------
--  Table structure for "proposal_instruments"
-- ----------------------------
DROP TABLE "proposal_instruments";
CREATE TABLE "proposal_instruments" (
	"proposal_instrument_id" int4 NOT NULL,
	"instrument_id" int4 NOT NULL,
	"proposal_id" varchar(10) NOT NULL,
	"last_change_date" timestamptz NOT NULL DEFAULT now()
)
WITHOUT OIDS;
ALTER TABLE "proposal_instruments" OWNER TO "metadata_admins";
GRANT SELECT ON "proposal_instruments" to "metadata_readers";

-- ----------------------------
--  Table structure for "proposal_members"
-- ----------------------------
DROP TABLE "proposal_members";
CREATE TABLE "proposal_members" (
	"proposal_member_id" int4 NOT NULL,
	"proposal_id" varchar(10) NOT NULL DEFAULT 0,
	"person_id" int4 NOT NULL,
	"active" char(1) NOT NULL DEFAULT 'Y'::bpchar,
	"last_change_date" timestamptz NOT NULL DEFAULT now()
)
WITHOUT OIDS;
ALTER TABLE "proposal_members" OWNER TO "metadata_admins";
GRANT SELECT ON "proposal_members" to "metadata_readers";

-- ----------------------------
--  Table structure for "proposals"
-- ----------------------------
DROP TABLE "proposals";
CREATE TABLE "proposals" (
	"proposal_id" varchar(10) NOT NULL,
	"title" varchar,
	"group_id" int4,
	"accepted_date" date,
    "last_change_date" timestamptz NOT NULL DEFAULT now()
)
WITHOUT OIDS;
ALTER TABLE "proposals" OWNER TO "metadata_admins";
GRANT SELECT ON "proposals" to "metadata_readers";

-- ----------------------------
--  Primary key structure for table "users"
-- ----------------------------
ALTER TABLE "users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("person_id");

-- ----------------------------
--  Primary key structure for table "instruments"
-- ----------------------------
ALTER TABLE "instruments" ADD CONSTRAINT "instruments_pkey" PRIMARY KEY ("instrument_id");

-- ----------------------------
--  Primary key structure for table "proposal_instruments"
-- ----------------------------
ALTER TABLE "proposal_instruments" ADD CONSTRAINT "proposal_instruments_pkey" PRIMARY KEY ("proposal_instrument_id", "instrument_id", "proposal_id");

-- ----------------------------
--  Primary key structure for table "proposal_members"
-- ----------------------------
ALTER TABLE "proposal_members" ADD CONSTRAINT "proposal_members_pkey" PRIMARY KEY ("proposal_member_id", "proposal_id", "person_id");

-- ----------------------------
--  Primary key structure for table "proposals"
-- ----------------------------
ALTER TABLE "proposals" ADD CONSTRAINT "proposals_pkey" PRIMARY KEY ("proposal_id");

--
-- Name: inst_id_idx; Type: INDEX; Schema: eus; Owner: metadata_admins; Tablespace: 
--

CREATE UNIQUE INDEX inst_id_idx ON instruments USING btree (instrument_id);


--
-- Name: person_id_idx; Type: INDEX; Schema: eus; Owner: metadata_admins; Tablespace: 
--

CREATE UNIQUE INDEX person_id_idx ON users USING btree (person_id);


--
-- Name: prop_inst_idx; Type: INDEX; Schema: eus; Owner: metadata_admins; Tablespace: 
--

CREATE UNIQUE INDEX prop_inst_idx ON proposal_instruments USING btree (proposal_instrument_id);


--
-- Name: prop_memb_idx; Type: INDEX; Schema: eus; Owner: metadata_admins; Tablespace: 
--

CREATE UNIQUE INDEX prop_memb_idx ON proposal_members USING btree (proposal_id, person_id);


--
-- Name: proposal_id_idx; Type: INDEX; Schema: eus; Owner: metadata_admins; Tablespace: 
--

CREATE INDEX proposal_id_idx ON proposals USING btree (proposal_id);
CREATE INDEX proposals_group_id_idx ON proposals USING btree (group_id);

