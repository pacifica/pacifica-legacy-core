SET search_path = eus, myemsl, public;

insert into myemsl.groups(group_id, name, type) values(1, 'l3724', 'bruce');
insert into myemsl.groups(group_id, name, type) values(2, 'l3849', 'bruce');
insert into myemsl.groups(group_id, name, type) values(3, '23812', 'bruce');
insert into myemsl.groups(group_id, name, type) values(4, '', 'proposal');

insert into myemsl.subgroups(parent_id, child_id) values(4, 1);
insert into myemsl.subgroups(parent_id, child_id) values(4, 2);
insert into myemsl.subgroups(parent_id, child_id) values(4, 3);

insert into myemsl.items(item_id, transaction, type) values(1, 2, 'file');
insert into myemsl.items(item_id, transaction, type) values(2, 2, 'file');
insert into myemsl.items(item_id, transaction, type) values(3, 2, 'file');

insert into myemsl.group_items(group_id, item_id) values(1, 1);
insert into myemsl.group_items(group_id, item_id) values(2, 2);
insert into myemsl.group_items(group_id, item_id) values(4, 3);

update eus.proposals set group_id = 4 where proposal_id = '12190';

