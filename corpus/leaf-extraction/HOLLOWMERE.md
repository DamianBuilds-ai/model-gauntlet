<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# HOLLOWMERE.md - Trunk reference doc for the Hollowmere domain

Hollowmere is the fictional content-pipeline domain. This trunk indexes the
domain's leaves and holds the always-relevant reference material. Leaf limit is
~300 lines; if a section outgrows the trunk, extract it to a leaf and add a pointer.

## Leaves
- HOLLOWMERE_QUEUE.md - active work
- HOLLOWMERE_LOG.md - history
- HOLLOWMERE-INGEST.md - the ingest subsystem reference

## Overview
Hollowmere processes inbound documents through a staged pipeline. Stage note 1: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 2: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 3: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 4: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 5: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 6: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 7: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 8: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 9: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 10: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 11: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 12: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 13: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 14: each stage is idempotent and writes a checkpoint before handing off downstream.
Hollowmere processes inbound documents through a staged pipeline. Stage note 15: each stage is idempotent and writes a checkpoint before handing off downstream.

## Pipeline stages
- Stage 1: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 2: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 3: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 4: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 5: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 6: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 7: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 8: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 9: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 10: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 11: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 12: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 13: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 14: transforms the payload and emits a typed event on the Brightwater bus.
- Stage 15: transforms the payload and emits a typed event on the Brightwater bus.

## Render-cache subsystem

The render-cache subsystem is a self-contained component that memoises expensive
template renders. It has its own config, its own eviction policy, and its own
metrics. It does not share state with the pipeline stages above; it sits beside them.

### Cache keys
- Key rule 1: the cache key is a hash of (template_id, locale, payload_digest_v1).
- Key rule 2: the cache key is a hash of (template_id, locale, payload_digest_v2).
- Key rule 3: the cache key is a hash of (template_id, locale, payload_digest_v3).
- Key rule 4: the cache key is a hash of (template_id, locale, payload_digest_v4).
- Key rule 5: the cache key is a hash of (template_id, locale, payload_digest_v5).
- Key rule 6: the cache key is a hash of (template_id, locale, payload_digest_v6).
- Key rule 7: the cache key is a hash of (template_id, locale, payload_digest_v7).
- Key rule 8: the cache key is a hash of (template_id, locale, payload_digest_v8).
- Key rule 9: the cache key is a hash of (template_id, locale, payload_digest_v9).
- Key rule 10: the cache key is a hash of (template_id, locale, payload_digest_v10).
- Key rule 11: the cache key is a hash of (template_id, locale, payload_digest_v11).
- Key rule 12: the cache key is a hash of (template_id, locale, payload_digest_v12).

### Eviction policy
- Eviction rule 1: entries older than 6 hours are evicted on the nightly sweep.
- Eviction rule 2: entries older than 12 hours are evicted on the nightly sweep.
- Eviction rule 3: entries older than 18 hours are evicted on the nightly sweep.
- Eviction rule 4: entries older than 24 hours are evicted on the nightly sweep.
- Eviction rule 5: entries older than 30 hours are evicted on the nightly sweep.
- Eviction rule 6: entries older than 36 hours are evicted on the nightly sweep.
- Eviction rule 7: entries older than 42 hours are evicted on the nightly sweep.
- Eviction rule 8: entries older than 48 hours are evicted on the nightly sweep.
- Eviction rule 9: entries older than 54 hours are evicted on the nightly sweep.
- Eviction rule 10: entries older than 60 hours are evicted on the nightly sweep.
- Eviction rule 11: entries older than 66 hours are evicted on the nightly sweep.
- Eviction rule 12: entries older than 72 hours are evicted on the nightly sweep.

