import pymysql


class BaseDAO:
    def __init__(self, conn: pymysql.connections.Connection):
        self.conn = conn

    def _find_one_by_parameters(self, query: str, parameters: tuple) -> dict:
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchone()

    def _execute(self, query: str, parameters: tuple) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(query, parameters)
            last_row = cursor.lastrowid
        return last_row
