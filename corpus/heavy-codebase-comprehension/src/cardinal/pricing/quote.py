"""Quote generation with soft inventory holds for Cardinal.

When sales builds a large quote, the system optionally places a soft hold so the
quoted stock is not sold out from under the customer while they decide. That soft
hold goes through reserve_stock directly. So generate_quote_with_hold is a TRUE
direct caller of reserve_stock.
"""

from decimal import Decimal

from cardinal.inventory.reservations import reserve_stock
from cardinal.pricing.calculator import price_cart


def generate_quote_with_hold(quote_id, lines, region, place_hold=True):
    priced = price_cart(lines, region)
    holds = []
    if place_hold:
        for line in priced["lines"]:
            # Direct call to reserve_stock to soft-hold quoted stock.
            holds.append(reserve_stock(line["sku"], line["qty"], quote_id))
    return {"quote_id": quote_id, "priced": priced, "holds": holds}


def generate_quote_no_hold(quote_id, lines, region):
    """No-hold variant. Not a reserve_stock caller."""
    return {"quote_id": quote_id, "priced": price_cart(lines, region), "holds": []}
