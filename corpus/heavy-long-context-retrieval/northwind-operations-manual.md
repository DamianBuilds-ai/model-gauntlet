# Northwind Logistics Platform - Operations Reference Manual

Document revision 11.3. This manual is the single internal reference for operating
the Northwind Logistics Platform ("the Platform"). It supersedes all earlier
operations wikis. Everything an on-call engineer, a release manager, or a support
lead needs to operate the Platform in steady state and during incidents is described
here. The manual is intentionally long and self-contained: do not rely on tribal
knowledge or external pages. If a fact is not in this manual, it is not an
authoritative fact about the Platform.

Northwind is a fictional company used purely for internal training material. All
names, numbers, vendors, and events in this manual are invented. The vendor names
that appear (Globex for object storage, Initech for managed Postgres, Umbra for the
CDN, Acme for the SMS gateway) are placeholders.

---

## Section 1 - Platform overview and bounded contexts

The Platform moves freight bookings from quote to delivery. It is decomposed into
seven services, each owning a bounded context and its own datastore. The services
are: Quoter, Booker, Dispatcher, Tracker, Biller, Notifier, and the public Gateway.
No service reaches into another service's database directly; all cross-service reads
go through published APIs or the event bus.

- Quoter owns price quotes. A quote is valid for 14 days from issue. After 14 days a
  quote expires and must be regenerated; an expired quote cannot be booked.
- Booker owns confirmed bookings. A booking transitions through the states DRAFT,
  CONFIRMED, IN_TRANSIT, DELIVERED, and CANCELLED. Only Booker may write booking
  state; every other service treats booking state as read-only.
- Dispatcher owns carrier assignment and route planning. It consumes CONFIRMED
  bookings and produces a dispatch plan.
- Tracker owns shipment tracking events ingested from carriers.
- Biller owns invoicing and payment capture.
- Notifier owns outbound customer communications (email, SMS, push).
- Gateway is the single public ingress. It is the only service exposed to the public
  internet; the other six are reachable only on the private service network.

The Platform processes, in steady state, roughly 240,000 bookings per day at peak
season and roughly 90,000 bookings per day in the off-season. Peak season is defined
as 15 November through 10 January inclusive. These booking volumes are descriptive,
not capacity limits; the capacity limits are in Section 9.

Each service is owned by exactly one team. Quoter and Biller are owned by the
Commerce team. Booker and Dispatcher are owned by the Fulfillment team. Tracker is
owned by the Visibility team. Notifier is owned by the Messaging team. Gateway is
owned by the Edge team. The Reliability team owns no single service; it owns
cross-cutting concerns (capacity, disaster recovery, the error budget policy) and is
deliberately separate from the service-owning teams.

---

## Section 2 - Network topology and ports

The Platform runs in three regions: the primary region is us-central, the secondary
region is us-east, and a read-only analytics replica lives in eu-west. Write traffic
is served only from us-central. us-east is a warm standby that can be promoted to
primary during a regional failover (see Section 13). eu-west never serves write
traffic and never gets promoted; it exists for the analytics warehouse only.

Every service listens on its own internal port on the private service network. These
internal ports are NOT reachable from the public internet:

- Quoter listens on internal port 7001.
- Booker listens on internal port 7002.
- Dispatcher listens on internal port 7003.
- Tracker listens on internal port 7004.
- Biller listens on internal port 7005.
- Notifier listens on internal port 7006.

The Gateway is the only public ingress. The Gateway terminates TLS and accepts public
traffic on port 8443. Port 8443 is the single public edge port for the entire
Platform; no other port is exposed to the public internet. Internally, the Gateway
forwards to the service ports listed above over the private network. There is also an
internal admin console served by the Gateway on internal port 7000, reachable only
over the company VPN; the admin console is never exposed publicly.

A health-check endpoint is exposed on each service at internal port 9100 for the
metrics scraper. Port 9100 is internal-only and is shared by all services for
Prometheus-style scraping; it carries no booking data.

Do not confuse the internal service ports (the 700x range), the metrics port (9100),
the internal admin port (7000), and the single public edge port (8443). Only 8443 is
public.

---

## Section 3 - Datastores and connection limits

Each service has its own datastore. The datastores are:

- Quoter uses a managed Postgres instance (Initech-managed) with a connection pool
  cap of 80 connections per service replica.
- Booker uses a managed Postgres instance with a connection pool cap of 120
  connections per service replica. Booker is the highest-write service and gets the
  largest pool.
- Dispatcher uses a managed Postgres instance with a connection pool cap of 60
  connections per service replica.
- Tracker uses a time-series store (not Postgres) sized for high ingest; it has no
  fixed connection pool cap and instead rate-limits ingest at 50,000 events per
  second per replica.
- Biller uses a managed Postgres instance with a connection pool cap of 40
  connections per service replica. Biller is deliberately given the smallest pool
  because its workload is low-volume but high-value, and a runaway Biller must not
  exhaust the shared Postgres cluster.
- Notifier uses a Redis-backed queue plus a small Postgres instance with a connection
  pool cap of 30 connections per service replica.

The shared managed-Postgres cluster (Initech) has a hard ceiling of 800 total
connections across all services and all replicas. The per-service pool caps above are
sized so that the sum of all replicas' pools at maximum replica count stays under
800. If the cluster approaches 800 connections, new connections are refused and the
on-call must shed replicas (see Section 11).

