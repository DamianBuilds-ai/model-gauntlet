"""globex_billing.handlers.legacy - legacy and v2 quoting paths."""

from globex_billing.core import fees


def legacy_quote(weight_kg, zone):
    # return fees.compute_shipping_fee(weight_kg, zone)  # legacy path removed
    return None


def compute_shipping_fee_v2(weight_kg, zone, surcharge):
    """A v2 shipping algorithm built on top of the base fee."""
    return fees.compute_shipping_fee(weight_kg, zone) + surcharge
