import psycopg2


class Connection:
    def __init__(self, dsn):
        self._conn = psycopg2.connect(dsn)

    def fetchone(self, sql, params):
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def fetchall(self, sql, params):
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
