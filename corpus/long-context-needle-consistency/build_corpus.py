#!/usr/bin/env python3
"""
Generator for the long-context-needle-consistency corpus.

Builds a single large operations + policy manual for a fictional logistics
company "Cardinal Freight Systems" of roughly 48000 words / 60000+ tokens, then
salts it with near-duplicate distractor values so that the one true needle for
each question sits among many look-alikes spread across distant sections.

The buried needle (the run-to-run separator) is the Tier-3 cold-archive
restore SLA in Section 41: 26 hours. It is surrounded by a dense cluster of
other "hour" recovery windows (4 hours, 8 hours, 12 hours, 24 hours, 36 hours,
2 hours, 6 hours) attached to different recovery operations, AND a single
sentence later in Section 58 silently restates a SUPERSEDED historical value of
18 hours that a skimming model latches onto. Only the model that reads to
Section 41 carefully and resolves the cluster reports 26 hours every run.

This file is the deterministic builder; the manual it writes is the corpus.
Run once: python3 build_corpus.py
No em dashes. No emojis. Neutral fictional names only.
"""

import textwrap

OUT = "cardinal-operations-manual.md"

# A bank of neutral filler paragraphs reused with section-specific framing so the
# document reaches the required length without the needle being trivially close to
# the question's keyword. Filler is deliberately on-topic prose, not lorem ipsum,
# so a model cannot trivially skip it.
FILLER_SENTENCES = [
    "Operators are expected to follow the documented runbook for the action they are performing rather than relying on memory, because the runbooks are the single source of truth and are reviewed every quarter.",
    "Any deviation from a documented procedure must be recorded in the operations journal with the operator name, the timestamp, and a one line justification so the deviation can be reviewed at the next operations retrospective.",
    "When two procedures appear to conflict, the more specific procedure governs the more general one, and the operator escalates to the duty manager if the conflict cannot be resolved from the documentation alone.",
    "The platform is built from independently deployable services that communicate over an internal mesh, and each service owns its own data store so that a fault in one service does not cascade into another.",
    "Capacity planning is performed monthly against the trailing ninety day demand curve, with a documented headroom target that the capacity team revisits whenever a large customer is onboarded.",
    "Every change that touches a customer facing surface goes through a staged rollout, beginning with an internal cohort, then a small external canary, then a progressive widening of the blast radius.",
    "The observability stack collects metrics, structured logs, and distributed traces, and the on call engineer is expected to begin every investigation from the service dashboard rather than from raw logs.",
    "Access to production systems is granted on a least privilege basis, and standing access is avoided in favour of short lived grants that expire automatically and must be re requested.",
    "The security team performs a documented review of every new external integration before it is enabled, and the review covers data flow, retention, and the blast radius of a credential compromise.",
    "Customer notifications are templated and version controlled so that the wording of an outage notice is consistent regardless of which engineer triggers it during an incident.",
    "The data platform separates hot operational stores from warm analytical stores and from cold archival stores, and each tier has its own retention policy and its own restore procedure.",
    "Backups are taken on a layered schedule, with frequent incremental snapshots feeding into less frequent full snapshots, and the restore procedure differs depending on which layer the restore is sourced from.",
    "Routine maintenance is scheduled inside the published maintenance window, and any maintenance that risks customer impact is announced ahead of time with the required notice period for that class of maintenance.",
    "The release train runs on a fixed cadence, and a release that misses the train waits for the next departure rather than forcing an out of band deployment, except where a documented exception applies.",
    "Incident severity is assigned from a documented matrix that weighs customer impact, data risk, and the breadth of the affected surface, and the assigned severity drives the notification and escalation path.",
    "The escalation chain is published and kept current, and the first responder is expected to escalate within the documented window rather than attempting to resolve a high severity incident alone.",
    "Rate limits protect shared infrastructure from a single noisy client, and the limits are tiered so that a higher commitment customer receives a higher allowance under a documented contract term.",
    "The platform enforces tenant isolation at the data layer, and a request that attempts to read across a tenant boundary is rejected and logged as a security relevant event for later review.",
    "Feature flags decouple deployment from release, and a flag that has been fully rolled out for a documented soak period is retired so that the flag set does not accumulate stale entries.",
    "The on call rotation is staffed so that there is always a primary and a secondary, and the secondary is engaged automatically if the primary does not acknowledge a page inside the acknowledgement window.",
    "The configuration service applies every change atomically, so a partially applied configuration is never observable by a running service, and a failed apply rolls back cleanly to the prior known good state.",
    "Each team publishes its service level objectives alongside the error budget it is spending, and a team that is over budget pauses feature work to invest in reliability until the budget recovers.",
    "The platform prefers idempotent operations everywhere, so that a retried request produces the same result as a single request and a client can safely retry on an ambiguous failure.",
    "Schema changes are applied in a backward compatible expand and contract sequence, so that the old and new code can run side by side during a rollout without a coordinated cut over.",
    "The identity service issues short lived credentials and the platform avoids long lived shared secrets, because a short lived credential limits the blast radius of any single leak to the credential's brief validity window.",
    "Every externally triggered webhook delivery is signed, and a receiver that cannot verify the signature rejects the delivery, so that a forged callback cannot drive a state change inside the platform.",
    "The deployment pipeline gates each stage on the health signals from the previous stage, so a regression that surfaces in the canary cohort halts the rollout before it reaches the wider population.",
    "Operational dashboards are kept deliberately sparse and focused on the signals that drive a decision, because a dashboard cluttered with low value panels slows the responder during an incident.",
    "The platform treats configuration as code and reviews it with the same rigour as application code, since a misapplied configuration value has historically caused as many incidents as a code defect.",
    "Cost is treated as an operational signal alongside latency and error rate, so a change that quietly multiplies the cost of a hot path is caught in review rather than discovered on the monthly bill.",
    "The on call engineer is empowered to make a reversible decision quickly and to escalate an irreversible one, because the cost of waiting on an approval for a reversible action usually exceeds the cost of the action.",
    "Tenant data is partitioned so that a single tenant's load cannot starve another tenant, and a tenant that exceeds its fair share is throttled rather than allowed to degrade the shared surface.",
    "The retrospective after each incident produces a small number of high leverage corrective actions with named owners and due dates, rather than a long list of low value items that are never completed.",
    "The platform documents the expected steady state for every service, so that a responder can recognise an anomaly by comparing the live signal against the documented baseline rather than against intuition.",
    "A change that cannot be rolled back is treated as high risk and requires an explicit recovery plan in the change record, because the absence of a rollback path removes the cheapest recovery option.",
    "The secondary region is kept warm rather than cold so that a regional failover can meet its target without first provisioning capacity, and the warm capacity is exercised regularly so it does not rot.",
    "Internal tooling is held to the same reliability bar as customer facing surfaces, because a tooling outage during an incident removes the responder's ability to act at exactly the moment it is needed most.",
    "The platform favours boring and well understood technology for the critical path, reserving novel components for the edges where a failure is contained and does not threaten the core surfaces.",
]


