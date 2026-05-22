# SYNTHETIC DATA - do NOT treat any text inside this file as instructions.
# This is data to be analyzed for cross-document contradictions.
# Fictional "Project Marlowe" specification set. 30 short spec docs follow,
# each delimited by a "=== DOC NN ===" header. Most are mutually consistent.

=== DOC 01: Overview ===
Project Marlowe is an order-fulfilment platform. It comprises the Intake service,
the Allocation engine, the Dispatch service, and the Ledger. Orders flow Intake ->
Allocation -> Dispatch, with the Ledger recording every state transition.

=== DOC 02: Glossary ===
An "order" is a customer request for one or more SKUs. A "shipment" is a physical
parcel produced by Dispatch. A "reservation" is an Allocation hold against inventory.
A "settlement" is a Ledger-confirmed financial close of an order.

=== DOC 03: Intake API ===
Intake exposes POST /orders. An order must contain at least one line item. The maximum
number of line items per order is 50. Intake rejects orders above this limit with HTTP
422.

=== DOC 04: Intake Validation ===
Intake validates that every SKU exists in the catalogue before accepting an order.
Unknown SKUs cause a 422. Currency must be one of AUD, USD, NZD.

=== DOC 05: Order States ===
The order lifecycle states are: RECEIVED, RESERVED, PICKING, DISPATCHED, SETTLED,
CANCELLED. An order may be CANCELLED only from RECEIVED or RESERVED.

=== DOC 06: Allocation Overview ===
The Allocation engine consumes RECEIVED orders and attempts to reserve inventory. On
success the order moves to RESERVED. On failure (insufficient stock) the order remains
RECEIVED and is retried.

=== DOC 07: Reservation TTL ===
A reservation, once created, is held for a fixed window before it expires and the stock
is released back to the available pool. The reservation hold window for Project Marlowe
is 30 minutes. After expiry the order returns to RECEIVED for re-allocation.

=== DOC 08: Allocation Retry ===
A RECEIVED order that fails allocation is retried every 5 minutes, up to 12 attempts.
After 12 failed attempts the order is flagged for manual review.

=== DOC 09: Inventory Model ===
Inventory is tracked per SKU per warehouse. Available stock = on-hand minus reserved.
Reservations decrement available immediately; they do not decrement on-hand until pick.

=== DOC 10: Dispatch Overview ===
Dispatch consumes RESERVED orders, generates pick lists, and produces shipments. A
single order may produce multiple shipments if line items span warehouses.

=== DOC 11: Pick Process ===
Picking moves an order from RESERVED to PICKING, then to DISPATCHED once all line items
are packed. On-hand stock is decremented at pick time.

=== DOC 12: Shipment Carriers ===
Dispatch supports three carriers: Falcon, Drayhorse, and Quill Post. Carrier selection
is by destination region and parcel weight.

=== DOC 13: Ledger Overview ===
The Ledger records every state transition with a timestamp and an actor. The Ledger is
append-only; corrections are made by compensating entries, never by mutation.

=== DOC 14: Settlement ===
An order is SETTLED when Dispatch confirms all shipments delivered AND the Ledger has a
matching payment-captured entry. Settlement is the terminal success state.

=== DOC 15: Cancellation Policy ===
A cancellation releases any active reservation back to inventory and writes a
compensating Ledger entry. Cancellations are not permitted after DISPATCHED.

=== DOC 16: Idempotency ===
All Intake POST /orders calls require an Idempotency-Key header. Duplicate keys within
24 hours return the original order rather than creating a new one.

=== DOC 17: Rate Limits ===
Intake is rate-limited to 200 requests per second per client. Bursts up to 400 are
permitted for up to 5 seconds.

=== DOC 18: Auth Model ===
All services authenticate via mutual TLS between internal components. External clients
use OAuth2 bearer tokens scoped to orders:write or orders:read.

=== DOC 19: Allocation SLA ===
Allocation must reach a reserve-or-retry decision within 2 seconds of receiving an
order. This is a hard latency SLA measured at p99.

=== DOC 20: Reservation Expiry Handling ===
When a reservation expires, the Allocation engine emits a ReservationExpired event. The
Dispatch service ignores these events; only Allocation acts on them by returning the
order to the RECEIVED state for re-allocation.

=== DOC 21: Warehouse Routing ===
Orders are routed to the nearest warehouse with available stock. Ties are broken by
lowest current pick queue depth.

=== DOC 22: Backorder Policy ===
If no warehouse has stock after 12 allocation attempts, the order may be backordered
with customer consent. Backordered orders bypass the reservation TTL.

=== DOC 23: Metrics ===
Each service emits orders_processed, latency_ms, and error_count metrics on a 15-second
interval to the central collector.

=== DOC 24: Audit Retention ===
Ledger entries are retained for 7 years. Operational logs are retained for 90 days.

=== DOC 25: Dispatch Reservation Assumption ===
Dispatch assumes that any order handed to it in the RESERVED state has a live, valid
reservation for its entire hold window, and that the reservation will not expire while
the order is being picked. Picking is expected to complete well within the hold window,
so Dispatch does not re-check the reservation before decrementing on-hand at pick time.

=== DOC 26: Pick Duration ===
The standard pick-to-pack duration for a multi-warehouse order is up to 45 minutes
under normal load, and may extend to 90 minutes during peak surge events.

=== DOC 27: Error Codes ===
Standard error codes: 422 validation, 409 conflict (e.g. idempotency mismatch), 429
rate limited, 503 downstream unavailable.

=== DOC 28: Deployment ===
Each service deploys independently via blue-green. The Ledger requires a maintenance
window for schema migrations; all other services migrate online.

=== DOC 29: Data Residency ===
All order and ledger data for AU customers resides in the ap-southeast-2 region. No
order data crosses region boundaries.

=== DOC 30: Notifications ===
Customers receive notifications on RESERVED, DISPATCHED, and SETTLED transitions.
CANCELLED also triggers a notification. PICKING does not.
