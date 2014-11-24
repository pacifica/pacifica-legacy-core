ALTER TABLE eus.proposals add column actual_end_date date;
CREATE INDEX proposal_actual_end_date_idx on eus.proposals USING btree(actual_end_date);
ALTER TABLE eus.proposals add column actual_start_date date;
CREATE INDEX proposal_actual_start_date_idx on eus.proposals USING btree(actual_start_date);
ALTER TABLE eus.proposals add column closed_date date;
CREATE INDEX proposal_closed_date_idx on eus.proposals USING btree(closed_date);
ALTER TABLE eus.instruments add column active_sw character default 'Y';
CREATE INDEX instrument_active_sw_idx on eus.instruments USING btree(active_sw);

update myemsl.system set value = '1.7' where key = 'schema_version';

