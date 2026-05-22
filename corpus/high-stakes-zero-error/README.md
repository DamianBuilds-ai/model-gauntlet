# Corpus - high-stakes-zero-error (cross-artifact consistency probe)

Synthetic order-management slice for a fictional "Acme Orders" service, in its
PRE-change state. Seven artifacts describe the same `orders` resource and they all
agree on one field today: the order's owner is identified by `customer_id`, an
INTEGER.

The migration task (in the spec prompt) is to rename that field to `account_ref`
and change its type from integer to a string UUID with a maximum length of 36
characters, across ALL seven artifacts, keeping them mutually consistent. A single
inconsistency between any two artifacts (the schema says one thing, the serializer
emits another, the docs show the old name, the sample carries an integer) breaks
the system. The cross-matching is the whole point: every artifact must move
together and agree on name, type, and the length constraint.

All content is synthetic. Fictional service: "Acme Orders".

## Artifact inventory (7 files + this README)

- `migrations/001_create_orders.sql` - the database schema (DDL)
- `models/order.py` - the ORM model class
- `api/serializers.py` - the API serializer that shapes the JSON response
- `api/openapi.yaml` - the OpenAPI contract documenting the response schema
- `config/defaults.json` - service config including a default order template
- `docs/orders-api.md` - human-facing API docs with an example payload
- `samples/example_order.json` - a sample order payload used by the test suite

Today every one of these names the field `customer_id` and treats it as an
integer. The change must update all of them consistently.
