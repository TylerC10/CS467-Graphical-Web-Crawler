import logging
import psycopg2
import psycopg2.extensions

from errors import PersistenceExecuteError
from errors import PersistenceConnectionError
import logging

# add inherent unicode support
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class Postgres(object):
    def __init__(self, dsn=None, database=None, user=None, password=None,
                 host='127.0.0.1', port='5432'):
        self._conn_params = {
            'dsn': dsn,
            'database': database,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self._conn = None

    def connect(self, autocommit=False):
        if not self.is_conn_alive():
            try:
                self._conn = psycopg2.connect(**self._conn_params)
                logging.info('DB Connection Established')
                self._conn.autocommit = autocommit
                self._conn.set_client_encoding('utf8')
                self._cursor = self._conn.cursor()
            except psycopg2.Error as err:
                logging.info('DB Connection establishment failed')
                raise PersistenceConnectionError(code=err.pgcode, msg=err.pgerror)

    def is_conn_alive(self):
        return self._conn is not None and self._conn.closed == 0

    def insert(self, table, values_dict):
        self._ensureConnection()

        # create query
        columns = ','.join(values_dict.keys())
        values_placeholder = ','.join(('%s', ) * len(values_dict))
        query = 'INSERT INTO %s (%s) VALUES (%s);' \
            %(table, columns, values_placeholder)

        # execute
        try:
            self._cursor.execute(query, values_dict.values())
        except psycopg2.Error as err:
            logging.info('Insert Query execution failed')
            raise PersistenceExecuteError(code=err.pgcode, msg=err.pgerror)

        # return the number of rows affected
        return self._cursor.rowcount

    def commit(self):
        self._assertConnection()
        self._conn.commit()

    def rollback(self):
        self._assertConnection()
        self._conn.rollback()

    def close(self):
        self._assertConnection()
        self._cursor.close()
        self._conn.close()
        logging.info('Connection Closed')

    def _assertConnection(self):
        if not self.is_conn_alive():
            raise PersistenceConnectionError(msg='Unable to perform ' \
                'operation. Connection is not alive')

    def _ensureConnection(self):
        if not self.is_conn_alive():
            self.connect()
