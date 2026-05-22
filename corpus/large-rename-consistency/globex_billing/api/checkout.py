"""globex_billing.api.checkout - checkout endpoint."""

from globex_billing.core import fees


def finalize(cart):
    shipping = fees.compute_shipping_fee(cart["weight"], cart["zone"])
    total = fees.recompute_shipping_fee_total(cart["line_items"])
    return {"shipping": shipping, "total": total}
