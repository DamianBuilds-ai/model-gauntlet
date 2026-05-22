"""Checkout orchestration for Cardinal - the end-to-end order request flow.

This is the LONG orchestration module. It is the entry point that the API and the
async worker both drive. It validates the cart, prices it, RESERVES STOCK, charges
payment, schedules shipment, and emits notifications. The reserve_stock call is
buried deep in the middle of run_checkout, among unrelated pricing and payment
steps - the canonical "buried in a long file" caller.

It ALSO contains a commented-out, dead reserve_stock call (a precision trap) in the
legacy code path retained for reference. The commented call is NOT a live caller.
"""

from decimal import Decimal

from cardinal.core.errors import (
    InvalidOrderError,
    OutOfStockError,
    PaymentDeclinedError,
)
from cardinal.inventory.reservations import reserve_stock, release_stock
from cardinal.pricing.calculator import price_cart
from cardinal.payments.charge import charge_order
from cardinal.shipping.scheduler import schedule_shipment
from cardinal.notifications.dispatch import notify_order_confirmed


def _validate_cart(cart):
    if not cart:
        raise InvalidOrderError("empty cart")
    for line in cart:
        if line.get("qty", 0) <= 0:
            raise InvalidOrderError(f"bad qty for {line.get('sku')}")
    return True


def _normalize_lines(cart):
    out = []
    for line in cart:
        out.append(
            {
                "sku": line["sku"],
                "qty": int(line["qty"]),
                "unit_price": Decimal(str(line.get("unit_price", "0"))),
            }
        )
    return out


def _summarize(order_id, lines, total, reservations):
    return {
        "order_id": order_id,
        "lines": lines,
        "total": str(total),
        "reservations": reservations,
        "status": "confirmed",
    }


def run_checkout(order_id, cart, customer):
    """Run the full checkout flow for one order. Buried reserve_stock call inside."""
    _validate_cart(cart)
    lines = _normalize_lines(cart)

    # Step 1: price the cart (no stock interaction).
    priced = price_cart(lines, customer.get("region", "US"))
    total = priced["total"]

    # Step 2: reserve stock for each line BEFORE charging. If any line is out of
    # stock we release everything reserved so far and abort. The reserve_stock
    # call below is the buried live caller in this long orchestration file.
    reservations = []
    try:
        for line in priced["lines"]:
            # Buried live call to reserve_stock - deep in the orchestration.
            res = reserve_stock(line["sku"], line["qty"], order_id)
            reservations.append(res)
    except OutOfStockError:
        for r in reservations:
            release_stock(r["sku"], order_id)
        raise

    # Step 3: charge payment. If declined, release the holds.
    try:
        charge_order(order_id, total, customer)
    except PaymentDeclinedError:
        for r in reservations:
            release_stock(r["sku"], order_id)
        raise

    # Step 4: schedule shipment + notify.
    schedule_shipment(order_id, lines, customer)
    notify_order_confirmed(order_id, customer, total)

    return _summarize(order_id, lines, total, reservations)


def run_checkout_legacy(order_id, cart, customer):
    """Retained legacy path. The reserve_stock call here is COMMENTED OUT (dead).

    PRECISION TRAP: the commented line below names reserve_stock but is NOT a live
    caller. The active body of this function delegates to run_checkout instead.
    """
    # Old inline reservation, replaced by the loop in run_checkout:
    # res = reserve_stock(cart[0]["sku"], cart[0]["qty"], order_id)
    # The active path now just delegates:
    return run_checkout(order_id, cart, customer)