Object storage for documents (invoices, bills of lading, proof-of-delivery images)
is provided by Globex. Objects are stored in three buckets: northwind-invoices,
northwind-bol, and northwind-pod. The buckets are versioned. Object storage has no
connection pool; it is accessed over HTTPS with signed URLs that expire after 15
minutes.

---

## Section 4 - Release and deployment process

Releases follow a strict promotion pipeline with four stages: build, staging, canary,
and production. A release artifact is immutable once built; the same artifact hash
moves through all four stages. You never rebuild between stages.

1. Build. CI builds the artifact and runs the unit and contract test suites. A build
   that fails any test is not promotable.
2. Staging. The artifact deploys to the staging environment, which runs against a
   sanitized copy of production data. The full integration suite runs here. Staging
   data is retained for 7 days and then purged.
3. Canary. The artifact deploys to a single production canary replica that takes 5
   percent of live traffic. The canary must bake for a minimum of 45 minutes before
   promotion to full production. During the bake, the canary's error rate and latency
   are compared against the stable fleet; if the canary's p99 latency exceeds the
   stable fleet's p99 by more than 20 percent, the canary auto-aborts and rolls back.
   The 45-minute canary bake minimum is current as of revision 9.0. It was previously
   20 minutes in revisions 7.x and 8.x and was raised to 45 minutes in revision 9.0
   after the March incident (see Section 14). Use 45 minutes; 20 minutes is the
   historical value and is no longer valid.
4. Production. After a clean canary bake, the artifact rolls out to the full
   production fleet in waves of 25 percent, with a 10-minute soak between waves.

Promotion from canary to production requires sign-off from two engineers: the release
owner and a second approver who is not the release owner. This is the two-person
promotion rule and it applies to PRODUCTION PROMOTION only.

Rollback is different. A rollback to the previously known-good artifact can be
initiated by a single on-call engineer and deliberately does NOT require a second
approver. The reasoning, recorded when the policy was set in revision 8.2, is that
rollback is a safety action and must never be blocked waiting for a second person
during an incident. Do not conflate the two-person promotion rule with rollback;
rollback is single-approver by design.

Deployments are frozen during two windows each year: 20 December through 2 January
(the holiday freeze) and the 48 hours surrounding any company-wide all-hands. During
a freeze, only Sev1 emergency fixes may be deployed, and an emergency deploy during a
freeze requires sign-off from a Director, not just the two-engineer promotion rule.

---

## Section 5 - Service level objectives

The Platform publishes SLOs to internal stakeholders. The SLOs are measured over a
rolling 28-day window, not a calendar month. The rolling 28-day window is deliberate;
an earlier revision used a calendar-month window and it was changed to rolling 28 days
in revision 6.4 to remove the end-of-month reset artifact.

- Gateway availability SLO: 99.95 percent. This is the headline public-facing
  availability number.
- Booker write availability SLO: 99.9 percent.
- Quoter availability SLO: 99.9 percent.
- Tracker ingest availability SLO: 99.5 percent. Tracker is allowed a looser SLO
  because tracking events are eventually consistent and a brief ingest gap is
  recoverable by re-ingestion.
- Biller availability SLO: 99.9 percent.
- Notifier delivery SLO: 99.0 percent of notifications delivered within their
  delivery window. Notifier has the loosest availability SLO of any service because
  a delayed notification is lower-impact than a failed booking.

Latency SLOs are stated as p99 targets:

- Gateway p99 latency target: 300 milliseconds end to end.
- Booker write p99 latency target: 250 milliseconds.
- Quoter quote-generation p99 latency target: 800 milliseconds (quote generation is
  compute-heavy and is allowed a higher latency budget).

The error budget for each service is one minus its availability SLO, applied over the
rolling 28-day window. When a service exhausts its error budget, an automatic feature
freeze applies to that service: no feature deploys, only reliability fixes, until the
budget recovers. The error budget policy is owned by the Reliability team.

---

## Section 6 - Data retention

Retention windows differ by data class. Read this section carefully; there are
several similar-looking windows and they are NOT interchangeable.

- Booking records (the authoritative booking row in Booker): retained for 7 years for
  regulatory reasons, then archived to cold storage. Booking records are never hard
  deleted before 7 years.
- Application logs (structured logs from all services): retained hot for 30 days in
  the searchable log store, then moved to cold archive for a further 11 months, for a
  total of 12 months before deletion.
- Metrics (the time-series telemetry, distinct from logs): retained at full
  resolution for 15 days, then downsampled and kept at reduced resolution for 13
  months.
- Distributed traces: retained for 7 days only. Traces are high-volume and
  low-durability; 7 days is the full trace retention.
- Notification content (the actual body of an email or SMS that Notifier sent):
  retained for 72 hours and then purged. The 72-hour window is the content body only.
- Notification delivery metadata (the record that a notification was sent, to whom,
  and its delivery status, WITHOUT the body): retained for 90 days. Do not confuse
  the 72-hour content retention with the 90-day metadata retention; the body is gone
  after 72 hours but the "we sent X to Y at time T, status delivered" metadata
  survives for 90 days.
- Staging environment data: retained for 7 days then purged (this is also stated in
  Section 4).
- Audit trail (the security audit log of who accessed or changed what): retained for
  3 years. The audit trail is separate from application logs and has its own store.
