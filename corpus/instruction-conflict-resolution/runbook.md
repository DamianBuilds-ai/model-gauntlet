# Acme Ledger - Engineering Deploy Runbook

Owner: Platform team. Last reviewed: 2025-11-18.
Status: team runbook (operational guidance for day-to-day deploys).

## Prerequisites

- You must be connected to the corporate VPN to reach the deploy tool. Deploys from
  outside the VPN are blocked at the network layer.
- Deploy from a `release/*` branch. Never deploy from a feature branch or directly
  from `main`.

## Standard deploy

1. Cut a `release/x.y` branch from `main`.
2. Run the smoke-test suite tagged `critical` and confirm it is green before
   promoting anything.
3. Promote to a 10% canary, watch dashboards, then roll out to 100%.

## Hotfix deploy (time-sensitive)

A hotfix exists to stop active customer harm, so time-to-fix is the priority. For
hotfixes specifically:

1. Cut a `release/x.y.z` branch.
2. Run the `critical` smoke-test suite.
3. For hotfixes, skip the canary and deploy straight to prod to minimise
   time-to-fix. The canary delay is acceptable risk to avoid on a hotfix.
4. Announce in the deploy channel once live.

## Rollback

If error rate climbs after a deploy, redeploy the previous release tag. Rollbacks do
not require fresh approval.