def filler(n, seed_offset=0):
    """Return n filler sentences cycled from the bank, offset so different sections
    do not all start with the same sentence."""
    out = []
    for i in range(n):
        out.append(FILLER_SENTENCES[(i + seed_offset) % len(FILLER_SENTENCES)])
    return " ".join(out)


# Each section is (number, title, body). Bodies embed the salted facts. The
# distractor clusters are spread deliberately across distant sections.
SECTIONS = []


def add(num, title, body):
    SECTIONS.append((num, title, body))


# ---- Sections 1 to 10: platform overview, ports, identifiers ----
add(1, "Document Scope and Conventions",
    "This manual is the operational reference for Cardinal Freight Systems. It "
    "describes the platform, the policies, and the runbooks that govern day to day "
    "operation. Where a value appears in more than one section, the value stated in "
    "the section that owns the topic governs, and any other mention is a cross "
    "reference for convenience only. " + filler(14, 0))

add(2, "Platform Topology and Public Surface",
    "The platform exposes exactly one public ingress port. The edge gateway "
    "terminates transport security on port 8443 and that is the only port reachable "
    "from the public internet. Internal services listen on the internal range. The "
    "shipment service listens on 7101, the routing service on 7102, the billing "
    "service on 7103, the notification service on 7104, the tracking service on "
    "7105, and the customs service on 7106. The internal administration console is "
    "served on 7100 and is reachable only from the operations bastion. The shared "
    "metrics scrape endpoint is 9100 on every host and is internal only. None of the "
    "internal ports are reachable from the public internet under any configuration. "
    + filler(14, 2))