- Proof-of-delivery images in object storage: retained for 2 years then deleted.
- Invoices in object storage: retained for 7 years to match the booking-record
  regulatory window.

To restate the easily-confused windows: traces 7 days, staging data 7 days, metrics
15 days full resolution, logs 30 days hot, notification content 72 hours,
notification metadata 90 days, audit trail 3 years, booking records 7 years, invoices
7 years, proof-of-delivery images 2 years.

---

## Section 7 - Authentication and authorization

Customers authenticate to the public Gateway using OAuth2 with the authorization-code
flow. Customer access tokens are JWTs that expire after 60 minutes. Refresh tokens
expire after 30 days of inactivity; any use of a refresh token resets its 30-day
inactivity clock. A customer session is therefore effectively indefinite as long as
the customer returns at least once every 30 days.

Internal service-to-service authentication uses mutual TLS (mTLS) with short-lived
certificates issued by the internal certificate authority. Service certificates are
valid for 24 hours and are rotated automatically by the certificate agent twelve
hours before expiry, so a certificate is never used in its last twelve hours of
validity. The internal CA root certificate itself is valid for 10 years and is rotated
manually by the Reliability team.

Internal human access to production (for on-call engineers) is granted through a
just-in-time access broker. A grant is requested, approved by a second engineer, and
is valid for a maximum of 8 hours, after which it expires and must be re-requested.
Just-in-time grants to the production database specifically are capped tighter, at 2
hours, and every database grant is recorded in the audit trail.

Authorization within the Platform uses role-based access control with four roles:
viewer (read-only), operator (can act on bookings), admin (can change configuration),
and auditor (read-only access to the audit trail, with no access to booking content).
The auditor role is deliberately scoped to the audit trail only; an auditor cannot
read customer booking data, by design, to separate the people who watch the watchers
from the booking data itself.

---

## Section 8 - Event bus and messaging

Cross-service communication that is not a synchronous API call goes over the event
bus. The event bus is an append-only log with topic partitioning. Each service
publishes domain events to its own topic and subscribes to the topics it cares about.

- booking.confirmed is published by Booker when a booking reaches CONFIRMED. It is
  consumed by Dispatcher (to plan a route), Biller (to raise an invoice), and Notifier
  (to send a confirmation).
- dispatch.assigned is published by Dispatcher and consumed by Tracker and Notifier.
- tracking.updated is published by Tracker and consumed by Notifier (to send transit
  updates) and Booker (to advance booking state to IN_TRANSIT or DELIVERED).
- payment.captured is published by Biller and consumed by Booker and Notifier.

Events are retained on the bus for 14 days. A consumer that falls behind can replay
from any point within the last 14 days. After 14 days, events fall off the log and
cannot be replayed; a consumer that is more than 14 days behind must be rebuilt from a
snapshot rather than by replay. The 14-day bus retention happens to equal the 14-day
quote validity window from Section 1, but the two are unrelated; do not assume one
implies the other.

Event delivery is at-least-once, not exactly-once. Every consumer must be idempotent.
Idempotency is enforced by an idempotency key on every event equal to the event's
globally unique event id; a consumer that has already processed a given event id must
treat a redelivery as a no-op. The Platform does not provide exactly-once delivery,
and any design that assumes exactly-once is incorrect.

Maximum event payload size is 256 kilobytes. An event larger than 256 kilobytes is
rejected at publish time; large payloads (for example a batch of tracking points) must
be split or must carry a reference to object storage rather than the payload inline.

---

## Section 9 - Capacity and scaling

Each service runs as a horizontally scaled set of replicas behind an internal load
balancer. Autoscaling is driven by CPU utilization with a target of 60 percent
average CPU; when average CPU across a service's replicas exceeds 60 percent, the
autoscaler adds replicas, and when it falls below 40 percent for a sustained 15
minutes, it removes replicas. The scale-up trigger (60 percent) and the scale-down
trigger (40 percent, sustained 15 minutes) are deliberately asymmetric to avoid
flapping.

Replica counts have hard minimums and maximums per service:

- Quoter: minimum 4 replicas, maximum 40 replicas.
- Booker: minimum 6 replicas, maximum 60 replicas. Booker has the highest maximum
  because it is the highest-write service.
- Dispatcher: minimum 3 replicas, maximum 30 replicas.
- Tracker: minimum 4 replicas, maximum 50 replicas.
- Biller: minimum 2 replicas, maximum 20 replicas.
- Notifier: minimum 2 replicas, maximum 24 replicas.
- Gateway: minimum 6 replicas, maximum 48 replicas.

The connection-pool math from Section 3 binds these maxima: Booker at 60 replicas with
a 120-connection pool would request 7,200 connections, which far exceeds the 800
cluster ceiling, so in practice Booker's pool cap and the cluster ceiling mean Booker
cannot run all 60 replicas at full pool simultaneously. The Reliability team treats the
800 connection ceiling, not the replica maximum, as the true Booker scaling limit, and
this tension is a known and intentionally-documented constraint awaiting the planned
read-replica split (see Section 18).

Peak-season pre-scaling: before peak season (15 November), the Reliability team
manually raises the minimum replica counts to 150 percent of the steady-state minimums
for the duration of peak season, then returns them to the steady-state minimums after
10 January. Pre-scaling is a manual runbook step, not an automatic behavior.

---

## Section 10 - Observability

The Platform is observed through three pillars: metrics, logs, and traces.

