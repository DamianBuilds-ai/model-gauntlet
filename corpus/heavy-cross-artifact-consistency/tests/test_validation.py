"""Northwind Orders - validation tests (Globex).

Tests the order-payload validator. The customer_ref cases below assert the OLD
string-format behaviour; CR-4471 retypes the field to a positive integer, so
these cases move to integer assertions and the cust_ string cases are replaced.
The order_ref cases are unrelated and stay as-is.
"""

from __future__ import annotations

import pytest

from src.orders.validation import (
    validate_order_payload,
    normalise_customer_ref,
    ValidationError,
)


def _body(**overrides):
    base = {
        "order_ref": "ord_5589",
        "customer_ref": "cust_00417",
        "currency": "USD",
        "line_items": [],
    }
    base.update(overrides)
    return base


def test_valid_payload_passes():
    validate_order_payload(_body())


def test_missing_customer_ref_raises():
    body = _body()
    del body["customer_ref"]
    # CR-4471: error message becomes "customer_id is required".
    with pytest.raises(ValidationError):
        validate_order_payload(body)


def test_bad_customer_ref_format_raises():
    # CR-4471: a non-integer customer_id raises; the cust_ string cases below are
    # replaced by integer cases (e.g. customer_id="417" string -> ValidationError,
    # customer_id=-1 -> ValidationError, customer_id=417 int -> passes).
    with pytest.raises(ValidationError):
        validate_order_payload(_body(customer_ref="417"))
    with pytest.raises(ValidationError):
        validate_order_payload(_body(customer_ref="cust_417"))
    with pytest.raises(ValidationError):
        validate_order_payload(_body(customer_ref="customer-417"))


def test_normalise_customer_ref_roundtrip():
    # CR-4471: normalise_customer_ref becomes a parse-to-int helper returning 417.
    assert normalise_customer_ref(" cust_00417 ") == "cust_00417"


def test_order_ref_format_unchanged():
    # order_ref is not the target; this stays a string check.
    with pytest.raises(ValidationError):
        validate_order_payload(_body(order_ref="5589"))
