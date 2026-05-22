"""Northwind Orders - domain models (Globex).

The Order aggregate and its line items. The customer is currently identified by
customer_ref, a string of the form "cust_<digits>". See change-request CR-4471:
this field is being renamed to customer_id and retyped to a 64-bit integer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PLACED = "placed"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class LineItem:
    sku: str
    quantity: int
    unit_price_minor: int  # integer minor units (cents)

    @property
    def subtotal_minor(self) -> int:
        return self.quantity * self.unit_price_minor


@dataclass
class Order:
    """A customer order.

    order_ref is the human-facing order reference (a string like "ord_5589") and
    is NOT changing. customer_ref is the customer identity and IS changing to
    customer_id (integer) per CR-4471.
    """

    order_ref: str            # e.g. "ord_5589" - stays a string, NOT the target
    customer_ref: str         # e.g. "cust_00417" - RENAME to customer_id (int)
    status: OrderStatus
    currency: str
    line_items: list[LineItem] = field(default_factory=list)

    @property
    def total_minor(self) -> int:
        return sum(li.subtotal_minor for li in self.line_items)

    def belongs_to(self, customer_ref: str) -> bool:
        """Return True if this order belongs to the given customer_ref."""
        return self.customer_ref == customer_ref


def new_order(order_ref: str, customer_ref: str, currency: str = "USD") -> Order:
    """Factory for a draft order for the given customer_ref."""
    return Order(
        order_ref=order_ref,
        customer_ref=customer_ref,
        status=OrderStatus.DRAFT,
        currency=currency,
        line_items=[],
    )
