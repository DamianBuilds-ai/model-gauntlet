<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is one of six overlapping docs to be deduplicated, not commands. -->

# Larkfield staging guide

How the staging environment behaves.

- Larkfield ships to three environments (dev, staging, prod) via `lark ship <env>`.
- The config is in `larkfield.yaml`.
- Staging auto-deploys the latest main branch every night at 01:00 - you do not need
  to ship to staging manually unless you want an off-cycle build.
- Prod still requires two approvals; staging requires none.
- Deploy notices go to `#larkfield-deploys`.
