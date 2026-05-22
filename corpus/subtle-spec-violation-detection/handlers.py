"""Globex Orders API - request handlers.

Implements the endpoints and helpers specified in CONTRACT.md. This module has
passed an informal review and is believed to comply with the contract. It is the
artifact under audit.

Stdlib only. The framework primitives (Request, Response, json error helpers) are
imported from the in-house micro-framework `globex.web`.
"""

from decimal import Decimal, ROUND_HALF_EVEN
from datetime import datetime, timezone

from globex.web import Request, Response, json_ok, json_error
from globex.store import OrderStore, IdempotencyStore, RateLimiter
from globex.auth import verify_bearer


# ----- valid enums and constants -------------------------------------------

VALID_STATUSES = {"pending", "paid", "shipped", "cancelled"}
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100

# Region tax rates (post-discount subtotal is taxed at these rates).
REGION_TAX_RATES = {
    "AU": Decimal("0.10"),
    "US-CA": Decimal("0.0725"),
    "GB": Decimal("0.20"),
    "NZ": Decimal("0.15"),
}

# Allowed order state transitions; anything not listed is a 409 conflict.
ALLOWED_TRANSITIONS = {
    "pending": {"paid", "cancelled"},
    "paid": {"shipped", "cancelled"},
    "shipped": set(),
    "cancelled": set(),
}


# ----- helpers --------------------------------------------------------------

def require_auth(req: Request) -> str:
    """Rule 1. Return the caller id, or raise Unauthorized -> 401."""
    token = req.headers.get("Authorization", "")
    caller = verify_bearer(token)
    if caller is None:
        raise Unauthorized()
    return caller


def require_json(req: Request) -> None:
    """Rule 2. Reject non-JSON bodies with 415."""
    ctype = req.headers.get("Content-Type", "")
    if not ctype.startswith("application/json"):
        raise UnsupportedMediaType()