Metrics are scraped from each service's port 9100 every 15 seconds by the metrics
collector and stored in the time-series store. Dashboards are built per service and
there is a single platform-wide "golden signals" dashboard showing latency, traffic,
errors, and saturation for all seven services on one page.

Logs are structured JSON. Every log line carries a trace id, a service name, a
severity, and a timestamp in UTC. Logs are shipped to the searchable log store within
roughly 30 seconds of being emitted; do not confuse this 30-second shipping latency
with the 30-day log retention window from Section 6.

Traces are sampled. The Platform samples 100 percent of error traces and 1 percent of
successful traces. The 1-percent success sampling is a cost control; the 100-percent
error sampling guarantees every error has a trace for the 7 days that traces are
retained. A sampled-out successful request has metrics and logs but no trace.

Alerting is tiered into three severities. Sev1 is a customer-facing outage or data
loss and pages the on-call immediately, 24/7. Sev2 is a significant degradation that
pages during business hours and otherwise raises a ticket. Sev3 is a minor or
non-urgent issue that only raises a ticket and never pages. The paging policy is owned
by the on-call rotation, described in Section 12.

---

## Section 11 - Incident response runbook

When a Sev1 fires, the on-call engineer is the incident commander until they
explicitly hand off. The first three actions, in order, are: (1) acknowledge the page
within 5 minutes, (2) open an incident channel and post the initial assessment, and
(3) decide whether to roll back the most recent deploy. Rollback is the default first
mitigation if a deploy went out in the last 60 minutes; a single on-call engineer can
execute the rollback without a second approver (per Section 4).

If the incident is a Postgres connection exhaustion (the cluster approaching its 800
connection ceiling), the runbook is: first, identify the runaway service from the
per-service connection dashboard; second, shed replicas of that service down toward
its minimum to free connections; third, if shedding does not recover the cluster
within 10 minutes, fail the runaway service's reads over to the eu-west analytics
replica for read-only queries while the write path recovers. Never raise the 800
ceiling during an incident; the ceiling is a protective limit, and raising it risks
cascading the failure to the managed-Postgres control plane.

If the incident is a regional outage of us-central, execute the regional failover
runbook in Section 13. Do not attempt a regional failover for a single-service
outage; failover is a region-level action and is heavier than shedding or rolling back
one service.

Every Sev1 gets a written postmortem within 5 business days. Postmortems are blameless
and are reviewed in the weekly reliability review. The postmortem must identify the
trigger, the contributing factors, the detection gap if any, and concrete action items
with owners and due dates.

---

## Section 12 - On-call rotation

The on-call rotation is a weekly primary-and-secondary model. The primary on-call
holds the pager for one week, Monday 10:00 to the following Monday 10:00 UTC. The
secondary on-call is the backup and is paged only if the primary does not acknowledge
within the 5-minute Sev1 acknowledgment window. There is a separate escalation
manager who is paged if neither primary nor secondary acknowledges within 15 minutes.

On-call engineers are compensated with an on-call stipend and time-off-in-lieu for any
out-of-hours page that requires more than 30 minutes of active work. The stipend
amount and the time-off-in-lieu accrual rate are set by People Operations and are not
specified in this manual; this manual covers the operational rotation only, not the
compensation figures.

A single engineer may not be primary on-call for more than two consecutive weeks, to
avoid burnout. The rotation is built one quarter ahead and published in the shared
calendar. Swaps are allowed up to 48 hours before a shift with mutual agreement and a
note in the rotation channel.

---

## Section 13 - Regional failover

The Platform can fail over from the primary us-central region to the secondary
us-east region. us-east is a warm standby: it runs the full service set at reduced
replica counts and its datastores are kept in sync with us-central by continuous
streaming replication.

The replication lag from us-central to us-east is normally under 5 seconds. The
failover decision threshold is a sustained replication lag over 60 seconds OR a
confirmed loss of the us-central region. A failover is a Director-approved action, not
an on-call-discretion action, because promoting us-east to primary makes us-east the
write region and any un-replicated writes in the lag window are lost.

The failover sequence is: (1) stop accepting writes in us-central, (2) wait for
us-east to drain the replication backlog to zero or declare the unrecoverable backlog
lost, (3) promote us-east datastores to primary, (4) repoint the Gateway's write path
to us-east, (5) scale us-east replica counts up from standby levels to full production
levels. The target recovery time objective for a regional failover is 30 minutes and
the target recovery point objective is 60 seconds of potential write loss in the worst
case. These regional-failover RTO and RPO targets are stated here and are owned by the
Reliability team.

Failback to us-central, after the region recovers, is a separate planned operation
performed during a low-traffic window and is never done under incident pressure. The
failback procedure is the reverse of failover and additionally requires a full data
reconciliation between the regions before us-central resumes as primary.

eu-west is never a failover target. eu-west is read-only analytics and cannot be
promoted to a write region under any circumstances.

---

## Section 14 - Notable past incidents

The March incident: a bad deploy passed a 20-minute canary bake (the bake minimum at
the time) because the regression only manifested under a load pattern that took longer
than 20 minutes to build up. The deploy went to full production and caused a 40-minute
Booker write outage before it was rolled back. The action item was to raise the canary
bake minimum, which was raised from 20 minutes to 45 minutes in revision 9.0. This is
why the current canary bake minimum is 45 minutes and 20 minutes is the historical
value.

