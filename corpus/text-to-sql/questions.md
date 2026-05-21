# Natural-language questions for the text-to-SQL eval

Each variant must produce a single SQL query (targeting the schema in `schema.sql`)
that answers the question. All synthetic. The questions rise in difficulty so the
eval can see where cheaper models start producing wrong joins or aggregations.

## Q1 (easy)
List the names of all customers in Australia, alphabetically.

## Q2 (medium)
What is the total revenue (sum of price_cents times quantity) from orders with
status 'paid' or 'shipped'? Return a single number in cents.

## Q3 (medium-hard)
For each product category, how many distinct customers have ordered at least one
product in that category? Only count orders that are not 'cancelled'. Return
category and the distinct-customer count, highest count first.

## Q4 (hard)
Find customers who placed their first-ever order in the same calendar month they
were created, AND whose first order was later cancelled. Return customer name and
the order date. (This requires reasoning about "first order per customer" and
joining back to the customer creation date.)