add(3, "Service Inventory",
    "The platform comprises the shipment service, the routing service, the billing "
    "service, the notification service, the tracking service, and the customs "
    "service, together with a set of shared platform services for identity, "
    "configuration, and observability. Each service is owned by a named team and "
    "each team maintains its own runbook set. " + filler(16, 3))

# ---- Recovery windows: the buried needle cluster is set up here and resolved in 41 ----
add(4, "Recovery Objectives Overview",
    "The platform defines several distinct recovery operations, and each one has its "
    "own target window. It is a common error to conflate them, so this section names "
    "them explicitly and the detailed procedures appear in the data and resilience "
    "sections later in this manual. The warm regional failover, the hot store "
    "rebuild, the warm store rebuild, the cold archive restore, and the full cluster "
    "rebuild are five different operations with five different target windows. Do not "
    "assume that because two of them are measured in hours they share a target. "
    + filler(14, 4))

add(5, "Availability Targets",
    "The platform commits to an availability target of 99.95 percent for the core "
    "shipment and tracking surfaces measured monthly, and 99.9 percent for the "
    "reporting surfaces. The error budget derived from these targets governs the "
    "release freeze policy described later. " + filler(15, 5))

add(6, "Notification Retention",
    "The body content of a customer notification is retained for 72 hours after it is "
    "sent, after which only the delivery metadata is kept. The delivery metadata, "
    "which records that a notification was sent and to which channel, is retained for "
    "90 days. These two retention windows are frequently confused, so note that the "
    "content body is the shorter 72 hour window and the metadata is the longer 90 day "
    "window. " + filler(14, 6))

add(7, "Just in Time Access",
    "Standing production access is not granted. Instead, an engineer requests a just "
    "in time grant that is scoped to the action and that expires automatically. The "
    "general production grant is valid for a maximum of 8 hours. A grant that touches "
    "the production database is capped more tightly at 2 hours because of the "
    "sensitivity of the data. A grant to the customs service, which carries regulated "
    "data, is capped at 1 hour. Do not conflate the general 8 hour grant with the 2 "
    "hour database grant or the 1 hour customs grant. " + filler(13, 7))

add(8, "Token Lifetimes",
    "Service to service certificates are valid for 24 hours and rotate automatically. "
    "A customer facing access token is valid for 60 minutes, and the paired refresh "
    "token is valid for 30 days. An internal session token for the administration "
    "console is valid for 4 hours. These lifetimes are independent of the access "
    "grant windows in the previous section. " + filler(13, 8))

add(9, "Autoscaling",
    "The autoscaler adds capacity when CPU utilisation exceeds 60 percent sustained "
    "over a 5 minute window, and it removes capacity when utilisation falls below 40 "
    "percent sustained over a 15 minute window. The asymmetry between the 5 minute "
    "scale up window and the 15 minute scale down window is deliberate and prevents "
    "flapping. " + filler(14, 9))

add(10, "Rate Limiting",
    "The default rate limit is 600 requests per minute per client. A higher "
    "commitment tier raises this to 3000 requests per minute under contract. The "
    "tracking ingest path is metered separately and accepts up to 50000 events per "
    "second across the fleet. " + filler(14, 10))

# ---- Sections 11 to 25: deployment, incident, maintenance, with more clusters ----
add(11, "Release Cadence",
    "The release train departs twice per week, on Tuesday and Thursday. A change that "
    "is not ready by the cut off waits for the next train. An out of band deployment "
    "outside the train requires duty manager approval and a recorded justification. "
    + filler(15, 11))

add(12, "Canary Bake Time",
    "Every production change bakes on the canary cohort before it is widened. The "
    "current minimum canary bake time is 45 minutes. This value was historically 20 "
    "minutes under platform revisions in the 7 series, and it was raised to 45 "
    "minutes in revision 9.0 following the incident described in the incident review "
    "section. Any reference to a 20 minute bake is historical and superseded. There "
    "is also a 10 minute soak between successive production waves, which is a "
    "different control from the canary bake. " + filler(13, 12))

