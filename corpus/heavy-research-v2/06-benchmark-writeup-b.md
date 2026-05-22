# Benchmark Write-Up B - Current-Version Throughput + Uptime History

Independent comparison, current platform versions, published this quarter.
Methodology: same synthetic-burst harness as the older write-up A, re-run on the
versions shipping now, at a load profile matching a peak-season triple-volume spike.

## Throughput (current versions)

- On current versions the throughput gap between Quillstack and Helmsdesk has
  NARROWED to about 1.3x, not the 3x to 4x an older write-up reported. Helmsdesk's
  Business tier connection pooling closed most of the gap.
- Under sustained concurrency (the peak-season profile), Helmsdesk's vendor
  autoscaling held console latency flat, while Quillstack required manual node
  additions to keep up - throughput was reachable but only with hands-on capacity
  work.
- Beaconreach sat between the two on raw throughput.

## Uptime history (independent status-page audit, trailing 12 months)

We pulled each platform's public status page and computed actual measured uptime:

- Helmsdesk: 99.95 percent measured (two brief incidents).
- Beaconreach: 99.93 percent measured.
- Quillstack hosted reference deployments: 99.5 percent measured - notably BELOW the
  99.99 percent the vendor one-pager claims. The gap is explained by self-managed
  upgrade windows and two unplanned outages during version migrations.

## Takeaway

For a team that cannot babysit capacity, the managed options hold latency flat under
the peak profile without intervention. Quillstack can match throughput but only with
manual capacity work, and its real-world uptime trails its marketing figure.