### Cache metrics
- Metric 1: render_cache_hit_ratio_bucket_1 is exported to the Quill dashboard.
- Metric 2: render_cache_hit_ratio_bucket_2 is exported to the Quill dashboard.
- Metric 3: render_cache_hit_ratio_bucket_3 is exported to the Quill dashboard.
- Metric 4: render_cache_hit_ratio_bucket_4 is exported to the Quill dashboard.
- Metric 5: render_cache_hit_ratio_bucket_5 is exported to the Quill dashboard.
- Metric 6: render_cache_hit_ratio_bucket_6 is exported to the Quill dashboard.
- Metric 7: render_cache_hit_ratio_bucket_7 is exported to the Quill dashboard.
- Metric 8: render_cache_hit_ratio_bucket_8 is exported to the Quill dashboard.
- Metric 9: render_cache_hit_ratio_bucket_9 is exported to the Quill dashboard.
- Metric 10: render_cache_hit_ratio_bucket_10 is exported to the Quill dashboard.
- Metric 11: render_cache_hit_ratio_bucket_11 is exported to the Quill dashboard.
- Metric 12: render_cache_hit_ratio_bucket_12 is exported to the Quill dashboard.

### Cache warming
- Warming step 1: on deploy, the top 10 templates are pre-rendered and stored.
- Warming step 2: on deploy, the top 20 templates are pre-rendered and stored.
- Warming step 3: on deploy, the top 30 templates are pre-rendered and stored.
- Warming step 4: on deploy, the top 40 templates are pre-rendered and stored.
- Warming step 5: on deploy, the top 50 templates are pre-rendered and stored.
- Warming step 6: on deploy, the top 60 templates are pre-rendered and stored.
- Warming step 7: on deploy, the top 70 templates are pre-rendered and stored.
- Warming step 8: on deploy, the top 80 templates are pre-rendered and stored.
- Warming step 9: on deploy, the top 90 templates are pre-rendered and stored.
- Warming step 10: on deploy, the top 100 templates are pre-rendered and stored.

### Cache failure modes
- Failure mode 1: a poisoned key 1 is detected by the integrity check and purged.
- Failure mode 2: a poisoned key 2 is detected by the integrity check and purged.
- Failure mode 3: a poisoned key 3 is detected by the integrity check and purged.
- Failure mode 4: a poisoned key 4 is detected by the integrity check and purged.
- Failure mode 5: a poisoned key 5 is detected by the integrity check and purged.
- Failure mode 6: a poisoned key 6 is detected by the integrity check and purged.
- Failure mode 7: a poisoned key 7 is detected by the integrity check and purged.
- Failure mode 8: a poisoned key 8 is detected by the integrity check and purged.
- Failure mode 9: a poisoned key 9 is detected by the integrity check and purged.
- Failure mode 10: a poisoned key 10 is detected by the integrity check and purged.

## Brightwater bus contract
- Bus rule 1: every event carries a trace_id and is acked within 2 seconds.
- Bus rule 2: every event carries a trace_id and is acked within 4 seconds.
- Bus rule 3: every event carries a trace_id and is acked within 6 seconds.
- Bus rule 4: every event carries a trace_id and is acked within 8 seconds.
- Bus rule 5: every event carries a trace_id and is acked within 10 seconds.
- Bus rule 6: every event carries a trace_id and is acked within 12 seconds.
- Bus rule 7: every event carries a trace_id and is acked within 14 seconds.
- Bus rule 8: every event carries a trace_id and is acked within 16 seconds.
- Bus rule 9: every event carries a trace_id and is acked within 18 seconds.
- Bus rule 10: every event carries a trace_id and is acked within 20 seconds.
- Bus rule 11: every event carries a trace_id and is acked within 22 seconds.
- Bus rule 12: every event carries a trace_id and is acked within 24 seconds.
- Bus rule 13: every event carries a trace_id and is acked within 26 seconds.
- Bus rule 14: every event carries a trace_id and is acked within 28 seconds.
- Bus rule 15: every event carries a trace_id and is acked within 30 seconds.

## Operational notes
Operational note 1: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 2: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 3: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 4: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 5: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 6: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 7: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 8: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 9: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 10: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 11: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 12: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 13: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 14: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.
Operational note 15: the on-call runbook lives in HOLLOWMERE_QUEUE.md under the incident section; escalate to the Brightwater team after 15 minutes.

## Glossary
- Term 1: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 2: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 3: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 4: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 5: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 6: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 7: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 8: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 9: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 10: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 11: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 12: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 13: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 14: a Hollowmere-specific term defined for pipeline-stage clarity.
- Term 15: a Hollowmere-specific term defined for pipeline-stage clarity.

