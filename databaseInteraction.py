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
            select purchaselink, itemdesc, priority, thumbnail, qtydesired, sum(qtypurchased)
            from items inner join purchase on items.itemid=purchase.itemid
            group by purchaselink, itemdesc, priority, thumbnail, qtydesired
            order by priority
            ) as getsum
            where sum<qtydesired;
            ''')
            return cur.fetchall()