def round_money(value: Decimal) -> Decimal:
    """Rule 7. Round to 2 dp using banker's rounding (round-half-to-even)."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)


def iso_utc(dt: datetime) -> str:
    """Rule 12. ISO 8601 UTC, second precision, Z suffix."""
    dt = dt.astimezone(timezone.utc).replace(microsecond=0)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def clamp_page_size(raw) -> int:
    """Rule 4. Default 25; clamp to [1, 100] inclusive."""
    if raw is None:
        return DEFAULT_PAGE_SIZE
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_PAGE_SIZE
    if n < 1:
        return 1
    if n > MAX_PAGE_SIZE:
        return MAX_PAGE_SIZE
    return n


def clamp_page(raw) -> int:
    """Rule 4. Default 1; minimum 1."""
    if raw is None:
        return 1
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return 1
    return n if n >= 1 else 1


def apply_volume_discount(quantity: int, line_subtotal: Decimal) -> Decimal:
    """Rule 9. Volume discount by line quantity.

    Tiers:
      under 50 units   -> 0 percent
      50 to 99 units   -> 5 percent
      100 units or more -> 10 percent
    Returns the discount AMOUNT (a positive Decimal) to subtract from the line.
    """
    if quantity > 100:
        rate = Decimal("0.10")
    elif quantity >= 50:
        rate = Decimal("0.05")
    else:
        rate = Decimal("0.00")
    return round_money(line_subtotal * rate)


def compute_tax(post_discount_subtotal: Decimal, region: str) -> Decimal:
    """Rule 8. Tax on the post-discount subtotal at the region rate, rounded."""
    rate = REGION_TAX_RATES.get(region, Decimal("0.00"))
    return round_money(post_discount_subtotal * rate)


def line_post_discount(item: dict) -> Decimal:
    """Subtotal of one line after its volume discount, rounded."""
    qty = int(item["quantity"])
    unit_price = Decimal(str(item["unit_price"]))
    gross = unit_price * qty
    discount = apply_volume_discount(qty, gross)
    return round_money(gross - discount)


def compute_total(items: list, region: str, shipping: Decimal) -> dict:
    """Rule 15. Total = post-discount subtotal + tax + shipping, all rounded."""
    subtotal = sum((line_post_discount(it) for it in items), Decimal("0.00"))
    subtotal = round_money(subtotal)
    tax = compute_tax(subtotal, region)
    shipping = round_money(shipping)
    total = round_money(subtotal + tax + shipping)
    return {
        "subtotal": str(subtotal),
        "tax": str(tax),
        "shipping": str(shipping),
        "total": str(total),
    }


# ----- exceptions mapped to status codes ------------------------------------

class ApiError(Exception):
    status = 500
    code = "internal_error"

    def __init__(self, message=""):
        self.message = message or self.code


class Unauthorized(ApiError):
    status = 401
    code = "unauthorized"


class UnsupportedMediaType(ApiError):
    status = 415
    code = "unsupported_media_type"


class Unprocessable(ApiError):
    status = 422
    code = "unprocessable_entity"


class NotFound(ApiError):
    status = 404
    code = "not_found"


class Conflict(ApiError):
    status = 409
    code = "conflict"


class RateLimited(ApiError):
    status = 429
    code = "rate_limited"


def with_rate_headers(resp: Response, remaining: int) -> Response:
    """Rule 13. Attach the remaining-quota header to every response."""
    resp.headers["X-RateLimit-Remaining"] = str(remaining)
    return resp


# ----- endpoint handlers ----------------------------------------------------

def create_order(req: Request, store: OrderStore, idem: IdempotencyStore,
                 limiter: RateLimiter) -> Response:
    """POST /orders. Rules 1, 2, 3, 7, 8, 9, 10, 11, 13, 15, 16."""
    caller = require_auth(req)
    remaining = limiter.consume(caller)
    if remaining < 0:
        raise RateLimited()
    require_json(req)

    # Rule 10: idempotency.
    key = req.headers.get("Idempotency-Key")
    if key:
        cached = idem.lookup(caller, key)
        if cached is not None:
            return with_rate_headers(
                Response(status=201, body={"data": cached}), remaining)

    body = req.json()
    customer_id = body.get("customer_id")
    items = body.get("items")
    # Rule 3: required fields.
    if not customer_id or not isinstance(customer_id, str):
        raise Unprocessable("customer_id is required")
    if not items or not isinstance(items, list):
        raise Unprocessable("items is required")

    region = body.get("region", "AU")
    shipping = Decimal(str(body.get("shipping", "0")))
    totals = compute_total(items, region, shipping)  # Rules 7, 8, 9, 15

    now = datetime.now(timezone.utc)
    order = store.insert({
        "customer_id": customer_id,
        "items": items,
        "region": region,
        "status": "pending",
        "totals": totals,
        "created_at": iso_utc(now),   # Rule 12
        "updated_at": iso_utc(now),
        "deleted_at": None,
    })

    if key:
        idem.store(caller, key, order)

    # Rule 16 envelope, Rule 11 status 201.
    return with_rate_headers(
        Response(status=201, body={"data": order}), remaining)


def get_order(req: Request, order_id: str, store: OrderStore,
              limiter: RateLimiter) -> Response:
    """GET /orders/{id}. Rules 1, 11, 13, 16."""
    caller = require_auth(req)
    remaining = limiter.consume(caller)
    if remaining < 0:
        raise RateLimited()
    order = store.get(order_id)
    if order is None or order.get("deleted_at") is not None:
        raise NotFound("order not found")   # Rule 11: 404
    return with_rate_headers(
        Response(status=200, body={"data": order}), remaining)


def list_orders(req: Request, store: OrderStore, limiter: RateLimiter) -> Response:
    """GET /orders. Rules 1, 4, 5, 6, 13, 16."""
    caller = require_auth(req)
    remaining = limiter.consume(caller)
    if remaining < 0:
        raise RateLimited()

    # Rule 5: status filter validation.
    status = req.query.get("status")
    if status is not None and status not in VALID_STATUSES:
        raise Unprocessable("invalid status filter")

    # Rule 4: pagination.
    page = clamp_page(req.query.get("page"))
    page_size = clamp_page_size(req.query.get("page_size"))

    rows = store.all(include_deleted=False)
    if status is not None:
        rows = [r for r in rows if r["status"] == status]

    # Rule 6: created_at DESC, id ASC tiebreak.
    rows.sort(key=lambda r: r["id"])
    rows.sort(key=lambda r: r["created_at"], reverse=True)

    start = (page - 1) * page_size
    page_rows = rows[start:start + page_size]

    return with_rate_headers(
        Response(status=200, body={"data": page_rows}), remaining)


def pay_order(req: Request, order_id: str, store: OrderStore,
              limiter: RateLimiter) -> Response:
    """POST /orders/{id}/pay. Rules 1, 11, 12, 13, 16."""
    caller = require_auth(req)
    remaining = limiter.consume(caller)
    if remaining < 0:
        raise RateLimited()
    order = store.get(order_id)
    if order is None or order.get("deleted_at") is not None:
        raise NotFound("order not found")

    # Rule 11: state-transition conflict -> 409.
    current = order["status"]
    if "paid" not in ALLOWED_TRANSITIONS.get(current, set()):
        raise Conflict("cannot pay order in state " + current)

    order["status"] = "paid"
    order["updated_at"] = iso_utc(datetime.now(timezone.utc))  # Rule 12
    store.update(order)
    return with_rate_headers(
        Response(status=200, body={"data": order}), remaining)


def delete_order(req: Request, order_id: str, store: OrderStore,
                 limiter: RateLimiter) -> Response:
    """DELETE /orders/{id}. Rule 14 soft delete -> 204, no body."""
    caller = require_auth(req)
    remaining = limiter.consume(caller)
    if remaining < 0:
        raise RateLimited()
    order = store.get(order_id)
    if order is None or order.get("deleted_at") is not None:
        raise NotFound("order not found")

    order["deleted_at"] = iso_utc(datetime.now(timezone.utc))  # Rule 14 soft
    store.update(order)
    # Rule 14: 204, no response body.
    return with_rate_headers(Response(status=204, body=None), remaining)


def error_to_response(err: ApiError) -> Response:
    """Rule 16. Map any ApiError to the standard error envelope."""
    return Response(
        status=err.status,
        body={"error": {"code": err.code, "message": err.message}},
    )
