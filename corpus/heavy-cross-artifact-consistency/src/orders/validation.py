"""Northwind Orders - payload validation (Globex).

Validates an incoming order payload. The customer_ref rule below enforces the OLD
string format "cust_<digits>" via a regex. CR-4471 retypes the field to a positive
integer, so this regex rule must be replaced with an integer check and the field
renamed to customer_id.
"""

from __future__ import annotations

import re


# OLD: customer_ref is a string like "cust_00417". This pattern enforces it.
# Under CR-4471 the field becomes customer_id (a positive integer) and this
# pattern is removed in favour of an integer check.
CUSTOMER_REF_PATTERN = re.compile(r"^cust_\d{5}$")

# order_ref is a separate field and is NOT changing. Leave this pattern alone.
ORDER_REF_PATTERN = re.compile(r"^ord_\d{4}$")


class ValidationError(ValueError):
    pass


def validate_order_payload(body: dict) -> None:
    """Validate the create-order body. Raises ValidationError on a bad field."""
    if "order_ref" not in body:
        raise ValidationError("order_ref is required")
    if not ORDER_REF_PATTERN.match(str(body["order_ref"])):
        raise ValidationError("order_ref must match ord_<4 digits>")

    # customer_ref: required, must match the cust_ string format.
    if "customer_ref" not in body:
        raise ValidationError("customer_ref is required")
    if not CUSTOMER_REF_PATTERN.match(str(body["customer_ref"])):
        raise ValidationError("customer_ref must match cust_<5 digits>")

    if "currency" in body and len(str(body["currency"])) != 3:
        raise ValidationError("currency must be a 3-letter code")

    for li in body.get("line_items", []):
        if li.get("quantity", 0) <= 0:
            raise ValidationError("line item quantity must be positive")
        if li.get("unit_price_minor", -1) < 0:
            raise ValidationError("unit_price_minor must be non-negative")


def normalise_customer_ref(raw: str) -> str:
    """Return the canonical customer_ref string for a raw input.

    Under CR-4471 this becomes a parse-to-int helper: strip the cust_ prefix and
    return the integer customer_id.
    """
    raw = raw.strip()
    if not CUSTOMER_REF_PATTERN.match(raw):
        raise ValidationError("customer_ref must match cust_<5 digits>")
    return raw
