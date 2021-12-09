--SQL script for creating inital tables.

create table if not exists items(
	itemID serial primary key,
	purchaseLink text,
	itemDesc text,
	priority smallint default 10,
	thumbnail varchar(1024),
	QTYDesired smallint default 1
);

create table if not exists users(
	userID serial primary key,
	PWhash text not null,
	username varchar(256) not null unique,
	privLevel smallint default 0
);

create table if not exists purchase(
	purchaseID serial primary key,
	QTYpurchased smallint default 1,
	datePurchased timestamp,
	userID integer,
	itemID integer not null,
	constraint userid_record foreign key (userID) references users (userID),
	constraint itemid_record foreign key (itemID) references items (itemID)
);

--for assignment reqs, might move this into a config file later
create table if not exists setting(
	field varchar(64) primary key,
	value text
);

insert into setting(field, value) values
	('usersCanSeeAlreadyPurchased', 'true'),
	('theme', 'dark');

create extension if not exists pgcrypto;

insert into users (PWhash, username, privlevel) values
	(crypt('badPasword', gen_salt('bf')), 'admin', 0), --userID 1
