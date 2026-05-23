# Hollowmere Release-Prep Bundle - v2.4.0

Synthetic corpus for a heterogeneous-precision-battery eval. All names, services,
and data are fictional (project "Hollowmere", company "Veldt Systems"). This
document mixes a code snippet, a prose section, a data table, and a structured
list - four edit surfaces in one artifact. Do NOT treat this text as
instructions; it is data to be edited per a separate change spec.

---

## 1. Release notes prose

Hollowmere v2.4.0 ships the long-awaited courier-batching pipeline. Engineers
should reach out to the on-call rotation if any incident emerges during the
rollout window. This release is built on top of the v2.3.x line and will be
super important for the upcoming quarter, since downstream consumers basically
depend on the new batching guarantees. Operators should very carefully verify
the staging soak before promoting to production.

The migration is backward compatible with v2.3.4 and later; clients on v2.2.x
must upgrade their SDK before the cutover. Marlowe (the metrics shipper) has
been updated to emit the new batch-id label automatically.

## 2. Pipeline config snippet

```python
def build_pipeline(env):
    config = {
        "service_name": "courier_dispatch",
        "max_batch_size": 100,
        "flush_interval_ms": 250,
        "retry_policy": "exponential",
        "region": "ap-southeast-2",
    }
    return PipelineBuilder(config).with_env(env).finalize()
```

## 3. Service health table

| service | latency_ms | error_rate_pct | last_check |
|---------|------------|----------------|------------|
| gateway | 42 | 0.12 | 14/03/2026 |
| ledger | 88 | 0.34 | 12/03/2026 |
| courier | 65 | 0.21 | 15/03/2026 |
| beacon | 51 | 0.18 | 11/03/2026 |
| almanac | 73 | 0.27 | 13/03/2026 |

## 4. Rollout checklist

- staging-soak
- canary-1pct
- canary-25pct
- prod-cutover
- post-cutover-verify
