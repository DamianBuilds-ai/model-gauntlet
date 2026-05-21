# Decision Brief - Analytics Platform Selection

Synthetic corpus doc 1 of 16. Fictional company "Riverbend" (a mid-market logistics
SaaS) must choose ONE data and analytics platform to standardise on for the next
three years. This doc set is the research dossier a Researcher must synthesise into a
single recommendation. The tradeoffs (cost, latency, ops burden, scaling, compliance)
are spread across the docs - no single doc has the whole picture. Synthetic data only.

## The decision

Pick ONE of three candidate platforms for Riverbend's central analytics warehouse:

- **Lumen Cloud** - a fully managed cloud data warehouse.
- **Strato DB** - a self-managed open-source columnar database Riverbend would run on
  its own infrastructure.
- **Beacon Analytics** - a managed analytics platform with a built-in BI layer.

## Constraints that matter to Riverbend

- Riverbend has a SMALL data team (3 engineers). Operational burden is a first-order
  concern, not an afterthought.
- Riverbend handles EU customer data, so data-residency and compliance posture matter.
- Query latency on interactive dashboards matters to internal users.
- Three-year total cost matters more than month-one cost.
- Expected data volume roughly 5x over three years.

## What the rest of this dossier contains

Vendor one-pagers, two independent benchmark write-ups, a cost analysis, a compliance
memo, an ops/postmortem note, a community-forum thread, an analyst note, and a couple
of internal Slack-thread captures. Read them all - the tradeoffs are deliberately
distributed and at least one source is not trustworthy.
