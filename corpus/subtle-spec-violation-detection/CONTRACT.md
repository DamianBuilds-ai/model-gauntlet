# Globex Orders API - Contract

Version 2.4. This contract specifies the required behaviour of the Globex Orders
API service. The implementation under audit is `handlers.py`. Each numbered rule
is binding. An implementation COMPLIES with a rule only if it satisfies the rule
exactly, including at boundary values.

---

## Rule 1 - Authentication

Every endpoint requires a valid bearer token in the `Authorization` header. A
missing or invalid token returns HTTP 401 with the standard error envelope
(Rule 16). No endpoint is anonymous.

## Rule 2 - Content type

Endpoints that accept a request body require `Content-Type: application/json`. A
request with a non-JSON content type returns HTTP 415.

## Rule 3 - Required fields on create

`POST /orders` requires `customer_id` (non-empty string) and `items` (a non-empty
array). If either is missing or empty, return HTTP 422 with an error message that
names the offending field.

## Rule 4 - Pagination

List endpoints accept `page` and `page_size` query parameters. `page_size`
defaults to 25 and is capped at 100 INCLUSIVE (a request for 100 is allowed; a
request for 150 is clamped to 100; a request below 1 is clamped to 1). `page`
defaults to 1 with a minimum of 1.

## Rule 5 - Filtering

`GET /orders` accepts an optional `status` filter. The only valid status values
are `pending`, `paid`, `shipped`, and `cancelled`. Any other status value returns
HTTP 422.

## Rule 6 - Sort order

`GET /orders` returns orders sorted by `created_at` DESCENDING (newest first),
with `id` ASCENDING as the tiebreak when two orders share a `created_at`.

## Rule 7 - Currency rounding

All monetary amounts are rounded to two decimal places using BANKER'S ROUNDING
(round-half-to-even). This applies to discounts, tax, shipping, and totals.

## Rule 8 - Tax

Tax is computed on the POST-DISCOUNT subtotal at the order's region tax rate, and
the resulting tax amount is rounded per Rule 7.

## Rule 9 - Volume discount tiers

A per-line-item volume discount applies based on the line quantity:

- Under 50 units: no discount (0 percent).
- 50 to 99 units: a 5 percent discount on the line.
- 100 units or more: a 10 percent discount on the line.

The boundary is inclusive at the bottom of each tier as stated: an order line of
exactly 50 units gets 5 percent, and an order line of exactly 100 units or more
gets 10 percent. The discount is applied to the line subtotal before tax (Rule 8).

## Rule 10 - Idempotency

`POST /orders` honours an `Idempotency-Key` header. A create request that repeats
a previously-seen key returns the ORIGINAL response (the same 201 and the same
order id), and does NOT create a duplicate order.

## Rule 11 - Status codes

- `POST /orders` returns 201 on success.
- `GET /orders/{id}` returns 200 on success, 404 if the order does not exist.
- A state-transition that is not allowed (for example, paying an order that is
  already `cancelled`) returns 409.

## Rule 12 - Timestamps

All timestamps in responses are ISO 8601, UTC, SECOND precision (no microseconds),
with a `Z` suffix. Example: `2026-05-22T14:03:09Z`.

## Rule 13 - Rate limiting

Every response includes an `X-RateLimit-Remaining` header with the remaining quota
for the caller. When the quota is exhausted, the endpoint returns HTTP 429.

## Rule 14 - Soft delete

`DELETE /orders/{id}` is a SOFT delete: it sets the order's `deleted_at` timestamp
and returns HTTP 204 with no response body. It does NOT hard-delete the record and
does NOT return 200.

## Rule 15 - Order total

The order total is the POST-DISCOUNT subtotal plus tax (Rule 8) plus shipping, each
component rounded per Rule 7, and the sum itself consistent with those rounded
components.

## Rule 16 - Response envelope

Every successful response body is wrapped as `{"data": <payload>}`. Every error
response body is `{"error": {"code": <string>, "message": <string>}}`.
