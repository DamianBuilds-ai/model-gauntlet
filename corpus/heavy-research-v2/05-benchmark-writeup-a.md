# Benchmark Write-Up A - Support Platform Throughput

Independent throughput comparison across the three platforms. Methodology:
synthetic ticket bursts, measured median time-to-first-render of the agent console
and concurrent-session ceiling.

## Headline result

Quillstack was the clear throughput leader, sustaining roughly 3x to 4x the
concurrent agent sessions of Helmsdesk before console latency degraded, and edging out
Beaconreach as well. If raw throughput under load is the deciding factor, Quillstack
wins comfortably.

## Test conditions

- We tested Quillstack version 2.1 on self-hosted reference hardware.
- Helmsdesk was tested on its Standard tier (the Business tier with its larger
  connection pool had not yet shipped at the time of this test).
- Note: there have been two major Quillstack releases since this test, and Helmsdesk
  introduced its high-throughput Business tier connection pooling AFTER we published.
  We have not re-run against current versions.

## Caveat

These numbers reflect the versions named above. Treat the headline multiple as a
point-in-time figure, not a current one. A newer run on current versions may differ.
