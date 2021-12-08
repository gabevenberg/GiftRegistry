#handles connecting to the database and running queries

def connect(host, name, user, password, port):
        conn=psycopg2.connect(host=host, dbname=name, user=user, password=password, port=port)
        return conn
