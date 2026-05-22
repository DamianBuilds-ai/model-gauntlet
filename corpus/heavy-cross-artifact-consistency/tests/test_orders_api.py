"""Northwind Orders - API tests (Globex).

Exercises the create + by-customer endpoints. The customer_ref values in the
fixtures and the assertions move to customer_id (integer) per CR-4471. Note that
order_ref assertions stay as strings (order_ref is not the target).
"""

from __future__ import annotations

import pytest

from src.orders.api import OrdersApi
from src.orders.db.order_repository import OrderRepository


VALID_BODY = {
    "order_ref": "ord_5589",
    "customer_ref": "cust_00417",
    "currency": "USD",
    "line_items": [
        {"sku": "WIDGET-1", "quantity": 2, "unit_price_minor": 1999},
    ],
}


def test_create_order_returns_customer_ref(fake_repo):
    api = OrdersApi(fake_repo)
    result = api.create_order(dict(VALID_BODY))
    # CR-4471: this becomes result["customer_id"] == 417 (integer).
    assert result["customer_ref"] == "cust_00417"
    assert result["order_ref"] == "ord_5589"
    assert result["total_minor"] == 3998


def test_get_orders_for_customer_filters_by_customer_ref(fake_repo):
    api = OrdersApi(fake_repo)
    api.create_order(dict(VALID_BODY))
    # CR-4471: the lookup argument becomes the integer 417.
    orders = api.get_orders_for_customer("cust_00417")
    assert len(orders) == 1
    assert orders[0]["customer_ref"] == "cust_00417"


def test_get_orders_for_unknown_customer_is_empty(fake_repo):
    api = OrdersApi(fake_repo)
    # CR-4471: becomes the integer 99999.
    orders = api.get_orders_for_customer("cust_99999")
    assert orders == []


def test_cancel_order_does_not_touch_customer(fake_repo):
    # order_ref is the order reference and stays a string; this test is unaffected
    # by the customer_ref -> customer_id change except via the shared fixture.
    api = OrdersApi(fake_repo)
    api.create_order(dict(VALID_BODY))
    result = api.cancel_order("ord_5589")
    assert result["status"] == "cancelled"
    assert result["order_ref"] == "ord_5589"
