-- Acme Orders - initial schema (PRE-change state).
-- The orders table identifies the owner by customer_id, an INTEGER. The
-- migration must rename this to account_ref and change its type to a string
-- (UUID, max length 36), consistently with every other artifact.

CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    customer_id  INTEGER NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_cents  INTEGER NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_customer_id ON orders (customer_id);
