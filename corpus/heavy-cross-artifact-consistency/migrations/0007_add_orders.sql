-- Northwind Orders - migration 0007 (Globex)
-- Creates the orders table. The customer_ref column is TEXT today; CR-4471
-- renames it to customer_id and retypes it to BIGINT. order_ref stays TEXT.

CREATE TABLE IF NOT EXISTS orders (
    order_ref      TEXT PRIMARY KEY,
    customer_ref   TEXT NOT NULL,            -- CR-4471: -> customer_id BIGINT NOT NULL
    status         TEXT NOT NULL DEFAULT 'draft',
    currency       TEXT NOT NULL DEFAULT 'USD',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index used by the by-customer lookup. The column name in this index moves to
-- customer_id under CR-4471.
CREATE INDEX IF NOT EXISTS idx_orders_customer_ref
    ON orders (customer_ref);

-- order_ref format check is unrelated to the customer field and does not change.
ALTER TABLE orders
    ADD CONSTRAINT chk_order_ref_format
    CHECK (order_ref ~ '^ord_[0-9]{4}$');
