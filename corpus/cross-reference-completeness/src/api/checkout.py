"""Checkout API endpoint for Acme Ledger.

The hot path. One direct call to the deprecated legacy_compute_tax when pricing
a cart at checkout, plus the import line at the top.
"""

from decimal import Decimal

from src.tax.legacy import legacy_compute_tax


def price_cart(cart, region):
    subtotal = sum((Decimal(i["unit_price"]) * i["qty"] for i in cart), Decimal("0"))
    # Direct call in the checkout hot path - deprecated, must migrate.
    tax = legacy_compute_tax(subtotal, region)
    return {"subtotal": subtotal, "tax": tax, "total": subtotal + tax}


def handle_checkout(request):
    region = request["customer"]["region"]
    pricing = price_cart(request["cart"], region)
    return {"status": "ok", "pricing": pricing}
