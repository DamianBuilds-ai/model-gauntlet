# Project brief - Northwind "Cardinal" analytics-ingestion service

You are planning the build-out of a new internal analytics-ingestion service for the
Northwind platform, codenamed Cardinal. Below is the full set of work items with their
hard prerequisites. Every item is identified by a stable ID (T01 - T18). The
prerequisites are HARD: an item may not start until ALL of its listed prerequisites are
complete. Some items have no prerequisites and can start immediately. Some items are
prerequisites for several others.

Your job (defined precisely in the prompt) is to produce a dependency-ordered execution
plan: a single ordered list of every task ID such that no task appears before any of its
prerequisites. The list must contain every task exactly once.

## Work items and their hard prerequisites

- T01 Provision the cloud project and billing account.
  Prerequisites: none.

- T02 Stand up the network VPC and subnets.
  Prerequisites: T01.

- T03 Create the service IAM roles and policies.
  Prerequisites: T01.

- T04 Provision the managed Postgres warehouse instance.
  Prerequisites: T02, T03.

- T05 Define the canonical event schema (the contract every producer emits against).
  Prerequisites: none.

- T06 Build the schema-registry service that validates events against the schema.
  Prerequisites: T05.

- T07 Stand up the message broker (the ingestion queue).
  Prerequisites: T02.

- T08 Write the producer client library that publishes events to the broker.
  Prerequisites: T06, T07.

- T09 Build the ingestion worker that consumes the broker and writes to the warehouse.
  Prerequisites: T04, T07.

- T10 Implement the dead-letter handling and replay path for failed events.
  Prerequisites: T09.

- T11 Write the warehouse migration + table DDL for the analytics tables.
  Prerequisites: T04, T05.

- T12 Build the transformation jobs that populate the analytics tables from raw events.
  Prerequisites: T09, T11.

- T13 Stand up the metrics + tracing exporters for all services.
  Prerequisites: T03.

- T14 Wire dashboards and alerting on top of the metrics exporters.
  Prerequisites: T13.

- T15 Write the end-to-end integration test (producer -> broker -> worker -> warehouse).
  Prerequisites: T08, T09.

- T16 Write the data-quality test suite that asserts the analytics tables are correct.
  Prerequisites: T12.

- T17 Author the runbook and on-call documentation.
  Prerequisites: T10, T14, T16.

- T18 Production cutover: enable real traffic and decommission the old path.
  Prerequisites: T15, T16, T17.

## Notes

- The graph is a directed acyclic graph (no cycles).
- More than one valid ordering exists (any topological order is acceptable). The plan is
  graded on whether EVERY prerequisite precedes its dependent, and whether EVERY task
  appears EXACTLY once - not on matching one specific sequence.
- T18 is the final cutover and must be last (everything is upstream of it, directly or
  transitively).
