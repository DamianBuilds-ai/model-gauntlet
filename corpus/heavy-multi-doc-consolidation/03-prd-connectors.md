# PRD - Helios Data Connectors

Author: Lena (Product)
Status: in progress

## Summary

Connectors ingest a customer's operational data into Helios so the dashboard builder
(doc 02) can query it. At GA, Helios ships connectors for the three most-used Globex
data sources: the Orders API, the Inventory export, and the Billing export.

## Requirements

- Each connector runs an initial full sync, then incremental syncs every 15 minutes.
- A connector surfaces sync status (last sync time, row count, errors) to the user.
- Connector data lands in the aggregation service (doc 09), which is the shared
  upstream that the dashboard builder also reads from.

## Dependencies

- The connectors depend on the aggregation service (doc 09). This is the SAME shared
  upstream the dashboard builder (doc 02) depends on, so a slip in the aggregation
  service blocks BOTH the builder and the connectors. This is the single highest-fanout
  dependency in the project (see the risk register doc 12, RISK-1).
- The Billing-export connector additionally touches the billing integration (doc 22),
  whose owner is contested (doc 04 says Dana owns the billing adapter; doc 22 says
  Raj's team does).

## Out of scope

Custom/arbitrary connectors (a generic webhook ingest) are explicitly a fast-follow,
not GA. Only the three named connectors ship at GA.
