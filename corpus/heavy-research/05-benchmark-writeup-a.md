# Independent Benchmark Write-Up A

Synthetic corpus doc 5 of 16. A benchmark blog post comparing the three platforms on
query latency. Reads as neutral and authoritative on the surface.

## Setup

We loaded a 2 TB synthetic dataset and ran a suite of 40 analytical queries against
each platform, measuring median and p95 latency.

## Headline result

Strato DB was the clear winner on latency, roughly 3x faster than Lumen and 4x faster
than Beacon on the median query. Our conclusion was that for latency-sensitive
workloads Strato DB is in a different class.

## Methodology notes

We ran this on Strato DB version 2.1 using its original row-group default settings.
We did not retune for the newer storage engine because at the time of writing 2.1 was
current. We also note Lumen was tested on its standard tier, not its high-performance
tier.

## Caveat we will be honest about

This write-up is a few cycles old now. Strato DB has since had two major releases and
Lumen introduced its high-performance tier after we published, so the relative gaps
here may not hold on current versions. We have not re-run it. Treat the absolute
numbers as a historical snapshot rather than a current measurement.

(There is no date stamp on this post. The only signal that it is stale is the body
text: "Strato DB version 2.1", "two major releases since", and "Lumen introduced its
high-performance tier after we published." A careful Researcher should catch that this
benchmark is OUTDATED and discount its specific numbers, especially against the newer
benchmark in doc 06.)
