# Cardinal Logistics - Incident Response Runbook

How to run an incident from page to post-mortem. This runbook is reviewed after
every Sev-1 and Sev-2.

## Severity levels

- Sev-1: customer-facing outage or data loss. All hands.
- Sev-2: degraded service, partial impact, or a stuck queue.
- Sev-3: internal-only or cosmetic.

## Page and acknowledge

When a page fires, the primary on-call acknowledges in the paging tool. The primary
has 10 minutes to acknowledge before the page escalates to the secondary - this is
the standard acknowledgement timeout (see CL-2026-014, which reduced it after the
2026-03-14 missed-page incident). Acknowledging does not mean resolved; it means a
human owns it.

## Declare and communicate

For Sev-1 and Sev-2, declare the incident in the incident channel and post an
initial status update within 30 minutes. Updates every 30 minutes until resolved.

## Mitigate

Prefer mitigation over root-cause during an active incident. Rollback is the first
tool: a single on-call engineer can execute a rollback without a second approver.
Promotion to production is different and needs the two-person rule, but rollback is
single-approver by design.

## Post-mortem

Blameless post-mortem within 5 business days for every Sev-1 and Sev-2. The
2026-03-14 missed-page incident is the canonical example - its action item was the
escalation-timeout reduction recorded in ADR-031.
