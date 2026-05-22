# Northwind Orders API (Globex)

This document describes the order API for Northwind Orders. Per change request
CR-4471 the customer identity field is being renamed from `customer_ref` to
`customer_id` and retyped from a string to a 64-bit integer; this document must be
updated to match.

## The order resource

An order has the following fields.

| Field            | Type    | Required | Notes                                            |
|------------------|---------|----------|--------------------------------------------------|
| `order_ref`      | string  | yes      | Human-facing order reference, format `ord_NNNN`. Not changing. |
| `customer_ref`   | string  | yes      | Customer identity, format `cust_NNNNN`. CR-4471: rename to `customer_id`, type integer. |
| `status`         | string  | yes      | One of draft, placed, fulfilled, cancelled.      |
| `currency`       | string  | yes      | ISO 4217 three-letter code.                      |
| `line_items`     | array   | no       | Order line items.                                |

## Create an order

`POST /orders`

Request body:

```json
{
  "order_ref": "ord_5589",
  "customer_ref": "cust_00417",
  "currency": "USD",
  "line_items": [
    { "sku": "WIDGET-1", "quantity": 2, "unit_price_minor": 1999 }
  ]
}
```

The `customer_ref` must currently match `^cust_\d{5}$`. Under CR-4471 this becomes
`customer_id`, a positive integer (the example value `cust_00417` becomes `417`).

## List a customer's orders

`GET /orders/by-customer/{customer_ref}`

Returns all orders for the given customer. For example,
`GET /orders/by-customer/cust_00417` lists the orders for customer `cust_00417`.
Under CR-4471 the path becomes `GET /orders/by-customer/{customer_id}` and the
example becomes `GET /orders/by-customer/417`.

## Notes

The `customer_ref` field is the most-referenced field in the API and appears in
the request body, the response body, and the by-customer path. When CR-4471 lands,
every one of those occurrences becomes `customer_id` with an integer value.