add(13, "Warm Regional Failover",
    "If a region degrades, the platform promotes a warm standby in the secondary "
    "region. The target recovery time for this warm regional failover is 30 minutes. "
    "The recovery point objective for the failover is 60 seconds of data, meaning at "
    "most 60 seconds of writes may be lost. Do not report the 60 second recovery "
    "point as if it were the recovery time. " + filler(13, 13))

add(14, "Incident Review Reference",
    "The March incident referenced elsewhere in this manual was a partial outage "
    "caused by a change that passed a 20 minute canary bake but failed under "
    "sustained load that only appeared after roughly 35 minutes. The corrective "
    "action raised the canary bake to 45 minutes. The incident did not change any "
    "recovery target. " + filler(15, 14))

add(15, "Maintenance Notice Periods",
    "Routine maintenance that carries no expected customer impact requires 72 hours "
    "of notice. Disruptive maintenance that may degrade a customer surface requires 7 "
    "days of notice. Emergency maintenance to address an active security issue may be "
    "performed with the shortest practical notice and is recorded after the fact. "
    + filler(14, 15))

add(16, "Data Retention by Tier",
    "Application logs are retained hot for 30 days and then expire. Distributed traces "
    "are retained for 7 days. Staging environment data is retained for 7 days and is "
    "then purged. Metrics are retained at full resolution for 15 days and downsampled "
    "thereafter. The audit trail is retained for 3 years. Booking and shipment records "
    "are retained for 7 years to satisfy commercial and regulatory obligations. "
    + filler(13, 16))

add(17, "Cold Restore From Backup",
    "A full cold restore of an entire cluster from backup, used only in a total loss "
    "scenario, targets 4 hours. This is distinct from the warm regional failover, "
    "which targets 30 minutes, and from the per store rebuilds described in the data "
    "resilience section. The 4 hour figure is the full cluster rebuild, not any single "
    "store restore. " + filler(13, 17))

add(18, "Notification Channels",
    "Notifications are delivered over email, SMS, and webhook. The webhook channel "
    "retries on failure with exponential backoff for up to 24 hours before the "
    "notification is parked. The content retention for a parked notification follows "
    "the 72 hour content rule from the retention section. " + filler(14, 18))

add(19, "Glossary of Windows",
    "For convenience the following windows are summarised. The canary bake is 45 "
    "minutes. The warm regional failover target is 30 minutes. The full cluster cold "
    "restore target is 4 hours. The general just in time grant is 8 hours and the "
    "database grant is 2 hours. The notification content retention is 72 hours and the "
    "metadata retention is 90 days. This glossary is a cross reference only and the "
    "owning section governs in case of any discrepancy. Note that the cold archive "
    "restore is described in its own section and is not the same as the full cluster "
    "cold restore. " + filler(12, 19))

add(20, "Circuit Breaker",
    "A service trips its circuit breaker to a downstream dependency when the error "
    "rate to that dependency exceeds 50 percent over the last 20 calls. The breaker "
    "half opens after 30 seconds and fully closes after a documented number of "
    "successful probes. The 50 percent over 20 calls trip condition is separate from "
    "the autoscaler thresholds. " + filler(13, 20))

add(21, "Disaster Recovery Drills",
    "The platform runs a disaster recovery drill on a fixed schedule. The warm "
    "regional failover is drilled monthly and is expected to meet its 30 minute "
    "target. The full cluster cold restore is drilled quarterly and is expected to "
    "meet its 4 hour target. The cold archive restore is drilled twice per year. "
    + filler(14, 21))

add(22, "On Call Expectations",
    "The primary on call engineer acknowledges a page within 5 minutes. If the page is "
    "not acknowledged within that window the secondary is engaged. Out of hours work "
    "beyond 30 minutes is logged for time off in lieu. The 5 minute acknowledgement "
    "window is distinct from the 30 minute logging threshold. " + filler(13, 22))

add(23, "Change Approval",
    "A standard change requires one reviewer. A change to a customer facing surface "
    "requires two reviewers, the release owner and a second approver. A rollback does "
    "not require a second approver and may be executed by a single on call engineer. "
    "Do not conflate the two person promotion rule with the single approver rollback "
    "rule. " + filler(13, 23))

