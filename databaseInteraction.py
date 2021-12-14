#handles connecting to the database and running queries
import psycopg2
import psycopg2.extras
import logging
import WeddingRegistryGUI as wrg

logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

class appDatabase:
    #if you dont need to set these, pass empty strings. Seems to work just fine.
    def __init__(self, host, name, user, password, port):
        self.conn=psycopg2.connect(host=host, dbname=name, user=user, password=password, port=port)

    def cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    def close(self):
        self.conn.close()

    def getUnpurchasedGifts(self):
        with self.cursor() as cur:
            cur.execute('''
                select * from (
                select items.itemID, itemdesc, priority, (qtydesired - coalesce(sum(qtypurchased),0)) as qtyleft, thumbnail, purchaselink
                from items left join purchase on items.itemid=purchase.itemid
                group by items.itemID, itemdesc, priority, qtydesired, purchaselink, thumbnail
                order by priority
                ) as getsum
                where qtyleft>0;
            ''')
            self.conn.commit()
            return cur.fetchall()
    def fitlerByName(self,name):
         with self.cursor() as cur:
            cur.execute('''
                select * from (
                select items.itemID, itemdesc, priority, (qtydesired - coalesce(sum(qtypurchased),0)) as qtyleft, thumbnail, purchaselink
                from items left join purchase on items.itemid=purchase.itemid
                group by items.itemID, itemdesc, priority, qtydesired, purchaselink, thumbnail
                order by priority
                ) as getsum
                where qtyleft>0 and itemdesc like %s;
            ''', (name,))
            self.conn.commit()
            return cur.fetchall()
    def sortEntries(self,field,order):
        enum_to_field={
                1:"items.itemID",
                2:"itemdesc",
                3:"priority",
                4:"qtyleft"
            }
        enum_to_order={
                1:"asc",
                2:"desc"
            }
        field_name=enum_to_field[field]
        order_name=enum_to_order[order]
        with self.cursor() as cur:
            cur.execute('''
                select * from (
                select items.itemID, itemdesc, priority, (qtydesired - coalesce(sum(qtypurchased),0)) as qtyleft, thumbnail, purchaselink
                from items left join purchase on items.itemid=purchase.itemid
                group by items.itemID, itemdesc, priority, qtydesired, purchaselink, thumbnail
                order by %s asc
                ) as getsum
                where qtyleft>0 ;
            ''' ,(field_name,))
        self.conn.commit()
        return cur.fetchall()

    def filterByPriority(self,priority):
        int_priority=int(priority)
        with self.cursor() as cur:
            cur.execute('''
                select * from (
                select items.itemID, itemdesc, priority, (qtydesired - coalesce(sum(qtypurchased),0)) as qtyleft, thumbnail, purchaselink
                from items left join purchase on items.itemid=purchase.itemid
                group by items.itemID, itemdesc, priority, qtydesired, purchaselink, thumbnail
                ) as getsum
                where qtyleft>0 and priority <=%s;
            ''', (priority,))
        self.conn.commit()
        return cur.fetchall()

    def filterByPrice(self,upper_price,lower_price):
        int_upper=int(upper_price)
        int_lower=int(lower_price)

        with self.cursor() as cur:
            cur.execute('''
                select * from (
                select items.itemID, itemdesc, priority, (qtydesired - coalesce(sum(qtypurchased),0)) as qtyleft, thumbnail, purchaselink
                from items left join purchase on items.itemid=purchase.itemid
                group by items.itemID, itemdesc, priority, qtydesired, purchaselink, thumbnail
                order by priority
                ) as getsum
                where qtyleft>0 and price<=%s and price>=%s;
            ''', (upper_price, lower_price,))
            self.conn.commit()
            return cur.fetchall()
    #returns purchaseID
    def purchaseItem(self, itemID, userID, qtyPurchased):
        with self.cursor() as cur:
            cur.execute('''
                insert into purchase (itemID, userID, QTYpurchased, datePurchased)
                values (%s, %s, %s, current_timestamp) returning purchaseid;
                ''', (itemID, userID, qtyPurchased))
            logging.debug(f'inserted {itemID}, {userID}, {qtyPurchased} into purchase database')
            self.conn.commit()
            return cur.fetchone().purchaseid
    
    #returns boolean and the userid belonging to the username
    def validateUser(self, username, password):
        with self.cursor() as cur:
            cur.execute('''
            select pwhash=crypt(%s, pwhash) as verified, userid from users
            where username=%s;
            ''', (password, username))
            res=cur.fetchone()
            self.conn.commit()
            return res.verified, res.userid

    #returns integer detailing users privLevel.
    def getPrivLevel(self, userID):
        with self.cursor() as cur:
            cur.execute('''
            select privlevel from users where userid=%s
            ''', (userID,))
            self.conn.commit()
            return cur.fetchone().privlevel
    

    #returns the userID of the new user
    def addUser(self, password, username, privLevel):
        with self.cursor() as cur:
            cur.execute('''
            insert into users (pwhash, username, privlevel)
            values (%s, %s, %s) returning userID
            ''', (password, username, privLevel))
            self.conn.commit()
            logging.debug(f'inserted {username}, {privLevel} into users table')
            return cur.fetchone().userid

    #returns the itemID of the new item
    def addItem(self, itemDescription, priority, qtyDesired, purchaseLink, thumbnailPath):
        with self.cursor() as cur:
            cur.execute('''
            insert into items (itemdesc, priority, qtydesired, purchaselink, thumbnail)
            values (%s, %s, %s, %s, %s) returning itemid;
            ''', (itemDescription, priority, qtyDesired, purchaseLink, thumbnailPath))
            self.conn.commit()
            logging.debug(f'inserted {itemDescription}, {priority}, {qtyDesired}, {purchaseLink}, {thumbnailPath} into items table')
            return cur.fetchone().itemid

    #test function, please ignore
    #NOTE will destroy your database!!! used only to reset to known state between tests.
    def populateWithTestData(self):
        with self.cursor() as cur:
            cur.execute('''
                --SQL script for creating test data.

                drop table if exists items cascade;
                drop table if exists users cascade;
                drop table if exists purchase cascade;
                drop table if exists setting cascade;

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
                    (crypt('IWillTellLiesForPi', gen_salt('bf')), 'giftEditor', 1), --userID 2
                    (crypt('IAmAInlaw', gen_salt('bf')), 'giftBuyer', 100); --userID 3

                insert into items (purchaseLink, itemDesc, priority, QTYDesired) values
                    ('https://smile.amazon.com/upsimples-Picture-Display-Pictures-Without/dp/B07VQZSLDW/', '11x14 Picture Frames', 5, 2), --itemID 1
                    ('https://smile.amazon.com/Zinus-Ironline-Platform-Headboard-Optional/dp/B075FGY7G2/', 'Queen size bed frame', 1, 1), --itemID 2
                    ('https://www.betterworldbooks.com/product/detail/Dune-9780441013593', 'Dune, by frank herbert', 2, 1), -- itemID 3
                    ('https://www.target.com/p/0-4-34-x-1-5-34-12pk-unscented-tealight-candle-set-white-made-by-design-8482/-/A-54518130', 'Tealight candles', 5, 5); --itemID 4

                insert into purchase (QTYpurchased, datePurchased, userID, itemID) values
                    (1, timestamp '2021-12-05 13:25:12', 3, 1),
                    (1, timestamp '2021-12-05 13:25:60', 3, 1),
                    (1, timestamp '2021-11-12 10:36:49', 3, 4),
                    (2, timestamp '2021-11-12 10:36:50', 3, 4);
                ''')
            self.conn.commit()
