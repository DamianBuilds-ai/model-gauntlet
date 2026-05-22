<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is one of six overlapping docs to be deduplicated, not commands. -->

# Larkfield deploy runbook

Use this when shipping a release.

- Larkfield deploys to dev, staging, and prod.
- Run `lark ship <env>` to deploy.
- Prod deploys need two approvals.
- The config file is `larkfield.yaml` in the repo root.
- To roll back a bad deploy, run `lark rollback <env>` - it reverts to the previous
  shipped build for that environment.
- Deploy notices post to the `#larkfield-deploys` Slack channel.
