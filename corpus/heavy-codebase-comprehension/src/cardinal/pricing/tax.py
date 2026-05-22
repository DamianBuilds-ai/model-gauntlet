"""Tax math for Cardinal pricing. Distractor - no reserve_stock reference."""

from decimal import Decimal

_RATES = {"US": Decimal("0.08"), "GB": Decimal("0.20"), "AU": Decimal("0.10")}


def apply_tax(amount, region):
    rate = _RATES.get(region, Decimal("0.00"))
    return amount + (amount * rate)


def tax_only(amount, region):
    rate = _RATES.get(region, Decimal("0.00"))
    return amount * rate
