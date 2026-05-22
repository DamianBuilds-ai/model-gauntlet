"""HTTP handler for the checkout endpoint of Cardinal.

This is the API entry point for POST /checkout. It drives run_checkout. It does
NOT call reserve_stock directly - it goes through run_checkout, which reserves
stock internally. So this handler is part of the request FLOW (it is upstream of
reserve_stock) but it is NOT a direct caller of reserve_stock. The trace must
distinguish "in the call path" from "direct caller".
"""

from cardinal.orders.checkout import run_checkout
from cardinal.core.errors import OutOfStockError, PaymentDeclinedError, InvalidOrderError


def handle_checkout(request):
    """POST /checkout. Drives run_checkout. NOT a direct reserve_stock caller."""
    body = request.get("json", {})
    order_id = body.get("order_id")
    cart = body.get("cart", [])
    customer = body.get("customer", {})
    try:
        result = run_checkout(order_id, cart, customer)
    except OutOfStockError as e:
        return {"status": 409, "error": "out_of_stock", "sku": e.sku}
    except PaymentDeclinedError as e:
        return {"status": 402, "error": "payment_declined", "reason": e.reason}
    except InvalidOrderError as e:
        return {"status": 400, "error": "invalid_order", "detail": str(e)}
    return {"status": 200, "body": result}
