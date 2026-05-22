# Helios Engineering Notes - Platform

Author: Theo (Platform engineering)
Status: working notes

## Architecture summary

Helios is a set of services behind the Globex API gateway. The application metadata
(accounts, dashboards definitions, connector configs) lives in Postgres. Analytics
queries run against the data store.

## Data store

These notes describe Postgres as the Helios data store for analytics. NOTE: the
data-pipeline notes (doc 09) say the analytics system of record is the Initech
Warehouse, NOT Postgres. This is a direct conflict on the analytics data store between
this doc and doc 09 (risk register doc 12, RISK-7). Both cannot be the system of record
for analytics; the conflict must be reconciled.

## Performance bar

The Platform team agreed with Product (doc 02) that the dashboard builder must render
the first widget within 2 seconds on a typical dataset. That bar is in the builder PRD.

## Retention

Engineering plans to retain ingested data for 180 days. NOTE: the Privacy doc (doc 28)
specifies 90 days. This doc (180 days) and doc 28 (90 days) conflict on the retention
window (risk register doc 12, RISK-4 is the row cap; the retention conflict is RISK-9).

## On-call ownership

Post-launch, the Platform team expects to own Helios on-call, folding it into the
existing platform rotation. NOTE: the org doc (doc 35) says a NEW dedicated Helios team
will own Helios on-call after launch, not the Platform team. Who owns Helios on-call
post-launch is contested between this doc and doc 35 (risk register doc 12, RISK-10).

## Regions

These notes assume a single US deployment at GA, matching the charter (doc 01). The
infra doc (doc 23) and GTM doc (doc 30) instead plan US + EU at GA. Regions at GA are
contested.
