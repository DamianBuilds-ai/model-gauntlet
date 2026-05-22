"""Acme Orders - ORM model (PRE-change state).

The Order model maps to the orders table. customer_id is an integer column. After
the migration it must be account_ref, a string of max length 36, matching the
schema, the serializer, the OpenAPI contract, the config, the docs, and the
sample.
"""

from dataclasses import dataclass


@dataclass
class Order:
    id: int
    customer_id: int          # integer FK to the customer
    status: str
    total_cents: int

    def owner_key(self) -> str:
        # Builds a cache key from the owner identifier.
        return f"order-owner:{self.customer_id}"

    @classmethod
    def from_row(cls, row: dict) -> "Order":
        return cls(
            id=row["id"],
            customer_id=row["customer_id"],
            status=row["status"],
            total_cents=row["total_cents"],
        )
