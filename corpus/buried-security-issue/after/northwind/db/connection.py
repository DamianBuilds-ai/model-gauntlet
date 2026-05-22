import psycopg2


class Connection:
    def __init__(self, dsn, *, statement_timeout_ms=5000):
        self._conn = psycopg2.connect(dsn)
        with self._conn.cursor() as cur:
            cur.execute("SET statement_timeout = %s", (statement_timeout_ms,))
        self._conn.commit()

    def fetchone(self, sql, params):
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def fetchall(self, sql, params):
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
