# Independent Benchmark Write-Up B

Synthetic corpus doc 6 of 16. A more recent, more rigorous benchmark. This is the
reliable latency source - it tests current versions.

## Setup

5 TB synthetic dataset (closer to Riverbend's three-year projection than the 2 TB in
write-up A, doc 05). Current versions of all three platforms as of this writing:
Strato DB 4.0 (the new storage engine), Lumen Cloud with its high-performance tier
enabled, and Beacon Analytics current release. 60-query suite, warm and cold runs
reported separately.

## Headline results (median latency, warm)

- Strato DB 4.0: fastest, but the margin over Lumen narrowed sharply versus older
  benchmarks once Lumen's high-performance tier is enabled. Strato is ~1.3x faster
  than Lumen now, not the 3x some older posts claim.
- Lumen Cloud (high-performance tier): close second, and it auto-scales under
  concurrent load where self-managed Strato needed manual tuning to keep up.
- Beacon Analytics: notably slower on large interactive dashboards - 2 to 3x slower
  than the other two at the 5 TB scale, and the gap widens with dashboard complexity.

## Concurrency finding

Under 50 concurrent dashboard users, Lumen held p95 latency best because of
autoscaling. Strato matched it ONLY after manual cluster tuning - which costs ops
time, the thing Riverbend is short on (doc 01, doc 08). Beacon degraded most under
concurrency.

## Bottom line

At Riverbend's projected 5 TB-plus scale and with concurrency, Strato and Lumen are
close on raw latency; Lumen wins on latency-under-load-without-ops-effort; Beacon
trails on interactive latency. This is the current picture; prefer it over the older
write-up A (doc 05).
