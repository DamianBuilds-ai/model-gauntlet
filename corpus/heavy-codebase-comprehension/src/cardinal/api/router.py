"""HTTP router for Cardinal. Distractor - maps routes to handlers, no reserve_stock.

Wires URL paths to handler functions. It references the handlers (handle_checkout,
handle_manual_hold, etc.) but never names or calls reserve_stock itself.
"""

from cardinal.api.checkout_handler import handle_checkout
from cardinal.api.admin_handler import handle_manual_hold, handle_stock_snapshot


ROUTES = {
    ("POST", "/checkout"): handle_checkout,
    ("POST", "/admin/hold"): handle_manual_hold,
    ("GET", "/admin/stock-snapshot"): handle_stock_snapshot,
}


def dispatch(method, path, request):
    handler = ROUTES.get((method, path))
    if handler is None:
        return {"status": 404, "error": "not_found"}
    return handler(request)
