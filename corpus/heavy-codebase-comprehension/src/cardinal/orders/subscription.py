"""Subscription renewal orders for Cardinal.

Recurring orders that renew on a schedule. Imports reserve_stock under an ALIAS
(reserve_stock as _hold) and calls it through the alias - so a search for the
literal name at the call site reads "_hold", not "reserve_stock". The aliased
import and the aliased call site are both true reserve_stock references.
"""

from cardinal.inventory.reservations import reserve_stock as _hold
from cardinal.payments.charge import charge_order


def renew_subscription(order_id, sku, qty, unit_price, customer):
    # Aliased call - _hold IS reserve_stock under another name.
    reservation = _hold(sku, qty, order_id)
    total = unit_price * qty
    charge_order(order_id, total, customer)
    return {"order_id": order_id, "reservation": reservation, "renewed": True}
