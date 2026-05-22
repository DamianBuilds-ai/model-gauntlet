"""Higher-level inventory hold helpers for Cardinal.

This module defines hold_inventory, a WRAPPER that forwards to reserve_stock. Any
caller of hold_inventory reaches reserve_stock transitively (indirect-via-wrapper).
The wrapper itself (the call on line 22) is a TRUE direct caller of reserve_stock;
its own callers (in orders/multi_item.py and reports/availability.py) are indirect
callers and must be flagged as such.
"""

from cardinal.inventory.reservations import reserve_stock
from cardinal.core.errors import OutOfStockError


def hold_inventory(line_items, order_id):
    """Reserve every line item for an order, all-or-nothing.

    WRAPPER over reserve_stock. Forwards each line to reserve_stock. If any line
    fails, the already-placed holds are NOT rolled back here (the caller decides) -
    that detail does not matter for the trace; what matters is this forwards to
    reserve_stock.
    """
    results = []
    for item in line_items:
        # Wrapper forward - this IS a live call to reserve_stock.
        res = reserve_stock(item["sku"], item["qty"], order_id)
        results.append(res)
    return results


def hold_single(sku, qty, order_id):
    """Thin wrapper that also forwards one line to reserve_stock."""
    return reserve_stock(sku, qty, order_id)
