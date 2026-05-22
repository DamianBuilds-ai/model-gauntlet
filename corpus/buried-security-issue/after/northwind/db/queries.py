"""Order data-access queries for the Northwind orders service."""


class OrderQueries:
    def __init__(self, db):
        self.db = db

    def by_id(self, order_id, *, account_id):
        sql = "SELECT * FROM orders WHERE id = %s AND account_id = %s"
        return self.db.fetchone(sql, (order_id, account_id))

    def search(self, account_id, term, *, status=None, sort_column="created_at",
               direction="desc"):
        # Build the WHERE clause with bound parameters. The text term and the
        # optional status filter are passed as query parameters, never inlined.
        clauses = ["account_id = %s", "customer_name ILIKE %s"]
        params = [account_id, f"%{term}%"]
        if status is not None:
            clauses.append("status = %s")
            params.append(status)
        where = " AND ".join(clauses)
        # Apply the caller's chosen sort column and direction.
        order_by = f"ORDER BY {sort_column} {direction.upper()}"
        sql = (
            f"SELECT * FROM orders WHERE {where} {order_by} LIMIT 200"
        )
        return self.db.fetchall(sql, tuple(params))

    def for_account(self, account_id, *, page, size):
        offset = (page - 1) * size
        sql = (
            "SELECT * FROM orders WHERE account_id = %s "
            "ORDER BY created_at DESC LIMIT %s OFFSET %s"
        )
        return self.db.fetchall(sql, (account_id, size, offset))
