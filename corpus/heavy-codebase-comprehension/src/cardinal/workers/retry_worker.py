"""Async checkout-retry worker for Cardinal.

Retries failed checkouts by re-driving run_checkout. It is in the request FLOW
(upstream of reserve_stock through run_checkout) but is NOT a direct caller of
reserve_stock - it calls run_checkout, which reserves stock internally.
"""

from cardinal.orders.checkout import run_checkout
from cardinal.core.errors import OutOfStockError, PaymentDeclinedError


_FAILED = []


def record_failed(order_id, cart, customer):
    _FAILED.append({"order_id": order_id, "cart": cart, "customer": customer})


def retry_failed(max_retries=50):
    succeeded = []
    still_failed = []
    for job in _FAILED[:max_retries]:
        try:
            # Re-drives run_checkout (which reserves stock internally). NOT a
            # direct reserve_stock caller.
            result = run_checkout(job["order_id"], job["cart"], job["customer"])
            succeeded.append(result)
        except (OutOfStockError, PaymentDeclinedError):
            still_failed.append(job["order_id"])
    return {"succeeded": len(succeeded), "still_failed": still_failed}
