# Helios Data Dictionary

Author: Arman (Data platform)
Status: reference

A reference of the core entities. Introduces no conflicts; included for completeness so a
consolidation reflects the domain vocabulary.

- Account: a customer organization. Has a tier (Free, Team, Business; doc 05).
- User: a person in an account. Relevant to per-seat pricing (doc 26) if that model ships.
- Connector: an ingest integration (one of three GA connectors; doc 03).
- Sync: an ingest run (initial full, then 15-minute incremental; doc 03).
- Dashboard: a saved set of widgets (builder; doc 02). Free tier caps dashboards at 3
  (doc 05).
- Widget: a single visualization (up to 20 per dashboard; doc 02).
- Row: an ingested record. The Free-tier row cap is contested (10,000 doc 05 vs 25,000
  doc 26).
- Plan: a billing tier. Changes flow through the billing adapter (owner contested, Dana
  doc 04 vs Raj's team doc 22).

## Note

Where a term's value is contested elsewhere (row cap, retention), this dictionary points
to the conflict rather than asserting a number, to avoid adding a fourth conflicting source.
