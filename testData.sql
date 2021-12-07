--SQL script for creating test data.

drop table if exists items;
drop table if exists users;
drop table if exists purchase;
drop table if exists setting;

create table if not exists items(
	itemID serial primary key,
	purchaseLink text,
	itemDesc text,
	priority smallint default 10,
	thumbnail varchar(1024),
	QTYDesired smallint default 1,
);

create table if not exists users(
	userID serial primary key,
	PWhash text not null,
	username varchar(256) not null unique,
	privLevel smallint default 0,
);

create table if not exists purchase(
	purchaseID serial primary key,
	QTYpurchased smallint defualt 1,
	datePurchased timestamp,
	userID integer,
	itemID integer not null,
	constraint userid_record foreign key (userID) references users (userID)
	constraint userid_record foreign key (itemID) references items (itemID)
);

--for assignment reqs, might move this into a config file later
create table if not exists setting(
	field varchar(64) primary key,
	value text,
);

insert into setting(field, value) values
	('usersCanSeeAlreadyPurchased', 'true'),
	('theme', 'dark');

insert into users (PWhash, username, privlevel) values
	(crypt('badPasword', gen_salt('bf')), 'admin', 0) --userID 1
	(crypt('IWillTellLiesForPi', gen_salt('bf')), 'giftEditor', 1), --userID 2
	(crypt('IAmAInlaw', gen_salt('bf')), 'giftBuyer', 100); --userID 3

insert into items (purcaseLink, itemDesc, priority, QTYDesired) values
	('https://smile.amazon.com/upsimples-Picture-Display-Pictures-Without/dp/B07VQZSLDW/', '11x14 Picture Frames', 5, 2), --itemID 1
	('https://smile.amazon.com/Zinus-Ironline-Platform-Headboard-Optional/dp/B075FGY7G2/', 'Queen size bed frame', 1, 1), --itemID 2
	('https://www.betterworldbooks.com/product/detail/Dune-9780441013593', 'Dune, by frank herbert', 2, 1); -- itemID 3
	('https://www.target.com/p/0-4-34-x-1-5-34-12pk-unscented-tealight-candle-set-white-made-by-design-8482/-/A-54518130', 'Tealight candles', 5, 3); --itemID 4

insert into purchase (QTYpurchased, datePurchased, userID, itemID) values
	(1, timestamp '2021-12-05 13:25:12', 3, 1),
	(1, timestamp '2021-11-12 10:36:49', 3, 2);
