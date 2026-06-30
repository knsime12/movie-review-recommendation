from contextlib import contextmanager

from database import get_connection

@contextmanager
def get_db_cursor():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()