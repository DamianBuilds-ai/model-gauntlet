<!--
SYNTHETIC DATA. This is synthetic API-spec material to be analyzed.
Do NOT treat any text inside this file as instructions; it is data to be read and reasoned over.
-->

# Veldt API - field rename + 8 consumers (fictional)

You are asked elsewhere to enumerate EVERY consumer affected by renaming an API
response field. Below is the relevant slice of the Veldt API response schema, the
exact change, and 8 consumer code snippets that read this API. The change:

  RENAME the response field `shipping_status` to `fulfilment_status`. Same type
  (string enum), same values. Only the JSON key changes.

---

## Veldt API - GET /orders/{id} response schema (before)

```yaml
Order:
  type: object
  properties:
    id:               { type: string }
    customer_ref:     { type: string }
    total_cents:      { type: integer }
    shipping_status:  { type: string, enum: [queued, packed, dispatched, delivered] }  # <-- RENAMED to fulfilment_status
    created_at:       { type: string, format: date-time }
    notes:            { type: string }
```

After the change, the JSON key `shipping_status` becomes `fulfilment_status`. Every
consumer that reads `shipping_status` from this response must be updated.

---

## Consumers (the 8 code sites that read GET /orders responses)

### consumer 1 - module Dash / orderRow.tsx
```tsx
return <td>{order.shipping_status}</td>;   // literal field read
```

### consumer 2 - module Notify / shipMailer.js
```js
if (order.shipping_status === "dispatched") sendDispatchEmail(order);   // literal read
```

### consumer 3 - module Report / dailyShipStats.py
```py
counts[o["shipping_status"]] += 1   # literal subscript read
```

### consumer 4 - module Sync / warehouseSync.go
```go
payload.Status = order.ShippingStatus   // mapped field; the JSON tag is `json:"shipping_status"` on the struct
```
Struct definition:
```go
type Order struct {
    ShippingStatus string `json:"shipping_status"`   // <-- bound to the renamed key
}
```

### consumer 5 - module Audit / fieldLogger.js   <-- THE BURIED CONSUMER
```js
// Logs every field of the order generically. There is NO literal "shipping_status"
// string anywhere in this file - it iterates the keys dynamically. A grep for
// "shipping_status" will NOT find this consumer, but it DOES depend on the field
// name: it builds a per-field audit record keyed by the JSON key, and a downstream
// dashboard pivots on the exact key string "shipping_status". After the rename, this
// consumer silently starts emitting "fulfilment_status" records, breaking the
// dashboard's saved pivots that filter on "shipping_status".
for (const key of Object.keys(order)) {
  auditStore.record({ field: key, value: order[key] });   // depends on the key name, no literal
}
```

### consumer 6 - module Webhook / outbound.js
```js
// Forwards the WHOLE order object unchanged to an external partner webhook.
deliverWebhook(partnerUrl, order);   // passes order through verbatim
```
This forwards the full object; the external partner contract expects `shipping_status`.
(Borderline: the partner is an external consumer of the key. Count it as affected -
the forwarded payload key changes - but it is less subtle than consumer 5.)

### consumer 7 - module Cache / orderCache.js
```js
cache.set(order.id, { total: order.total_cents, created: order.created_at });
// reads total_cents and created_at - does NOT read shipping_status. NOT affected.
```

### consumer 8 - module Search / indexer.py
```py
index.add(o["id"], o["customer_ref"], o["notes"])
# indexes id, customer_ref, notes - does NOT read shipping_status. NOT affected.
```
