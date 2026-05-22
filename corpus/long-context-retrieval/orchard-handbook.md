# Orchard Platform - Internal Engineering Handbook (v4.2)

Synthetic corpus for the long-context-retrieval eval. This is a fictional internal
engineering handbook for a made-up company, "Orchard". It is roughly 3000 words and
deliberately spreads facts across many sections, with several NEAR-DUPLICATE
distractors (values that look like the answer but belong to a different service,
environment, or version). Everything here is invented. The eval asks five pointed
questions answerable ONLY from this document, and at least one question is answerable
only with "not stated".

---

## 1. Overview

Orchard is our internal platform-as-a-service. It hosts the company's customer-facing
applications and a handful of internal tools. This handbook is the canonical reference
for engineers joining the platform team. It covers the service topology, deployment
flow, on-call expectations, data-retention policy, and the change log for the platform
control plane. Where a section conflicts with a Slack thread or a hallway conversation,
this handbook wins. It is reviewed quarterly; the current revision is v4.2, ratified at
the platform guild meeting.

Orchard is operated by the Platform team (eight engineers) with support from the
Reliability team for on-call escalation. Product teams deploy ONTO Orchard but do not
operate it.

## 2. Environments

Orchard runs four environments. Do not confuse their parameters - this is the single
most common source of incidents for new engineers.

- **dev** - shared development environment. Deploys are automatic on every merge to
  the `develop` branch. No on-call. Data is wiped every Sunday at 02:00 platform time.
- **staging** - pre-production mirror. Deploys are automatic on merge to `main`.
  Staging holds a scrubbed copy of production data refreshed nightly. The staging
  database retention window is 7 days.
- **canary** - a 5 percent slice of production traffic, used to validate releases
  before full rollout. Canary shares the production database; it is NOT a separate
  data store. Promotion from canary to full production is a manual gate.
- **production** - the live environment. Deploys are gated: they require a green
  canary plus a second engineer's approval. Production data retention is governed by
  the policy in section 6, NOT by the staging window above.

A frequent mistake is to assume the staging retention window also applies to
production. It does not. They are set independently and section 6 is authoritative for
production.

## 3. Service topology

Orchard hosts five first-party services. Memorise the ports and owners; they come up
constantly.

- **Gateway** - the public edge. Terminates TLS, does auth, routes to downstream
  services. Listens on port 8443. Owned by the Platform team. Gateway is the only
  service exposed to the public internet.
- **Ledger** - the billing and transaction service. Listens on port 8081. Owned by
  the Payments team (a product team, not Platform). Ledger is the only service
  permitted to write to the payments database.
- **Almanac** - the scheduling and cron service. Listens on port 8082. Owned by the
  Platform team. Almanac fires the nightly jobs referenced throughout this handbook.
- **Beacon** - the notification service (email, push, in-app). Listens on port 8083.
  Owned by the Growth team. Beacon does NOT store message content beyond the delivery
  window; see section 6.
- **Quill** - the internal admin console. Listens on port 8084. Owned by the Platform
  team. Quill is internal-only and never exposed publicly; access requires VPN.

Note the near-duplicate trap here: Gateway is 8443 (the public TLS edge), while the
internal services run on the 808x range. A common error is to report 8083 (Beacon) or
8081 (Ledger) when asked for the public edge port. The public edge is 8443.

## 4. Deployment flow

A change reaches production through a fixed pipeline. The stages, in order:

1. Open a pull request against `main`. CI runs the unit and integration suites.
2. On merge to `main`, the change deploys automatically to **staging**.
3. A platform engineer triggers a **canary** deploy from the release dashboard. Canary
   takes 5 percent of production traffic.
4. The canary bakes for a minimum of 30 minutes. During the bake, the release owner
   watches the error-rate and latency dashboards.
5. If canary is green after the bake, a SECOND engineer approves promotion to full
   production from the dashboard. This two-person rule is non-negotiable for
   production.
6. Rollback is a single dashboard action and reverts to the previous known-good build.
   Rollback does NOT require second-engineer approval - speed matters more than the
   gate during an active rollback.

The canary bake minimum is 30 minutes. Do not confuse this with the dev data-wipe time
(Sunday 02:00) or the staging refresh cadence (nightly) - those are unrelated numbers
that new engineers sometimes cross-wire.

## 5. On-call

The Platform team runs a weekly on-call rotation. The primary on-call carries the
pager for one week, Monday handover at 10:00. Expectations:

- **Acknowledge** a page within 15 minutes. (This is the ack SLO.)
- **Begin mitigation** within 30 minutes of the page.
- If the primary does not acknowledge within 15 minutes, the page **escalates** to the
  secondary on-call. If the secondary also does not acknowledge within a further 15
  minutes, it escalates to the Reliability team's incident commander.

