"""Inventory reservations for Cardinal order-fulfillment platform.

This module defines reserve_stock - the function the eval traces. reserve_stock
holds a quantity of a SKU against an order so two orders cannot both sell the last
unit. It is called from many places across the codebase (orders, api, workers,
pricing-side holds, and through a wrapper), some directly and some indirectly.

There is ALSO a deliberately similar function reserve_stock_snapshot in this file.
reserve_stock_snapshot is a DIFFERENT concern (it freezes a read-only snapshot of
stock levels for reporting; it does not hold inventory). It is a precision trap:
a caller of reserve_stock_snapshot is NOT a caller of reserve_stock.
"""

from decimal import Decimal

from cardinal.core.errors import OutOfStockError
from cardinal.core.ledger import write_ledger_entry


# In-memory stock book for the synthetic corpus. SKU -> available units.
_STOCK_BOOK = {}

# SKU -> list of active reservation holds.
_HOLDS = {}


def _available(sku):
    return _STOCK_BOOK.get(sku, 0)


def reserve_stock(sku, quantity, order_id):
    """Hold `quantity` units of `sku` against `order_id`.

    THIS is the target function the eval traces. Every live caller of THIS
    function (directly, via alias, or via the hold_inventory wrapper) is part of
    the answer key. Raises OutOfStockError if not enough stock is available.
    """
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    available = _available(sku)
    if available < quantity:
        raise OutOfStockError(sku, requested=quantity, available=available)
    _STOCK_BOOK[sku] = available - quantity
    _HOLDS.setdefault(sku, []).append({"order_id": order_id, "qty": quantity})
    write_ledger_entry("reserve", sku=sku, quantity=quantity, order_id=order_id)
    return {"sku": sku, "reserved": quantity, "order_id": order_id}


def release_stock(sku, order_id):
    """Release any hold this order placed on the SKU. Not a reserve_stock caller."""
    holds = _HOLDS.get(sku, [])
    kept = [h for h in holds if h["order_id"] != order_id]
    freed = sum(h["qty"] for h in holds if h["order_id"] == order_id)
    _HOLDS[sku] = kept
    _STOCK_BOOK[sku] = _available(sku) + freed
    if freed:
        write_ledger_entry("release", sku=sku, quantity=freed, order_id=order_id)
    return {"sku": sku, "released": freed, "order_id": order_id}


def reserve_stock_snapshot(skus):
    """PRECISION TRAP - a DIFFERENT function with a confusingly similar name.

    This freezes a read-only snapshot of current available levels for reporting.
    It does NOT hold inventory and does NOT call reserve_stock. A caller of this
    function is NOT a caller of reserve_stock. Listing a reserve_stock_snapshot
    caller as a reserve_stock caller is a precision error.
    """
    return {sku: _available(sku) for sku in skus}


def restock(sku, quantity):
    """Add units back to the book. Not a reserve_stock caller."""
    _STOCK_BOOK[sku] = _available(sku) + Decimal(quantity)
    write_ledger_entry("restock", sku=sku, quantity=quantity, order_id=None)
    return _available(sku)
