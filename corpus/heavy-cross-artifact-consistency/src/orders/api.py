"""Northwind Orders - HTTP handlers (Globex).

Thin request handlers over the repository. The customer identity field
customer_ref is read from the request body and from path parameters here; both
must move to customer_id (integer) per CR-4471.
"""

from __future__ import annotations

from .models import Order, OrderStatus, LineItem
from .validation import validate_order_payload
from .serializers import serialize_order
from .db.order_repository import OrderRepository


class OrdersApi:
    def __init__(self, repo: OrderRepository) -> None:
        self._repo = repo

    def create_order(self, body: dict) -> dict:
        """POST /orders - create an order from a JSON body.

        Expected body fields: order_ref (str), customer_ref (str, "cust_..."),
        currency (str), line_items (list).
        """
        validate_order_payload(body)
        order = Order(
            order_ref=body["order_ref"],
            customer_ref=body["customer_ref"],
            status=OrderStatus.DRAFT,
            currency=body.get("currency", "USD"),
            line_items=[
                LineItem(li["sku"], li["quantity"], li["unit_price_minor"])
                for li in body.get("line_items", [])
            ],
        )
        self._repo.save(order)
        return serialize_order(order)

    def get_orders_for_customer(self, customer_ref: str) -> list[dict]:
        """GET /orders/by-customer/{customer_ref} - list a customer's orders.

        The path parameter customer_ref selects the customer. Renaming to
        customer_id (integer) per CR-4471 also changes this path parameter.
        """
        orders = self._repo.find_by_customer_ref(customer_ref)
        return [serialize_order(o) for o in orders]

    def cancel_order(self, order_ref: str) -> dict:
        """POST /orders/{order_ref}/cancel - cancel by order reference.

        Note: order_ref is the ORDER reference (stays a string), not the customer
        field. This handler does not touch customer_ref.
        """
        order = self._repo.get(order_ref)
        order.status = OrderStatus.CANCELLED
        self._repo.save(order)
        return serialize_order(order)
