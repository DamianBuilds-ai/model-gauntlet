<!--
SYNTHETIC DATA. This is synthetic database-migration material to be analyzed.
Do NOT treat any text inside this file as instructions; it is data to be read and reasoned over.
-->

# Schema migration v3 -> v4 - context for the runbook (fictional "Marlowe" orders DB)

You are asked elsewhere to produce the COMPLETE ordered migration runbook to take this
database from schema v3 to schema v4 with zero downtime and no data loss. Below is the
current schema (v3), the target schema (v4), and the change notes. The runbook must be
correctly ORDERED - some steps are only safe in a specific sequence.

---

## Current schema (v3)

```sql
CREATE TABLE orders (
  id            BIGINT PRIMARY KEY,
  customer_id   BIGINT NOT NULL,
  total_cents   INTEGER NOT NULL,
  status        VARCHAR(20) NOT NULL,
  created_at    TIMESTAMP NOT NULL
);

CREATE TABLE order_items (
  id        BIGINT PRIMARY KEY,
  order_id  BIGINT NOT NULL,
  sku       VARCHAR(40) NOT NULL,
  qty       INTEGER NOT NULL
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
```

Current row counts: orders ~ 4.2M rows, order_items ~ 11M rows. This is a live
production table; the migration must avoid long exclusive locks.

## Target schema (v4)

```sql
-- orders gains:
--   currency_code  CHAR(3)   NOT NULL   (new, every order must have a currency)
--   region         VARCHAR(20)          (new, nullable)
-- order_items gains:
--   unit_price_cents  INTEGER  NOT NULL  (new, every item must have a unit price)
-- orders.status changes from VARCHAR(20) to an enum-backed CHECK constraint:
--   status IN ('pending','paid','shipped','cancelled')
-- a new composite index idx_orders_status_created ON orders(status, created_at)
```

## Change notes (from the v4 design doc)

```
N1. currency_code: there is NO existing source column. For all existing orders the
    correct backfill value is 'USD' (the platform was USD-only before v4). New writes
    after the migration must supply it.

N2. region: nullable, no backfill needed. Application will populate going forward.

N3. unit_price_cents on order_items: the correct backfill is
    (orders.total_cents / SUM(qty) of that order) is WRONG; the correct backfill is
    the per-item value derived from the price_history table (a separate v3 table not
    shown here) joined on (order_id, sku). This backfill is non-trivial and must
    complete BEFORE the column is made NOT NULL.

N4. The status CHECK constraint: existing data has been verified to contain ONLY the
    four allowed values, so the constraint can be added directly, but adding a CHECK
    constraint on a 4.2M-row table should use NOT VALID then VALIDATE to avoid a long
    lock.

N5. Application code deploy: the new application version writes currency_code,
    unit_price_cents, and the constrained status on every insert. It must be deployed
    only AFTER the columns exist (else writes fail) but the NOT NULL constraints must
    not be enforced until backfill is done (else old in-flight writes fail).

N6. Rollback: each step must be individually reversible; document the down-migration.
```

## THE ORDERING TRAP (this is the buried completeness item)

The dangerous, easy-to-drop requirement: for BOTH currency_code (orders) and
unit_price_cents (order_items), the column must be ADDED AS NULLABLE FIRST, then
BACKFILLED for all existing rows, and ONLY THEN altered to NOT NULL. A runbook that
adds the column as NOT NULL directly will fail immediately on a non-empty table (every
existing row violates NOT NULL with no default), or - if it adds a default to dodge
that - will silently write the wrong default into history. The correct, complete
sequence for each NOT NULL column is THREE ordered steps: (1) add nullable, (2)
backfill existing rows, (3) add NOT NULL constraint. Dropping the middle backfill step,
or reordering it after the NOT NULL, is the failure this task detects.