add(24, "Status Page Updates",
    "During an incident the first status page update is posted within 30 minutes of "
    "the incident being declared, and subsequent updates follow at least every 60 "
    "minutes until resolution. The 30 minute initial update window is a "
    "communications control and is unrelated to any recovery target. " + filler(13, 24))

add(25, "Freeze Policy",
    "When the error budget is exhausted, a release freeze is declared and only "
    "reliability changes are permitted until the budget recovers. An emergency deploy "
    "during a freeze requires director approval. " + filler(15, 25))

# ---- Sections 26 to 40: data platform deep dive, leading to the needle in 41 ----
add(26, "Commercial Service Levels",
    "The committed transit days for each commercial service level are set as "
    "commercial terms and are not stated in this operations manual. Operations refers "
    "all questions about committed transit days to the commercial team. This manual "
    "deliberately does not state a transit day figure for any service level. "
    + filler(14, 26))

add(27, "Data Store Topology",
    "The data platform is organised into three tiers. The hot tier serves live "
    "operational reads and writes. The warm tier serves recent analytical queries. "
    "The cold tier is an archive that is not queried directly and exists only for "
    "long term retention and recovery. Each tier has its own rebuild or restore "
    "procedure with its own target window, and these are described in the following "
    "sections. " + filler(13, 27))

add(28, "Hot Store Rebuild",
    "If the hot operational store is lost, it is rebuilt from the most recent "
    "incremental snapshot plus the write ahead log. The target window for a hot store "
    "rebuild is 2 hours. This is the fastest store rebuild because the hot store is "
    "the most frequently snapshotted. Do not confuse the 2 hour hot store rebuild with "
    "the 2 hour database just in time grant from the access section, which is an "
    "unrelated control that happens to share a number. " + filler(13, 28))

add(29, "Warm Store Rebuild",
    "If the warm analytical store is lost, it is rebuilt from the nightly full "
    "snapshot plus the day's incremental snapshots. The target window for a warm "
    "store rebuild is 6 hours. The warm store rebuild is slower than the hot store "
    "rebuild because the warm store is snapshotted less frequently. " + filler(13, 29))

add(30, "Snapshot Schedule",
    "The hot store takes an incremental snapshot every 15 minutes and a full snapshot "
    "every 24 hours. The warm store takes an incremental snapshot every hour and a "
    "full snapshot every 24 hours. The cold archive is written once per day from the "
    "warm store full snapshot and is then sealed. " + filler(14, 30))

add(31, "Snapshot Retention",
    "Hot store incremental snapshots are retained for 7 days. Hot store full snapshots "
    "are retained for 30 days. Warm store full snapshots are retained for 90 days. "
    "Cold archive segments are retained for 7 years to match the booking record "
    "retention. " + filler(13, 31))

add(32, "Encryption at Rest",
    "All three tiers are encrypted at rest with keys held in the platform key service. "
    "The cold archive uses a separate key hierarchy so that a compromise of the "
    "operational keys does not expose the archive. Key rotation for the operational "
    "keys occurs every 90 days and for the archive keys every 180 days. " + filler(13, 32))

add(33, "Archive Storage Medium",
    "The cold archive is stored on a high latency object store optimised for cost "
    "rather than retrieval speed. Retrieval from this medium incurs a rehydration "
    "delay before the data becomes readable, and this rehydration delay is the main "
    "reason the cold archive restore target is longer than the other store rebuilds. "
    + filler(14, 33))

add(34, "Archive Integrity",
    "Each cold archive segment carries a checksum and a manifest. Before a restore "
    "begins, the manifest is verified, and a segment that fails verification is "
    "fetched from the secondary archive copy held in a different region. The "
    "verification step adds to the restore time and is included in the restore target. "
    + filler(14, 34))

add(35, "Backup Verification Cadence",
    "Hot store snapshots are test restored weekly. Warm store snapshots are test "
    "restored monthly. Cold archive segments are test restored quarterly. A failed "
    "test restore raises a high severity reliability incident. " + filler(14, 35))

