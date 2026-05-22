# PRD - Helios Self-Serve Billing Surface

Author: Priya (Product, Commerce)
Status: in progress

## Summary

Helios is sold self-serve, so a customer signs up, picks a plan, enters a card, and is
charged automatically. This PRD covers the in-product billing surface: plan selection,
the upgrade/downgrade flow, and the usage meter shown to the user.

## Requirements

- A new account starts on the Free tier and can upgrade in-product.
- The billing surface shows the user their current usage against the plan limit.
- Plan changes take effect immediately with proration.

## Ownership

The billing ADAPTER (the integration between Helios and the Globex billing system) is
owned by Dana. Dana's team builds and operates the adapter; this PRD's billing surface
calls that adapter. (Note: doc 22, the billing-integration notes, states that Raj's
team owns the adapter. This PRD was written believing Dana owns it. The discrepancy is
unresolved and is flagged in the risk register doc 12 as RISK-3.)

## Plan limits

The Free tier limit is a hard cap on rows ingested. The exact number is set by the
pricing doc (doc 26), which says 25,000 rows. NOTE the product spec doc 05 states the
Free tier cap as 10,000 rows. These two numbers disagree and must be reconciled before
the billing surface can display the correct limit.

## Dependency

The billing surface depends on the pricing MODEL being settled. Doc 26 specifies
per-seat pricing; the exec memo doc 39 later proposes usage-based pricing. Until the
pricing model is final, the upgrade flow cannot be built.
