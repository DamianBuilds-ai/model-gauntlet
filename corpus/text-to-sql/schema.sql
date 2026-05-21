-- Synthetic schema for the text-to-SQL eval. Fully synthetic - a fictional "Acme"
-- e-commerce store. The eval gives a natural-language question and asks for SQL
-- against THIS schema.

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    country     TEXT NOT NULL,
    created_at  DATE NOT NULL
);

CREATE TABLE products (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    placed_at   DATE NOT NULL,
    status      TEXT NOT NULL  -- one of: 'pending','paid','shipped','cancelled'
);

CREATE TABLE order_items (
    id         INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL
);