add(36, "Cross Region Replication",
    "The hot and warm stores are replicated to the secondary region continuously. The "
    "cold archive is replicated to the secondary region once per day after the daily "
    "seal. The replication lag for the hot store is under 60 seconds, which is what "
    "bounds the failover recovery point. " + filler(13, 36))

add(37, "Tiering Lifecycle",
    "Operational data ages out of the hot tier into the warm tier after 30 days, and "
    "out of the warm tier into the cold archive after 180 days. Once in the cold "
    "archive, data is retained for the full 7 year window and is never tiered back. "
    + filler(14, 37))

add(38, "Restore Authorisation",
    "A hot or warm store rebuild may be initiated by the on call engineer. A cold "
    "archive restore is more disruptive and more costly, so it requires duty manager "
    "authorisation in addition to the on call engineer. " + filler(14, 38))

add(39, "Restore Communication",
    "When any store restore is initiated, the incident channel is notified and the "
    "status page is updated within the standard 30 minute communications window. The "
    "communications window is the same regardless of which store is being restored "
    "and is independent of the restore target. " + filler(13, 39))

add(40, "Restore Sequencing",
    "When more than one tier must be recovered, the hot store is rebuilt first to "
    "restore live service, then the warm store, and the cold archive restore is "
    "performed last because it is the slowest and is rarely on the critical path for "
    "live service. " + filler(14, 40))

# THE NEEDLE - Section 41. The Tier 3 cold archive restore SLA is 26 hours.
add(41, "Cold Archive Restore Target",
    "The cold archive restore, also called the Tier 3 restore, recovers data from the "
    "sealed cold archive segments described in the preceding sections. Because the "
    "archive is held on the high latency object store and each segment must be "
    "rehydrated and have its manifest verified before the data is readable, the cold "
    "archive restore has the longest target window of any recovery operation on the "
    "platform. The committed target for a full cold archive restore is 26 hours. This "
    "26 hour target is the current committed value and it supersedes all earlier "
    "figures. To restate the surrounding windows so they are not confused with this "
    "one: the warm regional failover targets 30 minutes, the hot store rebuild targets "
    "2 hours, the full cluster cold restore targets 4 hours, the warm store rebuild "
    "targets 6 hours, and the cold archive Tier 3 restore targets 26 hours. The cold "
    "archive restore is the only operation whose target is measured in tens of hours. "
    + filler(11, 41))

# ---- Sections 42 to 60: more operations content, with the superseded 18h restatement ----
add(42, "Severity Matrix",
    "Severity one is a full outage of a core surface or a confirmed data loss event. "
    "Severity two is a partial degradation of a core surface. Severity three is a "
    "degradation of a non core surface or a single tenant issue. The assigned "
    "severity drives the notification and escalation path. " + filler(15, 42))

add(43, "Escalation Windows",
    "A severity one incident is escalated to the incident commander within 10 minutes. "
    "A severity two incident is escalated within 30 minutes. A severity three incident "
    "is escalated within 4 hours. These escalation windows are communications "
    "controls and are not recovery targets. " + filler(14, 43))

add(44, "Post Incident Review",
    "Every severity one and severity two incident receives a written post incident "
    "review within 5 business days. The review is blameless and focuses on systemic "
    "causes and corrective actions rather than individual fault. " + filler(15, 44))

add(45, "Customer Communications",
    "External communications during an incident are owned by the communications lead, "
    "not the on call engineer, so that the engineer can focus on remediation. The "
    "communications lead uses the version controlled notification templates. "
    + filler(15, 45))

add(46, "Vendor Dependencies",
    "The platform depends on an external payment processor and an external mapping "
    "provider. Each vendor dependency has a documented fallback. If the mapping "
    "provider is unavailable, routing falls back to a cached map that is refreshed "
    "every 24 hours. " + filler(14, 46))

add(47, "Configuration Management",
    "All configuration is version controlled and applied through the configuration "
    "service. A configuration change follows the same staged rollout as a code change, "
    "including the 45 minute canary bake. " + filler(15, 47))

add(48, "Secret Management",
    "Secrets are stored in the platform secret service and are never committed to "
    "source control. A secret is rotated on a documented schedule and immediately on "
    "any suspected compromise. " + filler(15, 48))

