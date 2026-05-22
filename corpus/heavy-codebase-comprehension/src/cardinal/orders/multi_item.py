"""Multi-item bulk order path for Cardinal.

Bulk orders go through the hold_inventory WRAPPER (cardinal.inventory.holds), not
through reserve_stock directly. So bulk_reserve is an INDIRECT-via-wrapper caller
of reserve_stock - it reaches the target function only through hold_inventory. Both
the import of hold_inventory and the call to it must be flagged indirect-via-wrapper.
"""

from cardinal.inventory.holds import hold_inventory
from cardinal.payments.charge import charge_order


def bulk_reserve(order_id, line_items):
    # Indirect-via-wrapper: hold_inventory forwards each line to reserve_stock.
    return hold_inventory(line_items, order_id)


def bulk_checkout(order_id, line_items, total, customer):
    reservations = bulk_reserve(order_id, line_items)
    charge_order(order_id, total, customer)
    return {"order_id": order_id, "reservations": reservations}