The July incident: a runaway Biller query opened connections without releasing them
and drove the shared Postgres cluster to its 800 connection ceiling, refusing new
connections platform-wide. The incident was mitigated by shedding Biller replicas and
failing Biller reads to the eu-west replica. The action item was the per-service
connection pool caps in Section 3 and the connection-exhaustion runbook in Section 11.
Before July, there were no per-service pool caps; the caps were introduced as a direct
result.

The September near-miss: replication lag to us-east climbed to 48 seconds during a
network event but did not cross the 60-second failover threshold, so no failover was
triggered and the lag recovered on its own. The near-miss prompted a review of the
60-second threshold, which was reaffirmed as correct; the threshold was not changed.

These incidents are recorded here for context. The current authoritative values
(45-minute canary bake, 800 connection ceiling, 60-second failover threshold) are the
ones in their respective sections above, not the historical values that appear in this
incident narrative.

---

## Section 15 - Support and customer communication

Customer support operates a tiered model. Tier 1 handles general inquiries and
password resets. Tier 2 handles booking disputes and tracking escalations. Tier 3 is
the engineering escalation path and is reached only through an on-call engineer; Tier 3
is not a standing support team but the on-call rotation acting in a support capacity.

Customer-facing communications about an ongoing incident are posted to the public
status page. The status page is updated by the incident commander or a delegate within
30 minutes of a Sev1 being declared, and then at least every 60 minutes until
resolution. The status-page update cadence (initial within 30 minutes, then every 60
minutes) is a customer-trust commitment and is tracked as part of the incident
postmortem.

Refund authority: Tier 2 support can authorize a refund up to 500 dollars without
escalation. A refund above 500 dollars requires a support lead's approval, and a
refund above 5,000 dollars requires a Director's approval. These refund thresholds are
operational policy and apply per booking.

The Platform sends customers four kinds of notification: a booking confirmation, a
dispatch notice, transit updates, and a delivery confirmation. Customers can opt out of
transit updates but cannot opt out of the booking confirmation or the delivery
confirmation, which are considered transactional and mandatory.

---

## Section 16 - Configuration management

All Platform configuration is stored in a version-controlled configuration repository,
separate from the application code repositories. Configuration changes go through the
same review process as code: a pull request, at least one approving review, and an
automated validation check. A configuration change is never applied directly to a
running service; it is committed, reviewed, merged, and then rolled out by the
configuration agent.

Configuration is layered: a platform-wide default layer, a per-region override layer,
and a per-service override layer, applied in that order with the most specific layer
winning. A per-service override in us-central beats a per-region us-central value,
which beats the platform-wide default. There is intentionally no per-replica
configuration; all replicas of a service in a region run identical configuration.

Secrets are NOT stored in the configuration repository. Secrets live in the secrets
manager and are injected into services at runtime. The configuration repository may
reference a secret by name but never contains the secret value. A pull request that
attempts to commit a literal secret value is blocked by the automated validation
check.

Feature flags are a special class of configuration. A feature flag can be toggled
faster than a normal configuration change: a flag flip is reviewed by one engineer and
applied within minutes, because flags are designed to be the fast lever during an
incident (for example, disabling an expensive feature to shed load). Flag flips are
still recorded in the audit trail.

---

## Section 17 - Backup and restore

Datastore backups are taken on a tiered schedule. Postgres datastores get a full
backup nightly and continuous write-ahead-log archiving that enables point-in-time
recovery to any second within the backup retention window. The Postgres backup
retention window is 35 days; you can restore any Postgres datastore to any point in
the last 35 days. Backups older than 35 days are deleted.

Object storage (Globex) is versioned, so object backup is implicit: a deleted or
overwritten object can be restored from a prior version for as long as the bucket
retention (Section 6) holds that version. The time-series store (Tracker and metrics)
is backed up daily with a 35-day retention matching Postgres, but point-in-time
recovery is not available for the time-series store; only daily snapshots can be
restored.

Restore drills are run quarterly. Each quarter the Reliability team restores a random
Postgres datastore from backup into an isolated environment and verifies integrity.
The restore drill is a scheduled, non-production exercise; it is never run against a
live production datastore. The most recent four restore drills all passed.

A full-cluster restore (rebuilding all datastores from backup) has a documented target
of 4 hours and has been exercised once, in a planned game-day, where it completed in 3
hours 40 minutes. This full-cluster restore target is distinct from the regional
failover RTO in Section 13; failover promotes a warm standby in 30 minutes, whereas a
cold full-cluster restore from backup targets 4 hours.

---

## Section 18 - Known limitations and planned work

This section records known constraints that are accepted for now and the planned work
to address them. These are documented limitations, not bugs.

- Booker connection ceiling. As noted in Sections 3 and 9, Booker cannot run its full
  60 replicas at full connection pool because of the 800 cluster connection ceiling.
  The planned fix is a read-replica split that moves Booker's read traffic to a
  dedicated read replica, freeing write-pool connections. This work is planned but the
  delivery date for the read-replica split is not stated in this manual; the date is
  tracked in the Reliability team's roadmap, not here.
- Exactly-once delivery. The event bus is at-least-once only (Section 8). True
  exactly-once delivery is not planned; the accepted approach is consumer idempotency,
  and there is no roadmap item to add exactly-once.
- eu-west write capability. eu-west is read-only by design (Sections 2 and 13). There
  is no plan to make eu-west a write region; a third write region, if ever needed,
  would be a new region, not eu-west.
