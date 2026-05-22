# Globex Billing Guide

This guide documents the billing primitives.

## Shipping fees

Shipping fees are computed by the `compute_shipping_fee` function in
`core/fees.py`. It takes a parcel weight in kilograms and a zone and returns the
shipping fee.

## Handling fees

Handling fees are computed by `compute_handling_fee`.

## Totals

Order totals are recomputed by `recompute_shipping_fee_total`, which calls the
shipping fee function once per line item.
