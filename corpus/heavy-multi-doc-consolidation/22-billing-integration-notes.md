# Helios Billing Integration Notes

Author: Raj (Billing platform)
Status: working notes

## The billing adapter

The billing adapter connects Helios to the central Globex billing system (subscriptions,
invoices, payment capture). RAJ'S TEAM owns and operates the billing adapter.

NOTE: the billing PRD (doc 04) states that DANA owns the billing adapter. This document
states that Raj's team owns it. These two documents name DIFFERENT owners for the billing
adapter. This is the billing-owner conflict (risk register doc 12, RISK-3) and it is
UNRECONCILED in the source set - a consolidator must surface that ownership of the billing
adapter is disputed (Dana per doc 04 vs Raj's team per doc 22) and NOT silently pick one.

## Integration scope

- Plan create/change/cancel.
- Usage reporting from the Helios usage meter (doc 04) to billing.
- Proration on plan changes.

## Dependency on pricing model

The adapter's usage-reporting design depends on whether pricing is per-seat (doc 26) or
usage-based (doc 39, exec memo). Usage-based pricing requires the adapter to report
metered consumption; per-seat does not. The adapter cannot be finalized until the pricing
model is decided (RISK-12).