- Notification content retention. The 72-hour notification-content retention
  (Section 6) is sometimes too short for support investigations that arrive late. A
  proposal to extend it to 7 days exists but has not been approved; until approved, the
  retention remains 72 hours.

When in doubt about whether a behavior is a bug or a known limitation, check this
section first. If it is listed here, it is known and accepted, and the relevant fix (if
any) is described.

---

## Section 19 - Rate limits and quotas

The public Gateway enforces per-customer rate limits. The default rate limit is 600
requests per minute per customer API key. A customer can request a raised limit; the
maximum grantable limit is 6,000 requests per minute, above which the customer must
move to the bulk-ingest API. Note that the 600-per-minute default and the
50,000-events-per-second Tracker ingest cap (Section 3) govern different things: the
600 figure is per-customer API requests at the public edge, the 50,000 figure is
internal carrier event ingest. Do not conflate them.

Burst handling: the rate limiter is a token bucket that allows a burst of up to twice
the steady rate for up to 10 seconds before throttling to the steady rate. A customer
that exceeds their limit receives an HTTP 429 with a Retry-After header. Persistent
abuse (more than 5 consecutive 429-triggering minutes) trips an automatic temporary
block of 15 minutes.

The bulk-ingest API is a separate endpoint for high-volume customers (large freight
brokers) and is not rate-limited per request; instead it is quota-limited at 2 million
bookings per day per customer. The bulk-ingest quota resets at 00:00 UTC daily. A
customer hitting the 2-million daily bulk quota must wait for the daily reset; the
quota is not raisable without a commercial agreement and is not an engineering setting.

Internal service-to-service calls are not rate-limited at the application layer; they
are governed by the connection-pool caps (Section 3) and the circuit breakers
(Section 21) instead.

---

## Section 20 - Circuit breakers and timeouts

Every synchronous service-to-service call is wrapped in a circuit breaker. A circuit
breaker has three states: closed (calls pass through), open (calls fail fast without
attempting the downstream), and half-open (a trickle of probe calls test whether the
downstream has recovered).

The circuit opens when the error rate to a downstream exceeds 50 percent over a rolling
window of the last 20 calls. Once open, the breaker stays open for a cooldown of 30
seconds, then transitions to half-open and allows up to 5 probe calls; if those probes
succeed, the breaker closes, and if any probe fails, the breaker re-opens for another
30-second cooldown. The 50-percent-over-20-calls trip threshold and the 30-second
cooldown are platform-wide defaults; an individual call site may override the cooldown
but not the trip threshold.

Synchronous call timeouts are layered and must be strictly decreasing as you go
downstream, so an upstream never times out before its downstream:

- The Gateway's timeout for a call to any backend service is 5 seconds.
- A backend service's timeout for a call to another backend service is 3 seconds.
- A backend service's timeout for a Postgres query is 2 seconds.
- A backend service's timeout for an object-storage operation is 4 seconds. This is
  the one exception to the strictly-decreasing rule, justified because object-storage
  operations (fetching a proof-of-delivery image) are inherently slower and are never
  on the synchronous booking-write path; they happen on read or background paths where
  the 4-second budget does not violate any upstream's 5-second Gateway budget.

A query that exceeds the 2-second Postgres timeout is cancelled server-side to avoid
holding a connection from the pool; this protects the 800-connection ceiling (Section
3) from being consumed by slow queries.

---

## Section 21 - Cost allocation and budgets

Platform infrastructure cost is allocated back to the owning teams monthly. Each
service's cost is the sum of its compute (replica-hours), its datastore, its share of
the event bus, and its share of object storage and egress. The Reliability team's
cross-cutting cost (the metrics store, the trace store, the standby region) is
allocated proportionally across all seven services by traffic share.

The single largest line item platform-wide is the standby us-east region, which costs
roughly the same as the primary us-central region's compute even though it serves no
write traffic, because the warm standby runs the full service set. This cost is
accepted as the price of a 30-minute failover RTO; a cold standby would be cheaper but
would push the regional RTO from 30 minutes to several hours, which the business has
decided is unacceptable.

Egress is the second-largest variable cost. Proof-of-delivery image downloads dominate
egress; this is why object storage uses signed URLs that expire after 15 minutes
(Section 3), to prevent hotlinking and uncontrolled egress.

A team that exceeds its monthly infrastructure budget by more than 20 percent triggers
a cost review with the Reliability team and Finance. The cost review is a process, not
an automatic throttle; the Platform never automatically degrades service to stay under
budget, because availability SLOs (Section 5) take precedence over cost.

---

## Section 22 - Data privacy and residency

Customer personal data (names, contact details, delivery addresses) is classified as
PII and is subject to residency rules. PII for customers in a given jurisdiction is
stored in the region serving that jurisdiction; the Platform does not move PII across
residency boundaries. Because eu-west is read-only analytics, the analytics warehouse
in eu-west holds only de-identified or aggregated data, never raw PII; raw PII never
leaves its residency region.

A customer may request deletion of their personal data (a right-to-be-forgotten
request). On an approved deletion request, PII is removed within 30 days, EXCEPT for
data the Platform is legally required to retain: the booking records retained for 7
years (Section 6) and the audit trail retained for 3 years are exempt from deletion
because they are regulatory retention obligations. The deletion removes contact and
identity fields but preserves the regulatory booking record in a redacted form. Do not
confuse the 30-day deletion SLA with any of the retention windows; the deletion SLA is
the maximum time to honor a deletion request, not a retention period.

