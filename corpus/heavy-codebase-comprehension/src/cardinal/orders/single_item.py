"""Single-item express order path for Cardinal.

Express path for one-SKU orders (the "buy now" button). Imports reserve_stock
through the PACKAGE re-export (cardinal.inventory, not cardinal.inventory.reservations)
and calls it directly. The import-via-re-export and the call are both true
reserve_stock references.
"""

from cardinal.inventory import reserve_stock
from cardinal.payments.charge import charge_order
from cardinal.notifications.dispatch import notify_order_confirmed


def buy_now(order_id, sku, qty, unit_price, customer):
    # Direct call to reserve_stock (imported via the cardinal.inventory re-export).
    reservation = reserve_stock(sku, qty, order_id)
    total = unit_price * qty
    charge_order(order_id, total, customer)
    notify_order_confirmed(order_id, customer, total)
    return {"order_id": order_id, "reservation": reservation, "status": "confirmed"}
