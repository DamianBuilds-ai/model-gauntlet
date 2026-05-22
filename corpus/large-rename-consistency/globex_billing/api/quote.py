"""globex_billing.api.quote - quoting endpoint. Direct import + call site."""

from globex_billing.core.fees import compute_shipping_fee


def quote_parcel(weight_kg, zone, item_count):
    shipping = compute_shipping_fee(weight_kg, zone)
    return {"shipping": shipping}
