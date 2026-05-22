# Feature request: discount code endpoint

From: Priya (Product), to engineering. Logged in the Cardinal backlog.

We need an endpoint that applies a discount code to a cart and returns the new total.
Marketing is launching the spring codes next week and they want this in.

Codes live in the `promo_codes` table (Acme billing DB). A code has a percentage off.
Some codes are expired. Some are one-per-customer. The cart comes in as a list of line
items with prices. Just give back the discounted total.

Make it fast, it's on the checkout hot path. And make sure it doesn't break if someone
sends a code that doesn't exist - checkout should still work.

Thanks!