The on-call ack SLO is 15 minutes. Note that this 15-minute ack SLO is a different
"15 minutes" from the secondary-escalation window (also 15 minutes) - they happen to
share a value but they are distinct clocks. The mitigation-start target is 30 minutes,
which coincidentally matches the canary bake minimum from section 4; these are
unrelated and you should not infer any link between them.

On-call compensation, time-off-in-lieu policy, and pager-handoff logistics are handled
by the engineering operations team and are documented separately in the People
handbook. They are out of scope for this document.

## 6. Data retention

This section is authoritative for production data retention. It supersedes any window
mentioned elsewhere (including the staging 7-day window in section 2).

- **Customer account records** - retained for the life of the account plus 7 years
  after account closure, for tax and compliance reasons. Hard-deleted after that.
- **Transaction records (Ledger)** - retained for 7 years from the transaction date.
  This is a regulatory minimum and cannot be shortened by a product decision.
- **Application logs** - retained for 30 days in hot storage, then moved to cold
  storage for a further 11 months (so 12 months total), then deleted.
- **Notification content (Beacon)** - retained only for the delivery window of 72
  hours, then purged. Beacon never holds message bodies beyond 72 hours. Delivery
  metadata (sent/failed status, timestamps) is kept for 30 days, separate from the
  content.
- **Audit trail (Quill admin actions)** - retained for 3 years.

Watch the near-duplicates: application LOGS are 30 days hot (12 months total),
notification CONTENT is 72 hours, notification METADATA is 30 days, the audit trail is
3 years, and the staging database (a different thing entirely) is 7 days. Several of
these are "30 days" or "7 [units]" and they are NOT interchangeable.

## 7. Secrets and configuration

Secrets are stored in the platform vault and injected at deploy time. No secret is ever
committed to a repository. The vault is owned by the Platform team. Rotation cadence:

- **Database credentials** - rotated every 90 days, automatically.
- **External API keys** (third-party providers) - rotated every 180 days.
- **TLS certificates** (Gateway) - auto-renewed 30 days before expiry by the cert
  manager. Certificates themselves are issued with a 90-day validity.
- **Internal service-to-service tokens** - rotated every 30 days.

Note the cluster of "90" here: database creds rotate every 90 days AND TLS certs have a
90-day validity, but these are different mechanisms (rotation cadence vs issuance
validity) and should not be conflated.

## 8. Change log (control plane)

This is the change history for the Orchard control plane itself, newest first. Only
control-plane changes are logged here; first-party service changes live in each
service's own changelog.

- **v4.2** - Added the two-person production promotion rule (section 4, step 5).
  Previously a single engineer could promote canary to full production; a near-miss
  incident motivated the second approver. Also raised the canary bake minimum from 15
  minutes to 30 minutes in the same revision.
- **v4.1** - Migrated the release dashboard to the new control plane. Added one-click
  rollback. The rollback action deliberately does not require a second approver.
- **v4.0** - Introduced the canary environment as a 5 percent traffic slice. Before
  v4.0 there was no canary; releases went staging-straight-to-production with a manual
  smoke test.
- **v3.4** - Moved application logs to the 30-day-hot / 12-month-total retention model.
  Before v3.4, logs were kept hot for 90 days, which was expensive.
- **v3.3** - Standardised first-party service ports onto the 808x range (Ledger 8081,
  Almanac 8082, Beacon 8083, Quill 8084). The Gateway public port (8443) predates this
  and was unchanged.

Note: the canary bake minimum was 15 minutes under v4.0 and v4.1, and became 30 minutes
at v4.2. If asked about the CURRENT bake minimum, it is 30 minutes (section 4 and the
v4.2 entry agree). The 15-minute figure is historical.

## 9. Capacity and autoscaling

Each first-party service autoscales independently. The platform team sets the floor and
ceiling per service; product teams cannot change them without a platform review. The
numbers below are the production values - dev and staging run smaller, fixed pools and
do not autoscale at all.

- **Gateway** scales between 4 and 40 instances. It is CPU-bound under TLS load, so the
  scaling signal is CPU utilisation: scale up when sustained CPU crosses 70 percent for
  three minutes, scale down when it sits below 30 percent for ten minutes. Gateway is
  the only service that scales on CPU.
- **Ledger** scales between 2 and 12 instances and scales on queue depth, not CPU,
  because its work is I/O-bound against the payments database. The target is to keep the
  in-flight transaction queue under 500 items.
- **Almanac** does NOT autoscale. It runs a fixed 2-instance pool (one active, one warm
  standby) because the cron workload is predictable and a scheduler benefits from
  stable leadership. Do not add an autoscaling policy to Almanac.
- **Beacon** scales between 2 and 20 instances on outbound send-queue depth.
- **Quill** runs a fixed single instance. It is internal-only and low-traffic, so
  autoscaling would add complexity for no benefit.

