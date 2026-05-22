# Helios Vendor Notes - Initech Warehouse

Author: Arman (Data platform)
Status: reference

Notes on the managed columnar warehouse vendor (Initech Warehouse) used as the analytics
store in the data-pipeline design (doc 09).

## Why the warehouse

- Columnar storage suits the aggregation/dashboard query pattern (doc 02).
- Managed service reduces operational burden on the (contested, RISK-10) on-call team.
- Scales with the retention window (90 vs 180 days, RISK-9) and the tier row caps (doc 05).

## The data-store conflict (restated)

This vendor doc assumes the Initech Warehouse is the analytics system of record (matching
data-pipeline doc 09). The platform engineering notes (doc 11) instead name Postgres as the
analytics store. The two engineering positions conflict (RISK-7). This doc does not resolve
the conflict; it documents the warehouse option that doc 09 and the aggregation service (doc
25) are built against. If the decision lands on Postgres, this vendor relationship is moot
and the aggregation query path (doc 25) needs rework, threatening the October 6 GA (doc 18).

## Cost

Warehouse cost scales with stored volume, so it is sensitive to the retention decision (90
vs 180 days). Infra (doc 19) carries both estimates pending that decision.
