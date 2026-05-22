"""Northwind Orders - persistence layer (Globex).

Raw SQL persistence for orders. The customer_ref column and the SQL strings that
reference it must move to customer_id (a BIGINT) per CR-4471. Note the SQL column
name and the bound parameter names both appear here.
"""

from __future__ import annotations

from ..models import Order  # noqa: F401  (imported for type context)


class OrderRepository:
    def __init__(self, conn) -> None:
        self._conn = conn

    def save(self, order) -> None:
        # The customer_ref column is TEXT today; CR-4471 makes it BIGINT and the
        # column name becomes customer_id.
        self._conn.execute(
            """
            INSERT INTO orders (order_ref, customer_ref, status, currency)
            VALUES (:order_ref, :customer_ref, :status, :currency)
            ON CONFLICT (order_ref) DO UPDATE SET
                customer_ref = excluded.customer_ref,
                status = excluded.status,
                currency = excluded.currency
            """,
            {
                "order_ref": order.order_ref,
                "customer_ref": order.customer_ref,
                "status": order.status.value,
                "currency": order.currency,
            },
        )

    def get(self, order_ref: str):
        row = self._conn.execute(
            "SELECT order_ref, customer_ref, status, currency "
            "FROM orders WHERE order_ref = :order_ref",
            {"order_ref": order_ref},
        ).fetchone()
        return row

    def find_by_customer_ref(self, customer_ref: str) -> list:
        """Find all orders for a customer_ref.

        Under CR-4471 this becomes find_by_customer_id(customer_id: int) and the
        WHERE clause matches the integer customer_id column.
        """
        return self._conn.execute(
            "SELECT order_ref, customer_ref, status, currency "
            "FROM orders WHERE customer_ref = :customer_ref",
            {"customer_ref": customer_ref},
        ).fetchall()
