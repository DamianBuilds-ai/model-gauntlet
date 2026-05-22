# Three-Year Total Cost Analysis

Scope: fully loaded three-year cost for Cardinal Freight (5 support seats, EU
region), INCLUDING the people-time to operate each platform. All figures indicative
and in the same currency unit.

## Helmsdesk (managed)

- Subscription (Business tier, 5 seats, 3 years): ~54,000.
- Operating time: configuration only. No infrastructure to run. Estimated ~0.05 FTE
  of the ops lead's time ongoing. People cost over 3 years: ~9,000.
- Three-year all-in: ~63,000.

## Quillstack (self-managed open source)

- Software license: 0 (open source).
- Infrastructure (servers, DB, cache, backups, EU region, 3 years): ~30,000.
- Operating time: this is the big one. Self-hosting needs upgrades, patching, scaling
  ahead of peak, backup verification, and incident response - with NO dedicated
  platform engineer, this lands on the ops lead. Estimated ~0.4 FTE ongoing. People
  cost over 3 years: ~72,000.
- Paid support contract (recommended given no in-house engineer): ~18,000 over 3
  years.
- Three-year all-in: ~120,000.

## Beaconreach (managed AI bundle)

- Subscription (bundled, 5 seats, 3 years): ~78,000.
- Operating time: configuration only, plus the AI training pass. ~0.05 FTE. People
  cost: ~9,000.
- Three-year all-in: ~87,000.

## Read

On fully-loaded three-year cost, Helmsdesk is the cheapest (~63,000), Beaconreach next
(~87,000), and Quillstack the MOST expensive (~120,000) once the operating time for a
team with no platform engineer is counted. The open-source zero-license figure is
misleading for a small team: the people cost dominates.
