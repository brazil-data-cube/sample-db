import psycopg2
import psycopg2.extras


class Cursor(object):
    def __init__(self, pg_cursor):
        self.pg_cursor = pg_cursor

    def __del__(self):
        if self.pg_cursor:
            self.pg_cursor.close()

    def get(self):
        return self.pg_cursor


class PostgisStorager(object):
    def __init__(self, host='localhost', port=5432, username='postgres', password='', database='amostras'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._pg = None
        self._cursor = None

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        if self._cursor:
            self._cursor.close()

        if self._pg:
            self._pg.close()

    def connect(self):
        self._pg = psycopg2.connect("dbname='{4}' user='{2}' password='{3}' host='{0}' port={1}".format(
            self._host, self._port, self._username, self._password, self._database))

    def cursor(self, **kwargs):
        if self._cursor is None:
            self._cursor = self._pg.cursor(**kwargs)
        return self._cursor

    def execute(self, sql, cursor=None):
        if cursor is None:
            cursor = self.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql)
        self._pg.commit()

        return cursor.fetchall()

    def insert_many(self, sql, values):
        cursor = self.cursor()
        psycopg2.extras.execute_batch(cursor,
                                      sql,
                                      values)
        self._pg.commit()
