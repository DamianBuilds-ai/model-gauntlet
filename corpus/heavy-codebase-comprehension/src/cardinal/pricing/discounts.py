"""Discount math for Cardinal pricing. Distractor - no reserve_stock reference."""

from decimal import Decimal

_PROMOS = {
    "SAVE10": Decimal("0.10"),
    "SAVE20": Decimal("0.20"),
    "WELCOME": Decimal("0.05"),
}


def apply_discounts(amount, promo_codes):
    total_pct = Decimal("0")
    for code in promo_codes:
        total_pct += _PROMOS.get(code, Decimal("0"))
    if total_pct > Decimal("0.5"):
        total_pct = Decimal("0.5")
    return amount - (amount * total_pct)