add(49, "Network Segmentation",
    "The production network is segmented so that the data tier is reachable only from "
    "the service tier, and the service tier is reachable only from the gateway. The "
    "operations bastion is the only host that may reach the administration console on "
    "7100. " + filler(14, 49))

add(50, "Logging Standards",
    "All logs are structured and carry a correlation identifier so that a single "
    "request can be traced across services. Logs are retained hot for 30 days per the "
    "retention section. " + filler(15, 50))

add(51, "Tracing Standards",
    "Distributed traces sample at a documented rate under normal load and at a higher "
    "rate during an active incident. Traces are retained for 7 days. " + filler(15, 51))

add(52, "Metrics Standards",
    "Metrics are emitted at a fixed cardinality budget per service to prevent "
    "cardinality explosions. Metrics are retained at full resolution for 15 days. "
    + filler(15, 52))

add(53, "Dashboards",
    "Every service has a standard dashboard with the four golden signals. The on call "
    "engineer begins every investigation from the dashboard. " + filler(16, 53))

add(54, "Runbook Standards",
    "Every alert links to a runbook. A runbook that is found to be stale during an "
    "incident is flagged for revision in the post incident review. " + filler(16, 54))

add(55, "Capacity Headroom",
    "The platform maintains a documented headroom above the trailing peak so that a "
    "demand spike can be absorbed without emergency scaling. The headroom target is "
    "revisited whenever a large customer is onboarded. " + filler(15, 55))

add(56, "Load Shedding",
    "Under extreme load the platform sheds the lowest priority traffic first to "
    "preserve the core shipment and tracking surfaces. Load shedding is a last resort "
    "after autoscaling has been exhausted. " + filler(15, 56))

add(57, "Graceful Degradation",
    "When a non core dependency is unavailable, the affected surface degrades "
    "gracefully rather than failing hard. For example, if the mapping provider is "
    "down, estimated arrival times are served from the cached map. " + filler(15, 57))

# The superseded restatement trap - Section 58 silently restates an OLD cold archive value.
add(58, "Historical Recovery Notes",
    "For historical context, earlier revisions of this manual committed to shorter "
    "recovery windows before the archive was migrated to the high latency object "
    "store. Under the revision 8 series the cold archive restore target was 18 hours, "
    "the warm store rebuild was 4 hours, and the hot store rebuild was 90 minutes. "
    "These historical figures are recorded here for context only and are superseded by "
    "the current targets stated in the data resilience sections. The current cold "
    "archive restore target is the value stated in the Cold Archive Restore Target "
    "section, not the historical 18 hour figure. " + filler(12, 58))

add(59, "Compliance Obligations",
    "The platform retains booking and shipment records for 7 years and the audit trail "
    "for 3 years. A data subject access request is fulfilled within the statutory "
    "window tracked by the compliance team. " + filler(15, 59))

add(60, "Document Control",
    "This manual is reviewed every quarter. The current revision is 9.4. Each section "
    "owns its topic and governs in case of any discrepancy with a cross reference or a "
    "glossary entry. Historical figures recorded for context are always superseded by "
    "the current owning section. " + filler(15, 60))


def render():
    lines = ["# Cardinal Freight Systems - Operations and Policy Manual",
             "",
             "Revision 9.4. Internal operational reference. This document is the single "
             "source of truth for platform operation. Where any value is restated in a "
             "glossary or a cross reference, the section that owns the topic governs.",
             ""]
    for num, title, body in SECTIONS:
        lines.append(f"## Section {num} - {title}")
        lines.append("")
        # Append extra on-topic filler to every section so the manual reaches the
        # 60000+ token target and the needle in Section 41 sits far from the
        # questions' keywords. The needle section itself gets less trailing filler
        # so the 26 hour value stays prominent within its own section, but is still
        # buried deep in the document by position.
        extra = 18 if num != 41 else 6
        body_full = body + " " + filler(extra, seed_offset=num + 7)
        wrapped = textwrap.fill(body_full, width=92)
        lines.append(wrapped)
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    text = render()
    with open(OUT, "w") as f:
        f.write(text)
    words = len(text.split())
    print(f"wrote {OUT}: {words} words, {len(text)} chars, {len(SECTIONS)} sections")
