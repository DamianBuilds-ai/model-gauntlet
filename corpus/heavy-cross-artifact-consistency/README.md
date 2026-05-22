# Corpus - heavy-cross-artifact-consistency (the rename-and-retype-across-N-artifacts probe)

A complete slice of a fictional order-management service ("Northwind Orders") for
the company "Globex". The slice spans FOURTEEN interlinked artifacts: application
code, a database model, a SQL migration, a JSON Schema, an OpenAPI spec, two
config files, a seed-data fixture, three test files, prose documentation, and an
example request log. A single domain field appears, by design, in nearly every
one of them. The task is to perform ONE coordinated rename-and-retype of that
field across the WHOLE slice so that every artifact stays mutually consistent.
Any artifact left referencing the old name, or carrying the wrong type for the
new field, or holding an example value of the wrong type, is an inconsistency -
and one inconsistency means the change is not done.

This is the heavy, scaled-up analog of an ordinary refactor: at two or three
files a rename is trivial, but at fourteen artifacts in six different formats
(Python, SQL, JSON Schema, OpenAPI YAML, INI/ENV config, Markdown) - where the
field is sometimes the same word, sometimes embedded in a path, an example
payload, a column definition, a regex, a docstring, or a test assertion - a model
under load propagates the obvious code occurrences and silently DROPS the buried
cross-format ones (the OpenAPI example value, the JSON Schema type, the migration
column type, the config default, the doc table). The retype dimension is the
trap: the field changes from a STRING to an INTEGER, so every place that declares
its type, validates it, or shows an example value must also change, not just the
places that use its name.

All content is synthetic. Fictional company: "Globex", product "Northwind
Orders". No real people are named.

## The change

The order record currently identifies its customer with a field named
`customer_ref`, a STRING in the format `cust_<digits>` (e.g. `cust_00417`). The
business has migrated to a numeric customer identity service, so the field must
be renamed to `customer_id` and RETYPED to a 64-bit INTEGER (e.g. `417`). The new
field is required, must be a positive integer, and replaces the old string field
everywhere. The mapping from the old string form to the new integer is "strip the
`cust_` prefix and parse the remaining digits as an integer" (so `cust_00417`
becomes `417`).

Perform this rename-and-retype across every artifact in the slice so the whole
system stays consistent: same field name everywhere, same integer type everywhere
it is declared or validated, and every example / fixture / sample value expressed
as the new integer rather than the old `cust_...` string. Produce the full updated
content of every artifact that must change, and a checklist mapping each artifact
to what changed in it (or stating it needed no change, with the reason).

## Files

- `README.md` - this file (read for context; it is not an artifact to edit, but
  note it also references the field in this prose - the change-request brief
  states whether the README itself must be updated).
- `change-request.md` - the formal change request with the exact rules and the
  list of artifacts in scope.
- `src/orders/models.py` - the `Order` dataclass / domain model.
- `src/orders/api.py` - the HTTP handler that reads and writes the field.
- `src/orders/validation.py` - input validation for the field.
- `src/orders/serializers.py` - JSON serialisation of the order.
- `src/orders/db/order_repository.py` - the persistence layer (SQL strings).
- `schema/order.schema.json` - the JSON Schema for an order payload.
- `openapi/orders.yaml` - the OpenAPI 3 spec (path params, request body schema,
  example values).
- `config/app.ini` - application config (a default customer ref for the demo
  tenant).
- `config/.env.example` - environment-variable example file.
- `migrations/0007_add_orders.sql` - the SQL migration that created the column.
- `tests/test_orders_api.py` - API-level tests (fixtures + assertions).
- `tests/test_validation.py` - validation unit tests.
- `tests/fixtures/orders_seed.json` - seed data fixture (example order records).
- `docs/orders-api.md` - prose API documentation with a field table and examples.
- `docs/sample-request.log` - a captured example request/response log.

## Why this discriminates

Fourteen artifacts in six formats, one field threaded through nearly all of them,
and a RETYPE (string -> integer) layered on top of the rename. A model under load
renames the obvious Python occurrences and the doc heading and calls it done,
leaving behind: the JSON Schema `"type": "string"` and its `pattern` regex, the
OpenAPI request-body type and the `example: "cust_00417"` value, the migration's
`customer_ref TEXT NOT NULL` column type, the config default `cust_00001`, the
seed fixture's string values, the validation regex that enforced the `cust_`
prefix, and the doc field-table row that says the type is "string". Each of those
is an inconsistency, and the scored discriminator is whether the model holds ALL
of them - renaming AND retyping AND re-valuing every example - with zero residual
old-name occurrences, zero residual string-type declarations, and zero
old-format example values. A confidently-wrong change (renaming the field but
leaving its type as string in the schema, or "updating" an example to a value
that is still a string like `"417"` instead of the integer `417`) is worse than a
missed artifact, because it ships a system that looks migrated but is internally
inconsistent.

The exhaustive invariant key - every artifact, every occurrence, the required
new name, the required new type, and the required example value - is in the
spec's `notes` field (the answer key).
