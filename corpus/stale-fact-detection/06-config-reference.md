# Cardinal Logistics - Config Reference

The canonical reference for operational configuration keys and their current
values. This file is generated from the live config and is authoritative for
current values. Keys are grouped by subsystem.

## oncall

| key | value | notes |
|-----|-------|-------|
| `oncall.ack_timeout_minutes` | 10 | acknowledgement timeout before escalation to secondary (CL-2026-014, ADR-031) |
| `oncall.rotation_length_days` | 7 | one week per primary |
| `oncall.secondary_required` | true | every rotation has a secondary |

## gateway

| key | value | notes |
|-----|-------|-------|
| `gateway.rate_limit_rpm` | 600 | requests per minute per key (CL-2026-009) |
| `gateway.public_port` | 8443 | TLS terminates here; only public port |

## logging

| key | value | notes |
|-----|-------|-------|
| `logging.hot_retention_days` | 15 | hot-log retention (CL-2026-011) |
| `logging.trace_retention_days` | 7 | distributed trace retention |

## scaling

| key | value | notes |
|-----|-------|-------|
| `scaling.scale_up_cpu_pct` | 60 | scale up above this sustained CPU |
| `scaling.scale_down_cooldown_minutes` | 15 | sustained-below window before removing an instance (CL-2026-021) |

## deploy

| key | value | notes |
|-----|-------|-------|
| `deploy.freeze_start` | Fri 12:00 local | freeze window start (ADR-028 proposal to widen was rejected) |
| `deploy.freeze_end` | Mon 09:00 local | freeze window end |

## warehouse

| key | value | notes |
|-----|-------|-------|
| `warehouse.cutoff_local` | 16:00 | daily same-day dispatch cutoff (CL-2026-017) |