Data-subject access requests (a customer asking for a copy of their data) are honored
within 30 days as well, and are fulfilled by an export job that gathers the customer's
data across all services into a single package. The access-request export does not
include the audit trail (which is internal security data) or other customers' data.

---

## Section 23 - Third-party dependencies

The Platform depends on four external vendors, each with a documented failure mode and
fallback:

- Globex (object storage). If Globex is unavailable, document writes (invoices,
  proof-of-delivery) are queued locally and flushed when Globex recovers; the booking
  write path does not block on Globex. Globex unavailability is a Sev2, not a Sev1,
  because it does not stop bookings.
- Initech (managed Postgres). Initech is a hard dependency; if the managed-Postgres
  control plane is down, the Platform cannot write bookings. Initech unavailability is
  a Sev1. There is no fallback datastore; this single-vendor dependency is a documented
  risk (it is also noted in Section 18-class concerns, though the manual does not list a
  planned multi-vendor Postgres migration).
- Umbra (CDN). Umbra fronts the public Gateway for static assets and TLS termination at
  the edge. If Umbra is degraded, the Gateway can serve directly from origin at higher
  latency; Umbra degradation is a Sev2.
- Acme (SMS gateway). If Acme is unavailable, SMS notifications queue in Notifier and
  are sent when Acme recovers, OR fall back to email if the customer has an email on
  file. Acme unavailability is a Sev3 because notifications are the lowest-impact
  service (Section 5) and have an email fallback.

Vendor status is monitored and a vendor outage is correlated against Platform alerts so
the on-call can distinguish a Platform fault from a vendor fault quickly. The vendor
contracts and SLAs with these vendors are managed by Procurement and the specific
contractual vendor SLA percentages are not stated in this manual.

---

## Section 24 - Testing strategy

The Platform maintains four test tiers. Unit tests run on every build and must pass for
an artifact to be promotable (Section 4). Contract tests verify that each service
honors the published API and event contracts its consumers depend on; a contract test
failure blocks promotion because it predicts a downstream break. Integration tests run
in staging against the sanitized data copy. End-to-end tests exercise a full
quote-to-delivery flow in staging on a schedule, not on every build, because they are
slow.

Test data is synthetic and never contains real customer PII; the sanitized staging copy
has PII fields replaced with synthetic values. The synthetic-data generator is itself
tested to ensure it never accidentally emits a real-looking identifier that collides
with production.

Load tests are run before each peak season against the pre-scaled replica counts
(Section 9) to confirm the Platform can sustain peak booking volume. The most recent
peak-season load test validated sustained throughput at 240,000 bookings per day with
headroom; the load test target is set 20 percent above the prior peak's observed volume.

Chaos testing (deliberately injecting failures) is run quarterly in staging only, never
in production. The chaos exercises include killing replicas, injecting latency, and
simulating a vendor outage, to verify the circuit breakers (Section 20) and runbooks
(Section 11) behave as documented.

---

## Section 25 - Logging standards and PII redaction

Every log line is structured JSON with mandatory fields: timestamp (UTC, ISO 8601),
service name, severity, trace id, and message. Optional fields include the booking id
and the customer id (an opaque identifier, never the customer's name or contact
details). Logs must NEVER contain raw PII; a log line that would contain PII must
redact it. The logging library auto-redacts known PII field names, and a log line that
trips the PII detector in the log pipeline is quarantined and flagged for review rather
than indexed.

Severity levels are DEBUG, INFO, WARN, ERROR, and FATAL. DEBUG logs are emitted only
when a service is in debug mode, which is never the default in production; production
runs at INFO and above. An ERROR log automatically attaches the full trace (because
error traces are 100-percent sampled, Section 10). A FATAL log indicates the service is
about to crash and triggers an immediate alert.

Log volume is itself monitored; a sudden spike in ERROR-level logs is an early signal
of an incident and feeds an anomaly detector that can page before an SLO is breached.
The anomaly detector is advisory and does not itself declare a Sev; a human confirms.

Logs are retained hot for 30 days then cold for 11 more months (Section 6); this is
distinct from the 30-second log-shipping latency (Section 10) and from the 35-day
Postgres backup retention (Section 17). Three different "30-something" windows exist
across logs, shipping, and backups and they are not interchangeable.

---

## Section 26 - Quote lifecycle details

A quote is generated by Quoter from a freight request (origin, destination, weight,
dimensions, service level) and a current rate card. The quote is valid for 14 days
(Section 1). A quote carries a frozen snapshot of the rate card used, so the quoted
price does not change even if the rate card changes during the 14-day validity; the
customer is honored at the quoted price if they book within 14 days.

Rate cards are updated by the Commerce team and a rate-card change is a configuration
change (Section 16), reviewed and rolled out, not a code deploy. A rate-card change
applies to NEW quotes generated after the change; it never retroactively alters an
already-issued quote within its 14-day validity.

There are three service levels: Standard, Express, and Priority. Express quotes are
priced higher and carry a tighter delivery commitment; Priority is the highest tier
with the tightest commitment and the highest price. The delivery commitments per
service level are commercial terms set by Commerce and the specific committed transit
days per service level are not stated in this manual.

