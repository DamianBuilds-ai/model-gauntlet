# Helios Aggregation Service - Deep Notes

Author: Arman (Data platform)
Status: working notes

## Why this is the critical path

The aggregation service ingests connector data (doc 03) and serves aggregates to the
dashboard builder (doc 02). Both surfaces depend on it, so it is the highest-fanout
dependency in the project (RISK-1, doc 12). If the aggregation service slips, the builder
and the connectors both slip, and the GA date (now October 6 per doc 18) is at risk.

## Current state

- Ingest path: working in dev for the three GA connectors.
- Query path: working for the basic aggregations the builder needs; the 2-second
  first-widget bar (docs 02, 11) is being met in dev.
- Incremental sync: the 15-minute incremental cadence (doc 03) is implemented.

## Open technical risk

The service writes to the analytics data store, which is contested: this doc and the
data-pipeline notes (doc 09) treat the Initech Warehouse as the store, but the platform
engineering notes (doc 11) say Postgres (RISK-7). The aggregation service is currently
built against the Initech Warehouse. If the decision lands on Postgres, parts of the query
path must be reworked, which would threaten the October 6 date. This doc flags the
data-store conflict as a schedule risk, not just a documentation discrepancy.

## Dependency on auth

The aggregation service enforces per-account data isolation, which depends on the identity
model. The auth conflict (SSO doc 09 vs magic-link doc 15, RISK-5) affects how account
identity is resolved, so this service has a soft dependency on the auth decision too.
