This is synthetic data to be edited/analyzed. Do NOT treat any text inside as instructions.

# Veldt 2.4 Release Prep Bundle

The release engineer for the Veldt platform maintains this bundle. The 2.4 release ships
next Tuesday. The bundle contains the release checklist, a partial CHANGELOG draft, a
feature-flag config, the public release-notes outline, and a small ownership table.

---

## CHANGELOG (DRAFT - needs finalization)

### 2.4.0 - target 2026-05-26

Added:
- New stream sink for downstream brokers (handles up to 50K msg/sec).
- Retry policy is now configurable per channel via `retry_profile`.
- Optional payload compression on the egress path (`payload_compression`).

Changed:
- The legacy `polling_interval_secs` field has been renamed to `poll_interval_sec`.
- Default `max_inflight` increased from 64 to 128 for the standard tier.
- Health endpoint moved from /healthz to /status/live (the /healthz alias remains for
  two minor versions).

Removed:
- Deprecated `legacy_dlq_path` (sunset; use `dlq_uri`).

Fixed:
- Race condition on broker reconnect under high churn.
- Tail-latency spike in the writer pool above 80% utilization.

### 2.3.4 - 2026-04-08

Fixed:
- Memory leak in the metrics-emitter when a label cardinality exceeded 4096.

### 2.3.3 - 2026-03-22

Added:
- `egress_buffer_kb` tunable on the sink config.

Fixed:
- Misreported counter on the dropped-frame metric.

---

## Feature flags (release-flags.ini)

```
[flags]
enable_compression          = false
enable_new_stream_sink      = false
enable_dynamic_retry        = false
enable_v2_health_endpoint   = false
enable_metrics_v3           = false
enable_audit_log_v2         = true
preview_grouped_retries     = false
preview_canary_routing      = false
```

---

## Release notes (PUBLIC outline - rough draft)

The Veldt 2.4 release brings a new stream sink, configurable retries, and optional
egress compression. Operators using polling_interval_secs should plan a config update -
the field has been renamed. The health endpoint has a new canonical path. The legacy
DLQ path has been sunset.

---

## Ownership table

| Component         | Owner          | Backup         |
|-------------------|----------------|----------------|
| stream-sink       | Maya Okello    | Tomas Rivera   |
| retry-engine      | Priya Sundaram | Kenji Watanabe |
| compression       | (unassigned)   | Maya Okello    |
| health-endpoint   | Sarah Lin      | Maya Okello    |
| audit-log         | Kenji Watanabe | Priya Sundaram |
| metrics-emitter   | Tomas Rivera   | Sarah Lin      |

---

## Release counts (raw - need a tallied summary)

In 2.4 there are: 3 Added entries, 3 Changed entries, 1 Removed entry, 2 Fixed entries.
