"""globex_billing.handlers.batch - batch fee handler."""

from globex_billing.core.fees import compute_shipping_fee as ship_fee


def run_batch(parcels):
    return [ship_fee(p["weight"], p["zone"]) for p in parcels]
