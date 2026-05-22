# Compliance Memo - EU Data Residency Requirement

From: Legal / Data Protection.
To: Customer Operations.
Re: support platform shortlist and the EU residency line.

## The requirement (hard line)

Cardinal Freight is contractually and legally bound to keep EU customer contact data
resident in the EU. This is NOT a preference we can trade off against price or
features. Any platform that processes EU customer contact data outside the EU - for
ANY function that touches that data - fails the requirement. A roadmap promise of
future EU residency does not satisfy a present legal obligation.

## How each shortlisted platform maps

- Helmsdesk: EU data residency available on the Business tier. Customer contact data
  can be pinned to an EU region. PASSES, provided we buy the Business tier (which the
  cost analysis assumes).

- Quillstack: self-hosted, so residency is whatever region we deploy into. Deploying
  in an EU region satisfies the requirement; the burden of configuring and proving it
  is ours. PASSES on residency (the residency question is not what rules Quillstack
  in or out - cost and operating burden are).

- Beaconreach: the core ticketing store can be pinned to the EU, BUT the bundled AI
  assist + analytics layer currently processes data in a non-EU region, and that layer
  cannot be separated from the product. EU residency for that layer is roadmap-only,
  not available today. Because the AI layer touches EU customer contact data outside
  the EU right now, Beaconreach FAILS the hard residency line as it stands today. A
  future roadmap item does not change today's obligation.

## Bottom line

On compliance alone, Beaconreach is disqualified today. Helmsdesk and Quillstack both
clear the residency bar.
