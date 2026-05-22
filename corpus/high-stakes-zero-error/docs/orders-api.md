# Acme Orders API - Reference (PRE-change state)

The Orders API returns order objects. Today the owner is identified by
`customer_id`, an integer. After the migration this becomes `account_ref`, a
string UUID (max 36 characters). This doc must be updated to match - the field
name, the type description, and the example payload below all reference the old
field and would mislead a consumer if left stale.

## Order object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Order identifier |
| `customer_id` | integer | Identifier of the order owner |
| `status` | string | One of pending, paid, shipped, cancelled |
| `total_cents` | integer | Order total in cents |

## Example response

```json
{
  "id": 4821,
  "customer_id": 91023,
  "status": "paid",
  "total_cents": 14900
}
```

## Notes

The `customer_id` is indexed for lookups. Consumers should treat it as the stable
owner key for an order.
