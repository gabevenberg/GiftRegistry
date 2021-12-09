#handles connecting to the database and running queries
import psycopg2
import psycopg2.extras

class appDatabase:
    #if you dont need to set these, pass empty strings. Seems to work just fine.
    def __init__(self, host, name, user, password, port):
        self.conn=psycopg2.connect(host=host, dbname=name, user=user, password=password, port=port)

    def cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    def close(self):
        self.conn.close()

    #TODO! get query working. Currently only returns items with at least one purchase.
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
            return cur.fetchall()
