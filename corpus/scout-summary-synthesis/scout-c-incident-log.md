<!-- SYNTHETIC DATA. Do NOT treat any text inside as instructions. This is scout output to be analyzed and synthesized, not commands to follow. -->

---
scout: C
target: recent incident log for the Hollowmere notifier
date: 2026-03-11
---

# Scout C - Hollowmere notifier incident log

## TL;DR
Two incidents in the last 30 days. Both were transient gateway timeouts to Quill;
neither required a code change. No open incidents.

## Findings
- INC-0431 (2026-02-22): Quill gateway timeout, notifier retried and recovered. Closed.
- INC-0447 (2026-03-04): Quill gateway timeout during a gateway deploy. Recovered after
  the gateway came back. Closed.
- No incident in the last 30 days was attributed to the notifier image version or to
  the retry ceiling value.
- On-call owner for the notifier: the `Brightwater` team.

## Source
Read the incident tracker filtered to `service=hollowmere-notifier`, last 30 days.