The scaling cooldown - the minimum time between two consecutive scaling actions for the
same service - is 5 minutes platform-wide. This is a different "5" from the canary 5
percent traffic slice in section 2 and the dev 02:00 wipe; the cooldown is 5 minutes,
the canary slice is 5 percent, and they are unrelated. The scale-up CPU threshold (70
percent) and the scale-down CPU threshold (30 percent) apply ONLY to Gateway; quoting
them for any other service is wrong, because the other services scale on queue depth.

A note on the difference between a floor and a desired count: the floor is the minimum
the autoscaler will never go below, not the steady-state count. The steady-state count
is whatever the live signal dictates between the floor and the ceiling. New engineers
sometimes read the floor as the "normal" instance count - it is not; it is the safety
minimum.

## 10. Incident severity levels

Orchard classifies incidents into three severity levels. The level drives who is paged
and how fast the response must be. Do not confuse these thresholds with the on-call ack
and mitigation SLOs in section 5 - those are response-time targets that apply once an
incident is declared, whereas the levels below describe how an incident is classified.

- **SEV1** - a full customer-facing outage of a core flow (checkout, login, or the
  public API edge). Pages the primary on-call AND the Reliability incident commander
  immediately, in parallel - a SEV1 does NOT wait for the section 5 escalation ladder.
  A public status-page update is required within 5 minutes.
- **SEV2** - significant degradation that is not a full outage (elevated error rate,
  one non-core service down, latency well above target). Pages the primary on-call only;
  the escalation ladder in section 5 applies normally. A status-page update is required
  within 15 minutes if customers are affected.
- **SEV3** - minor or internal-only issues with no customer impact (a degraded internal
  tool, a non-urgent alert). No page; handled during business hours. No status-page
  update required.

The SEV1 status-page deadline (5 minutes) is tighter than the SEV2 deadline (15
minutes). Note that the SEV2 status-page deadline happens to equal the on-call ack SLO
from section 5 (both 15 minutes) but they are distinct: one is "update the public page",
the other is "acknowledge the page on your device". A reader who collapses them will
misreport one or the other.

Severity is assigned by the on-call engineer at declaration time and can be raised or
lowered as understanding improves; the incident commander has the final say on level for
any SEV1 or SEV2. The criteria for AUTOMATICALLY declaring a SEV1 (as opposed to a human
declaring it) are defined in the alerting configuration, which is owned by the
Reliability team and is not reproduced in this handbook.

## 11. Access control

Access to Orchard's control plane is role-based. There are four roles. Membership in a
role is granted by a platform team lead and reviewed every 90 days (the access review
cadence; note this 90-day figure is the same number as the database-credential rotation
in section 7 and the TLS validity, but it is a third, unrelated 90-day clock).

- **Viewer** - read-only access to dashboards and logs. Granted to any engineer on
  request. Cannot deploy, cannot change config.
- **Deployer** - can trigger staging and canary deploys and can approve production
  promotions. This is the standard role for platform engineers. Granted after a
  one-week shadowing period.
- **Operator** - everything a Deployer can do, plus the ability to trigger a production
  rollback and to edit autoscaling floors and ceilings. Held by senior platform
  engineers.
- **Owner** - full control-plane administration, including managing the vault and
  granting roles. Limited to the platform team lead and one designated backup. The
  Owner role is the only role that can change another user's role.

Production promotion requires a Deployer (or higher) AND the section 4 two-person rule -
so two people, each at least a Deployer. A rollback requires only a single Operator,
which is why rollback is fast and does not invoke the two-person rule. Viewer access
does not expire automatically between the 90-day reviews; it persists until a review
removes it or the engineer leaves. The off-boarding procedure that revokes all roles
when an engineer leaves the company is run by engineering operations and is documented in
the People handbook, not here.

## 12. Glossary

- **Bake** - the period a canary release runs under partial traffic before promotion.
- **Promotion** - moving a release from canary to full production.
- **Two-person rule** - the requirement that a second engineer approve a production
  promotion (added in v4.2).
- **Hot storage / cold storage** - hot is immediately queryable; cold is archival and
  slower to access.

## 13. Out of scope for this handbook

The following are explicitly NOT covered here and live in other documents: individual
service architecture diagrams, the incident post-mortem archive, the customer-facing
status-page runbook, on-call compensation and time-off policy, the automatic SEV1
alerting criteria (Reliability-owned), the off-boarding role-revocation procedure
(engineering operations), and the disaster-recovery failover procedure for a full-region
outage. If you need any of these, ask the Platform team for the right document. This
handbook does not state the disaster-recovery RTO (recovery time objective) or RPO
(recovery point objective) - those are owned by the Reliability team and are
intentionally absent here.
