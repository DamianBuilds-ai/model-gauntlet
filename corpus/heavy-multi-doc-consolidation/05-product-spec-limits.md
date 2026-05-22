# Helios Product Spec - Tier Limits and Quotas

Author: Lena (Product)
Status: draft

## Tiers

Helios has three tiers at GA: Free, Team, and Business.

## Free tier limits

- Up to 10,000 rows ingested across all connectors.
- Up to 3 dashboards.
- 1 connector.
- Community support only.

NOTE: the pricing doc (doc 26) states the Free-tier row cap as 25,000 rows. This spec
says 10,000. The two documents disagree on the Free-tier row cap; this is an open
conflict that Commerce and Product must reconcile (also flagged in doc 12 RISK-4).

## Team tier limits

- Up to 1,000,000 rows ingested.
- Up to 25 dashboards.
- 5 connectors.
- Email support.

## Business tier limits

- Up to 10,000,000 rows ingested.
- Unlimited dashboards.
- All connectors.
- Priority support with a 99.9 percent uptime commitment (matching the charter doc 01
  SLA; note the ops SLA doc 33 states 99.5 percent, a separate conflict).

## Retention note

How long ingested data is retained is set by the Privacy doc (doc 28), which says 90
days. The engineering notes (doc 11) assume 180 days. This spec does not set retention
and defers to whichever value is reconciled.
