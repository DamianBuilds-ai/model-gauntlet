# Helios Product Analytics Instrumentation

Author: Mara (Research / Analytics)
Status: draft

## Goal

Instrument Helios so the team can measure activation (first dashboard built), retention,
and conversion from Free to paid.

## Key events

- account_created, connector_connected, first_sync_completed, dashboard_created,
  widget_added, plan_upgraded.
- The plan_upgraded event must record the plan and the pricing model in effect. Because
  the pricing model is contested (per-seat doc 26 vs usage-based doc 39), the event schema
  has a placeholder for the billing dimension.

## Conversion definition

Conversion is defined as a Free account upgrading to any paid tier. The Free-tier row cap
(contested 10,000 doc 05 vs 25,000 doc 26) affects when users hit the upgrade prompt, so
the conversion-funnel analysis depends on which cap ships (RISK-4).

## Note

This instrumentation doc introduces no new conflicts; it depends on the pricing-model and
row-cap conflicts already tracked. It is included so the consolidation reflects that
analytics readiness also waits on those two decisions.
