"""Acme Orders - API serializer (PRE-change state).

Shapes an Order into the JSON the API returns. It emits the field as
"customer_id" with an integer value. After the change it must emit "account_ref"
as a string, matching the schema, model, OpenAPI contract, docs, and sample.
"""


def serialize_order(order) -> dict:
    return {
        "id": order.id,
        "customer_id": order.customer_id,   # emitted JSON key + value
        "status": order.status,
        "total_cents": order.total_cents,
    }


def serialize_orders(orders) -> list:
    return [serialize_order(o) for o in orders]


def parse_order_request(payload: dict) -> dict:
    # Reads the inbound key. Must also move to account_ref.
    return {
        "customer_id": int(payload["customer_id"]),   # parses inbound key as int
        "status": payload.get("status", "pending"),
        "total_cents": payload["total_cents"],
    }
