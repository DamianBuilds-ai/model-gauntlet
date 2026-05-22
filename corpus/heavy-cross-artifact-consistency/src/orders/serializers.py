"""Northwind Orders - serialisation (Globex).

Turns an Order into the JSON-ready dict returned by the API. The customer_ref key
emitted here must become customer_id (and carry an integer value) per CR-4471.
"""

from __future__ import annotations

from .models import Order


def serialize_order(order: Order) -> dict:
    """Serialise an Order to the public JSON shape.

    The emitted "customer_ref" key holds the customer identity string today; under
    CR-4471 it becomes "customer_id" with an integer value.
    """
    return {
        "order_ref": order.order_ref,
        "customer_ref": order.customer_ref,
        "status": order.status.value,
        "currency": order.currency,
        "total_minor": order.total_minor,
        "line_items": [
            {
                "sku": li.sku,
                "quantity": li.quantity,
                "unit_price_minor": li.unit_price_minor,
                "subtotal_minor": li.subtotal_minor,
            }
            for li in order.line_items
        ],
    }
