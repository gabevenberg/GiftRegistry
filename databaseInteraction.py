#handles connecting to the database and running queries
import psycopg2

class appDatabase:
    def __init__(self, host, name, user, password, port):
        self.conn=psycopg2.connect(host=host, dbname=name, user=user, password=password, port=port)
    def close(self):
        self.conn.close()
