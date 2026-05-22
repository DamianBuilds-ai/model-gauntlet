"""Pricing calculator for Cardinal.

Distractor for the reserve_stock trace. price_cart is CALLED BY run_checkout, but
it does not call reserve_stock - pricing has no inventory side effects. This is a
long-ish module of pure pricing math.
"""

from decimal import Decimal

from cardinal.pricing.tax import apply_tax
from cardinal.pricing.discounts import apply_discounts


def _line_subtotal(line):
    return Decimal(str(line["unit_price"])) * line["qty"]


def price_line(line, region):
    subtotal = _line_subtotal(line)
    discounted = apply_discounts(subtotal, line.get("promo_codes", []))
    taxed = apply_tax(discounted, region)
    return {"sku": line["sku"], "qty": line["qty"], "amount": taxed}


def price_cart(lines, region):
    priced = [price_line(line, region) for line in lines]
    total = sum((p["amount"] for p in priced), Decimal("0"))
    # price_cart returns the priced lines with sku+qty so checkout can reserve them.
    return {"lines": priced, "total": total, "region": region}


def estimate_total(lines, region):
    return price_cart(lines, region)["total"]
