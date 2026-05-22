# Data Pipeline Notes - Globex Insight

Author: data engineering.

## Pipeline shape

The pipeline ingests consumption, billing, and activity events, transforms them, and
serves them to the dashboard panels.

## Storage

- The pipeline writes to PostgreSQL as the primary store for the dashboard's serving
  layer. All three panels read from Postgres.

  (Note: the platform migration plan names a different primary store. Confirm which is
  authoritative before build - this needs reconciling.)

## Serving components

- A cache layer sits in front of the serving store to absorb dashboard read bursts.
- A read replica of the primary store handles heavy analytical reads so they do not hit
  the write path.

  (The cache layer and the read replica are SEPARATE components serving different
  purposes; both exist in the design.)

## Authentication

- The dashboard authenticates customer users via SAML SSO. Enterprise accounts
  federate through their identity provider.

  (Note: the design notes describe a different auth method. This needs reconciling
  before the security review can start.)

## Dependencies

- Feeds all three dashboard panels (usage, billing, activity).
