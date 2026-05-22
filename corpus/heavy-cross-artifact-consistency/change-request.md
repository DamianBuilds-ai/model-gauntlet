# Change request CR-4471 - rename and retype customer_ref to customer_id

Product: Northwind Orders (Globex). Owner: platform engineering. Priority: high.

## Summary

The order record identifies its customer with the field `customer_ref`, a STRING
in the format `cust_<zero-padded-digits>` (for example `cust_00417`). Globex has
migrated to a numeric customer-identity service. The field must be renamed to
`customer_id` and RETYPED to a 64-bit signed INTEGER (for example `417`). This is
a single coordinated change across the whole service slice; partial application
leaves the system internally inconsistent.

## Exact rules

1. NEW NAME: the field is `customer_id` everywhere it currently appears as
   `customer_ref`. No artifact may retain the old name `customer_ref` after the
   change (in code, schema, config, docs, tests, examples, comments, or
   docstrings). A residual `customer_ref` anywhere is an inconsistency.

2. NEW TYPE: the field is a 64-bit signed INTEGER everywhere its type is declared,
   validated, or implied:
   - Python type hints / dataclass field type: `int` (not `str`).
   - JSON Schema: `"type": "integer"` (not `"string"`), with the old `pattern`
     regex removed and replaced by an integer constraint (`"minimum": 1`).
   - OpenAPI: `type: integer`, `format: int64` (not `type: string`), example a
     bare integer.
   - SQL column: `BIGINT NOT NULL` (not `TEXT NOT NULL` / `VARCHAR`).
   - Validation: enforce a positive integer; the old `cust_` prefix regex is
     removed.
   A place that keeps the old string type after the rename is an inconsistency
   (the "renamed but not retyped" trap).

3. NEW EXAMPLE VALUES: every example, default, fixture, or sample value of the
   field is expressed as the new INTEGER, derived from the old string by stripping
   the `cust_` prefix and parsing the remaining digits as an integer. So:
   - `cust_00417` becomes `417`
   - `cust_00001` becomes `1`
   - `cust_09900` becomes `9900`
   An example that keeps the `cust_` string form, OR that quotes the new value as
   a string (`"417"` instead of the integer `417`), is an inconsistency. JSON and
   YAML integer values must be unquoted numbers.

4. REQUIRED FIELD: `customer_id` is required (it was required before as
   `customer_ref`). Keep it required in the JSON Schema `required` array, the
   OpenAPI required list, the SQL `NOT NULL`, and the validation.

5. PATH PARAMETERS: where the OpenAPI spec or a route uses the value in a URL path
   (the `/orders/by-customer/{customer_ref}` path), rename the path parameter to
   `{customer_id}` AND set its schema to `type: integer, format: int64`.

6. THE MAPPING DOC: the prose documentation must describe the field as
   `customer_id`, type integer, and must NOT continue to describe a string with a
   `cust_` format. Update the field table row (name AND type AND example) and any
   prose sentence that references the old field.

7. THE CAPTURED LOG: `docs/sample-request.log` is a captured example request and
   response. Treat it as documentation that must be made consistent: rewrite the
   logged request and response bodies to use `customer_id` with an integer value
   matching the same customer the old log referenced (`cust_00417` -> `417`).

8. THE README: the README in this corpus references `customer_ref` in its prose
   for orientation. The README is NOT in scope for the rename (it is corpus
   meta-documentation describing the BEFORE state, not a shipped artifact); leave
   it unchanged. A change to the README is an out-of-scope edit and counts against
   precision, just as touching a non-target file would. (This is the one
   deliberate "leave it alone" artifact - the trap symmetric to the precision
   traps on the cross-reference probe.)

9. NO SEMANTIC DRIFT: do not change any unrelated field, do not add new fields,
   do not alter the order total / status / line-item logic. Only the customer
   identity field changes. A change that also renames or retypes an unrelated
   field (for example the order's `order_ref`, which stays a string and is NOT
   the target) is an inconsistency-by-overreach.

## Artifacts in scope (fourteen to edit; one decoy; README explicitly out of scope)

src/orders/models.py, src/orders/api.py, src/orders/validation.py,
src/orders/serializers.py, src/orders/db/order_repository.py,
schema/order.schema.json, openapi/orders.yaml, config/app.ini,
config/.env.example, migrations/0007_add_orders.sql, tests/test_orders_api.py,
tests/test_validation.py, tests/fixtures/orders_seed.json, docs/orders-api.md,
docs/sample-request.log.

(That list names fifteen paths. FOURTEEN of them genuinely reference the field
and must change. ONE of them - `config/.env.example` - is a decoy that does NOT
reference `customer_ref` at all (it holds only infrastructure variables) and must
NOT be edited; inventing a customer variable in it is an out-of-scope edit that
counts against precision. Determining which listed files actually contain the
field, versus the decoy, is part of the task. The README is a sixteenth path,
called out separately above as out of scope.)

## Deliverable

Produce the full updated content of every artifact that genuinely changes, and a
per-artifact checklist stating, for each of the fifteen listed paths: whether it
changed, and if so the name change + type change + example-value change made in
it; or, if it did not change, the reason (no reference to the field, or
explicitly out of scope). Do not claim an artifact is consistent if your output
left an old name, an old type, or an old-format example in it - a confidently
-wrong "done" is worse than an honestly-flagged miss.
