# Peak-Season Scaling Projection

Scope: how each platform handles Cardinal's peak season, when ticket volume triples
for roughly 10 weeks.

## The load shape

Baseline is steady. For ~10 weeks, inbound ticket volume and concurrent agent sessions
roughly triple, with sharp daily peaks. The platform must absorb this without the small
support team doing capacity engineering.

## Per platform

- Helmsdesk (managed): vendor autoscaling absorbs the spike. The team does nothing
  operationally. Console latency held flat under the peak profile in the current-version
  benchmark (doc 06).

- Beaconreach (managed): same autoscaling story; the spike is absorbed by the vendor.
  (Compliance still disqualifies it per doc 09, but on scaling alone it is fine.)

- Quillstack (self-hosted): scaling is a MANUAL exercise. Capacity must be added and
  configured ahead of the spike. The current-version benchmark (doc 06) showed it can
  reach the throughput, but only with hands-on node additions, and the postmortem
  (doc 08) is a concrete example of a small team failing to pre-scale and losing most
  of a working day. The older benchmark (doc 05) overstated its raw lead on stale
  versions and does not reflect current behaviour under autoscaling-vs-manual.

## Read

Under the peak profile, the managed options absorb the spike with zero team
intervention. Quillstack's throughput is reachable but conditional on the small team
remembering and executing manual capacity work - the exact failure mode the postmortem
documents.
