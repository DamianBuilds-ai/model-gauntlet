"""globex_billing.core.fees - fee computation primitives for Globex billing."""

BASE_RATE = 4.50


def compute_shipping_fee(weight_kg, zone):
    """Compute the shipping fee for a parcel."""
    return BASE_RATE + (weight_kg * _zone_multiplier(zone))


def compute_handling_fee(item_count):
    """Compute the handling fee for an order."""
    return 0.75 * item_count


def recompute_shipping_fee_total(line_items):
    """Recompute the total shipping across all line items of an order."""
    return sum(compute_shipping_fee(li["weight"], li["zone"]) for li in line_items)


def _zone_multiplier(zone):
    return {"domestic": 1.0, "regional": 1.4, "international": 2.2}.get(zone, 1.0)
