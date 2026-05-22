# Incident Response

## Scope

This runbook covers security and availability incidents affecting production
systems or customer data.

## Severity levels

- SEV1: customer-facing outage or confirmed data breach. All hands.
- SEV2: significant degradation or a near-miss security event.
- SEV3: minor, contained issue with a workaround.

## On-call

Engineering runs a follow-the-sun on-call rotation across the three hubs. The
primary on-call acknowledges a SEV1 page within 15 minutes. If unacknowledged, the
page escalates to the secondary, then to the engineering director.

## Investigation and evidence

When investigating an incident, responders pull the relevant audit logs from the
central log platform. Because audit logs are retained for 90 days, any
investigation must collect and preserve the relevant log evidence within that
window; for incidents under legal hold, the security team exports the evidence to
long-term storage so it survives the standard 90-day purge.

## Communication

SEV1 incidents get a status page update within 30 minutes and hourly updates
until resolved. Customer-impacting incidents are reported against the SLA in
09-customer-sla.md.

## Post-incident review

Every SEV1 and SEV2 gets a blameless post-incident review within five business
days, with action items tracked to completion.
