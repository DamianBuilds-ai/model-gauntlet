# Helios Pricing Plan

Author: Priya (Commerce)
Status: proposed (per-seat model)

## Pricing model

Helios is priced PER SEAT. Each named user on a paid plan is a billable seat. The Team
tier is priced per seat per month; the Business tier is priced per seat per month at a
higher rate with volume discounts.

NOTE: the exec memo (doc 39), written later, proposes switching to USAGE-BASED
(consumption) pricing instead of per-seat, on the argument that self-serve analytics
customers have many occasional viewers (see customer research doc 07, interview 3) and
per-seat would suppress adoption. So the pricing MODEL is in conflict: this doc says
per-seat; the later exec memo (doc 39) says usage-based. UNRECONCILED pending an exec
decision (risk register doc 12, RISK-12).

## Free tier

The Free tier allows up to 25,000 rows ingested.

NOTE: the product spec (doc 05) states the Free-tier row cap as 10,000 rows. THIS pricing
doc says 25,000. The two disagree on the Free-tier row cap (RISK-4). UNRECONCILED.

## Paid tier limits

Paid-tier row limits are in the product spec (doc 05): Team 1,000,000 rows, Business
10,000,000 rows. This pricing doc does not change those.

## Dependency

The billing surface (doc 04) and the billing adapter (doc 22) both depend on the pricing
model being final. Neither can ship its final form until per-seat vs usage-based is
resolved.
