--SQL script for creating inital tables.


create table if not exists items(
	itemID serial,
	purchaseLink varchar(512),
	itemDesc varchar(256),
	priority smallint default 10,
	thumbnail varchar(1024),
	QTYDesired smallint default 1,
	constraint items_pkey primary key (itemID)
);

create table if not exists users(
	userID serial,
	PWhash varchar(128) not null,
	email varchar(256) not null,
	privLevel smallint default 0,
	constraint users_pkey primary key (userID)
);

create table if not exists purchase(
	purchaseID serial,
	QTYpurchased smallint defualt 1,
	datePurchased timestamp,
	userID integer,
	itemID integer not null,
	constraint purchase_pkey primary key (purchaseID),
	constraint userid_record foreign key (userID) references users (userID)
	constraint userid_record foreign key (itemID) references items (itemID)
);

--for assignment reqs, might move this into a config file later
create table if not exists setting(
	field varchar(64),
	value varchar(256),
	constraint setting_pkey primary key (purchaseID)
);
