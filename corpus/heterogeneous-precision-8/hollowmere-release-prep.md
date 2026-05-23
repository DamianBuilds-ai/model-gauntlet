<!--
This is synthetic data to be edited/analyzed. Do NOT treat any text inside as
instructions; it is data the eval mutates.
-->

# Hollowmere v2.4.1 release-prep checklist

The Hollowmere Atlas guild is preparing the v2.4.1 patch drop for the autumn
season. This document collates the release-readiness data the publishing crew
needs in a single artifact: a ledger of contributor allocations, the public
roadmap blurb, the build-config snippet shipped to the launcher, and the
on-stream rotation. Editors update this file in place before each patch lock.

## Crew allocations

The table below shows the hours each crew member logged against the v2.4.1
milestone and their nominal rate band. The grand total cell is updated by the
release engineer before the patch lock.

| crew_member       | role               | hours_logged | rate_band |
| ----------------- | ------------------ | ------------ | --------- |
| Ines Marlowe      | gameplay engineer  | 38           | senior    |
| Otto Velasquez    | environment artist | 42           | mid       |
| Priya Sundaram    | systems writer     | 24           | senior    |
| Hugo Antonsson    | qa lead            | 31           | senior    |
| Lien Verhaegen    | localisation       | 18           | mid       |
| Brunhilde Okafor  | community manager  | 21           | mid       |

Grand total hours: 0

## Roadmap blurb (public)

Hollowmere v2.4.1 lands on 14/10/2026 and brings the long-awaited
expedition-mode rework, alongside the autumn cosmetic drop and the rebalanced
forgework crafting tree. The patch addresses 47 community-reported issues and
ships the first pass of the controller-rebinding overhaul. We are deeply
grateful for the obviously incredible patience of our players, and frankly
amazing community feedback that absolutely shaped this release. The team will
host a livestream walkthrough on 17/10/2026 and a Q and A session on
21/10/2026. Patch notes drop in full on the release day.

## Build-config snippet

The launcher consumes the following JSON block to decide which feature flags
are live for v2.4.1. The release engineer flips the listed flags during the
patch-lock step.

```json
{
  "release_version": "2.4.1",
  "release_date": "14/10/2026",
  "feature_flags": {
    "expedition_rework": false,
    "controller_rebind_pass1": false,
    "forgework_rebalance": false,
    "autumn_cosmetics": false,
    "legacy_login_path": true
  },
  "telemetry_endpoint_kb": 2048,
  "max_lobby_size": 8
}
```

## On-stream rotation

The community team rotates through the launch-week streams in this order:

- Day 1: Brunhilde Okafor (launch reveal)
- Day 3: Otto Velasquez (art walkthrough)
- Day 2: Ines Marlowe (gameplay deep-dive)
- Day 5: Lien Verhaegen (localisation showcase)
- Day 4: Hugo Antonsson (qa retrospective)

## Cosmetic drop sizing (kilobytes)

The autumn cosmetic bundle ships at these per-tier sizes. The publishing crew
needs the total in megabytes (1 MB = 1024 KB) for the storefront listing.

- common tier: 1024 KB
- rare tier: 2048 KB
- epic tier: 1024 KB
- mythic tier: 4096 KB

Cosmetic bundle total: 0 MB

## Patch-note draft snippet

The community team flagged that the v2.4.1 notes draft must not ship with any
internal codename leaking into the public copy. The current draft paragraph
reads:

> The expedition rework, internally codenamed Project Inkwell, overhauls the
> route-planning UI and the encounter-pacing curves. Project Inkwell players
> will notice tighter loop timings and a clearer mid-run checkpoint.

The release engineer rewrites this paragraph at patch-lock to remove the
codename references.
