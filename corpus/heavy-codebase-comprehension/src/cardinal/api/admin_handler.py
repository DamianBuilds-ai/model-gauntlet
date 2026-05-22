"""Admin HTTP handlers for Cardinal.

The admin manual-hold endpoint lets an operator place an inventory hold by hand
(for support cases). It imports reserve_stock directly and calls it - a TRUE direct
caller.

It ALSO has a reporting endpoint that calls reserve_stock_snapshot (the precision
trap function). The snapshot endpoint is NOT a reserve_stock caller.
"""

from cardinal.inventory.reservations import reserve_stock, reserve_stock_snapshot
from cardinal.core.errors import OutOfStockError


def handle_manual_hold(request):
    """POST /admin/hold. Direct reserve_stock caller (operator manual hold)."""
    body = request.get("json", {})
    sku = body.get("sku")
    qty = int(body.get("qty", 0))
    order_id = body.get("order_id", "manual-hold")
    try:
        # Direct call to reserve_stock from the admin manual-hold endpoint.
        res = reserve_stock(sku, qty, order_id)
    except OutOfStockError as e:
        return {"status": 409, "error": "out_of_stock", "available": e.available}
    return {"status": 200, "held": res}


def handle_stock_snapshot(request):
    """GET /admin/stock-snapshot. Calls reserve_stock_snapshot - NOT reserve_stock.

    PRECISION TRAP path: reserve_stock_snapshot is the similarly-named reporting
    function. This endpoint is NOT a reserve_stock caller.
    """
    skus = request.get("query", {}).get("skus", [])
    return {"status": 200, "snapshot": reserve_stock_snapshot(skus)}
