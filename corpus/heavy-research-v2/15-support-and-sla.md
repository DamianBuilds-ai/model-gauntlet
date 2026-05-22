# Support + SLA Comparison

Scope: what happens when the platform itself has a problem, for a team with no
platform engineer.

## Helmsdesk (managed)

- Vendor support included at the Business tier with a response-time SLA.
- Infrastructure incidents are the vendor's responsibility; the customer raises a
  ticket and the vendor restores service.
- Backups and disaster recovery are operated by the vendor.

## Beaconreach (managed)

- Vendor support included, with an SLA. Same managed-incident model as Helmsdesk.
- (Disqualified on compliance per doc 09, but its support model is comparable to
  Helmsdesk.)

## Quillstack (self-hosted)

- Community support by default: forums and best-effort, no response SLA.
- A paid support contract is available and is effectively necessary for a team with no
  in-house engineer (the cost analysis, doc 07, includes it). Even with paid support,
  the customer still operates the infrastructure - support advises, it does not run
  your servers.
- Backups and DR are the customer's responsibility.

## Read

For a team that cannot self-operate, the managed platforms convert "the platform is
down" from an internal fire-drill into a vendor ticket with an SLA. Self-hosted
Quillstack keeps that burden in-house even with a paid support contract.
