from contextlib import contextmanager

import pymysql


@contextmanager
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        database="process-engine",
        user="camunda",
        password="camunda",
    )
    try:
        yield conn
    finally:
        conn.close()
