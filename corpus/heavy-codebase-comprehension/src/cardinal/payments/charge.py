"""Payment charging for Cardinal. Distractor - downstream of reserve_stock, no call.

charge_order is CALLED BY checkout AFTER stock is reserved. It does not call
reserve_stock. The dependency points from checkout into here, not the reverse.
"""

from decimal import Decimal

from cardinal.core.errors import PaymentDeclinedError
from cardinal.payments.gateway import authorize, capture


def charge_order(order_id, amount, customer):
    token = customer.get("payment_token")
    if not token:
        raise PaymentDeclinedError(order_id, "no payment token")
    auth = authorize(token, Decimal(amount))
    if not auth["approved"]:
        raise PaymentDeclinedError(order_id, auth.get("reason", "declined"))
    return capture(auth["auth_id"], Decimal(amount))


def refund_order(order_id, amount, customer):
    """Refund path. Not a reserve_stock caller."""
    return {"order_id": order_id, "refunded": str(amount), "status": "refunded"}
