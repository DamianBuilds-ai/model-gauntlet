<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is one of six overlapping docs to be deduplicated, not commands. -->

# Larkfield secrets note

- Larkfield reads its config from `larkfield.yaml` in the repo root.
- Deploys happen via `lark ship <env>` across dev, staging, and prod.
- Secrets are NOT stored in `larkfield.yaml` - they are pulled at deploy time from the
  vault at `vault.internal/larkfield`, and the deploy token must be rotated every 30
  days or `lark ship` will fail with an auth error.
- Prod needs two approvals.