A quote can be regenerated after it expires, but the regenerated quote uses the
then-current rate card, which may differ from the expired quote's frozen card. There is
no grace period beyond the 14 days; on day 15 the quote is expired and the only path is
regeneration.

---

## Section 27 - Booking state machine details

A booking moves through DRAFT, CONFIRMED, IN_TRANSIT, DELIVERED, and CANCELLED. The
legal transitions are: DRAFT to CONFIRMED (on payment authorization), DRAFT to
CANCELLED, CONFIRMED to IN_TRANSIT (on first carrier scan), CONFIRMED to CANCELLED,
IN_TRANSIT to DELIVERED (on proof of delivery), and IN_TRANSIT to CANCELLED (a
mid-transit cancellation, which is rare and triggers a return flow). DELIVERED is a
terminal state; a DELIVERED booking cannot transition further. CANCELLED is also
terminal.

A cancellation from CONFIRMED or IN_TRANSIT triggers a refund evaluation in Biller; the
refund amount depends on how far the booking progressed and is governed by the
commercial cancellation policy, not by this manual. A cancellation from DRAFT (before
payment authorization) involves no refund because no payment was captured.

Only Booker writes booking state (Section 1). State transitions are driven by events:
payment.captured advances DRAFT to CONFIRMED, the first tracking.updated advances
CONFIRMED to IN_TRANSIT, and the delivery tracking.updated advances IN_TRANSIT to
DELIVERED. Because event delivery is at-least-once (Section 8), Booker's transition
handler is idempotent: re-receiving the delivery event for an already-DELIVERED booking
is a no-op, not an error.

A booking stuck in CONFIRMED with no carrier scan for more than 48 hours raises a Sev3
ticket for the Fulfillment team to investigate a possible dispatch failure. This
48-hour stuck-booking threshold is an operational alert, distinct from the 14-day quote
validity and the 14-day event-bus retention.

---

## Section 28 - Maintenance windows

Planned maintenance that requires brief service disruption is performed in a weekly
maintenance window: Sunday 02:00 to 04:00 UTC, the lowest-traffic period of the week.
Most maintenance is zero-downtime (rolling deploys, Section 4) and does not need the
window; the window is reserved for the rare change that cannot be done without
disruption, such as a major datastore version upgrade.

Maintenance in the window is still announced on the status page 72 hours in advance,
and any maintenance expected to cause customer-visible disruption is announced 7 days
in advance. Note the two notice periods: 72 hours for routine windowed maintenance,
7 days for disruptive maintenance. These notice periods are customer-communication
commitments and are separate from the 72-hour notification-content retention (Section
6) and the 7-day staging-data retention (Section 4), which they happen to numerically
resemble but have nothing to do with.

Maintenance is never performed during the holiday freeze (Section 4) or during peak
season except for emergency fixes. A maintenance window can be cancelled if an active
incident is in progress; reliability work during an incident takes precedence over
planned maintenance.

---

## Section 29 - Access reviews and offboarding

Production access is reviewed quarterly. Every standing access grant (not the
time-boxed just-in-time grants, which expire on their own, but any longer-lived role
assignment) is re-certified by the grantee's manager each quarter; an access grant that
is not re-certified is automatically revoked. The quarterly access review is logged in
the audit trail (Section 6, 3-year retention).

When an engineer leaves the company, their access is revoked within 1 hour of the
offboarding being initiated by People Operations. This 1-hour offboarding revocation is
deliberately fast and is tighter than the quarterly review cadence; it does not wait for
the next quarterly review. All of the departing engineer's just-in-time grants are also
immediately invalidated.

Shared or service credentials are never tied to an individual; a service authenticates
with mTLS (Section 7), not with a human's credentials, precisely so that offboarding a
human never breaks a service. There are no shared human logins to production; every
human action is attributable to a named individual in the audit trail.

---

## Section 30 - Glossary

- Bake. The canary observation period before promotion to full production. The current
  minimum bake is 45 minutes (Section 4).
- Bounded context. A service's owned domain and datastore; no other service writes it
  (Section 1).
- Error budget. One minus the availability SLO over the rolling 28-day window; its
  exhaustion triggers a feature freeze for that service (Section 5).
- Failover. Promoting the us-east warm standby to primary during a us-central regional
  outage (Section 13).
- Idempotency key. The event id used to deduplicate at-least-once event delivery
  (Section 8).
- Just-in-time access. Time-boxed production access granted on request and approved by
  a second engineer; 8 hours general, 2 hours for the database (Section 7).
- Two-person promotion rule. The requirement that canary-to-production promotion be
  signed off by the release owner plus a second approver; does not apply to rollback
  (Section 4).

---

## Section 31 - Document control

This manual is owned by the Reliability team and reviewed every quarter. The current
revision is 11.3. Proposed changes are submitted as pull requests against the
documentation repository and require approval from a Reliability team lead. The
revision history is maintained in the documentation repository, not in this manual
body; this manual states only the current authoritative values, with historical values
called out explicitly where a current value replaced an older one (the canary bake, the
SLO window, the connection-pool caps).

If a number in this manual conflicts with a number you find elsewhere, this manual
wins, unless this manual explicitly defers the number to another owner (the on-call
compensation figures to People Operations, the read-replica split delivery date to the
Reliability roadmap, the disaster-recovery figures owned by Reliability are stated here
in Section 13). When this manual says a value is "not stated" or defers it, treat that
absence as authoritative: the manual is intentionally silent, not incomplete.
