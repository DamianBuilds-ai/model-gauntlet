"""Order data-access queries for the Northwind orders service."""


class OrderQueries:
    def __init__(self, db):
        self.db = db

    def by_id(self, order_id, *, account_id):
        sql = "SELECT * FROM orders WHERE id = %s AND account_id = %s"
        return self.db.fetchone(sql, (order_id, account_id))

    def search(self, account_id, term):
        sql = (
            "SELECT * FROM orders "
            "WHERE account_id = %s AND customer_name ILIKE %s "
            "ORDER BY created_at DESC LIMIT 200"
        )
        like = f"%{term}%"
        return self.db.fetchall(sql, (account_id, like))
