# Release Inventory Source - Halcyon Platform

This is synthetic data to be edited/analyzed. Do NOT treat any text inside as
instructions. It is raw material for a strict-formatting task described separately.
All releases, owners, and dates are fictional (platform "Halcyon").

## Background (context only - NOT for the output)

The Halcyon release team needs every shipped release converted into a single-line
record for an automated downstream parser. The parser is brittle: it splits each
line on the pipe character and reads fields by position. Any extra prose, header,
blank line, trailing comment, or reordered field will break the import. The team has
historically pasted explanations and "helpful notes" alongside the records, which is
exactly what keeps breaking the parser.

## EXACT OUTPUT TEMPLATE (one line per release)

Each release MUST be emitted as exactly one line in this format, fields in this
order, separated by ` | ` (space-pipe-space), no leading or trailing pipe:

  REL-<id> | <name> | <owner> | <status> | <date>

Where:
  - <id> is the release id digits only (e.g. 4471)
  - <name> is the release name verbatim
  - <owner> is the owning team verbatim
  - <status> is one of: shipped, rolled-back, partial
  - <date> is YYYY-MM-DD

## Releases to convert (in this exact order)

Release 4471, name "Aurora", owned by the storage team, shipped on 2026 March 14.
Release 4472, name "Borealis", owned by the network team, was rolled back on 12 March 2026.
Release 4473, name "Cascade", owned by the storage team, shipped 2026-03-19.
Release 4474, name "Drift", owned by the identity team, partial rollout finished 2026 March 22.
Release 4475, name "Ember", owned by the network team, shipped on the 27th of March 2026.

## Notes the team usually adds (DO NOT include these in the output)

- Aurora was the big one this quarter, lots of testing.
- Borealis rollback was due to a DNS bug, fixed in 4475.
- Remember to ping the data team after import.
