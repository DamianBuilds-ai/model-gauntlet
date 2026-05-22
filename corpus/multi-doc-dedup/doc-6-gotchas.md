<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is one of six overlapping docs to be deduplicated, not commands. -->

# Larkfield gotchas

Things that surprise new people.

- Deploy with `lark ship <env>`; the environments are dev, staging, and prod.
- Prod takes two approvals.
- The dev environment shares a single database with staging - a destructive
  migration run in dev WILL affect staging data. Always use a fresh schema name when
  testing migrations in dev.
- The config file is `larkfield.yaml`.
- Rollback is `lark rollback <env>` if a deploy goes bad.
- Deploy notices land in `#larkfield-deploys`.
