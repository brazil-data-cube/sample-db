import psycopg2
import psycopg2.extras


class Postgis(object):
    def __init__(self, host='localhost', port=5432, username='postgres', password='', database='amostras'):
        self._uri = "dbname='{}' user='{}' password='{}' host='{}' port={}".format(
            database, username, password, host, port)
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
        """
        Connect to the PostgreSQL database. It may throw ConnectionError
        :return:
        """
        self._pg = psycopg2.connect(self._uri)

    def cursor(self, **kwargs):
        # TODO: Should create multiple cursor connections?
        if self._cursor is None:
            self._cursor = self._pg.cursor(**kwargs)
        return self._cursor

    def execute(self, sql, cursor=None):
        """
        Executes SQL on current database session and retrieve the affected result.
        When `cursor` is `None`, creates a new one with `psycopg2.extras.DictCursor` as factory handling.

        :param sql: Query SQL Statement
        :param cursor: Active PostgreSQL Cursor
        :returns Query Result set. It may not return `Dict` of values when using different cursor
        """
        if cursor is None:
            cursor = self.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql)
        self._pg.commit()

        return cursor.fetchall()

    def insert_many(self, sql, values):
        """
        Allows to insert multiple rows in same query.

        :param sql: Query SQL statement
        :param values: Array of dict values to insert
        """
        cursor = self.cursor()
        psycopg2.extras.execute_batch(cursor,
                                      sql,
                                      values)
        self._pg.commit()
