# Helios Infrastructure Capacity Notes

Author: Theo (Platform engineering)
Status: working notes

## Compute

Helios services autoscale on CPU. The aggregation service (doc 09) is the most
compute-intensive component and is sized for the beta load plus headroom for GA.

## Storage

Analytics data storage is sized against the retention window. The retention window is
itself contested - Privacy (doc 28) says 90 days, platform engineering (doc 11) says
180 days (RISK-9) - so the storage estimate carries two figures: a 90-day estimate and a
180-day estimate that is double the size. Final sizing waits on the retention decision.

## Note

This infra doc does NOT take a position on regions; see the dedicated infra deployment
doc (doc 23) for the regions plan, which says US + EU at GA (conflicting with the charter
doc 01 US-only). This capacity doc is about compute and storage sizing only.

## Data store

Storage sizing also depends on whether analytics lives in the Initech Warehouse (doc 09)
or Postgres (doc 11) - RISK-7 - because the two have different storage cost profiles.
This doc notes the dependency but does not resolve the data-store conflict.
