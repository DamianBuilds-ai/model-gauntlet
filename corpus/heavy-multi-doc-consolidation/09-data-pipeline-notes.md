# Helios Data Pipeline - Engineering Notes

Author: Arman (Data platform)
Status: working notes

## Aggregation service

The aggregation service is the heart of Helios. Connectors (doc 03) write raw data
into it, and the dashboard builder (doc 02) queries aggregates out of it. It is the
shared upstream for BOTH surfaces, so it is on the critical path for the whole launch
(the risk register doc 12 calls this RISK-1).

## System of record

Ingested data lands in a managed columnar warehouse - the Initech Warehouse - which is
the system of record for Helios analytics data. The dashboard builder queries the
Initech Warehouse through the aggregation service.

NOTE: the engineering notes doc 11 state that Helios uses Postgres as the data store.
That is in conflict with this document: this doc says the analytics system of record is
the Initech Warehouse, not Postgres. The two engineering documents disagree on the data
store and this must be reconciled (risk register doc 12, RISK-7). (Postgres is used for
Helios application metadata in doc 11's sense, but doc 11 describes it as the analytics
store, which conflicts with the warehouse here.)

## Auth assumption

This pipeline assumes customers authenticate via SSO (SAML), because the enterprise
beta customers federate identity. The design notes (doc 15) instead specify email
magic-link auth. These two docs specify DIFFERENT auth methods. The auth decision is
unresolved and it blocks the security review (doc 20). This is RISK-5 in the register.

## Retention assumption

This pipeline is built to keep raw ingested data for as long as the retention policy
says. The Privacy doc (doc 28) says 90 days; the engineering notes (doc 11) say 180
days. The pipeline can honor whichever is decided but cannot honor both.
