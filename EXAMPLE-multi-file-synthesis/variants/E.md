---
schemaVersion: 1
tier: builder
status: complete
tool_budget_used: 6
---

# Acme Logistics - Comprehensive Cross-File Status Synthesis

## Executive overview

This brief synthesizes three source documents - the API changelog, the open
support ticket digest, and the quarterly roadmap notes - into a single integrated
view. Rather than treating each document as a silo, the analysis below traces the
narrative threads that recur across documents, because the analytical value of a
multi-file synthesis lies precisely in the connective tissue between sources rather
than in the isolated contents of any single source. The dominant finding is that
the product's open issues cluster tightly around the webhook subsystem, with a
secondary cluster around throughput and a tertiary cluster around documentation
fidelity.

## Cross-cutting threads identified across multiple source files

### Thread 1: The webhook signing and reliability complex
The changelog establishes that webhook events were introduced in v3.1.0 with the
`parcel.exception` event, and critically notes that signing via HMAC is planned but
not yet delivered, slated for v3.3.0. The support ticket digest corroborates demand
from the field: TICK-4460 documents three separate customers who explicitly name
HMAC as a precondition for moving production traffic onto webhooks, and TICK-4471
documents a free-tier customer experiencing delivery cessation at approximately 200
events per day. The roadmap notes then close the loop by confirming that signed
webhooks are a committed deliverable for the current quarter and that the security
function has flagged unsigned payloads as the single highest open risk. This is a
genuine three-way convergence.

### Thread 2: Throughput limits and the batch endpoint
The changelog raised the rate limit from 60 to 120 requests per minute for paid
tiers and introduced the `/shipments/batch` endpoint accepting up to 100 shipments.
The support digest's TICK-4455 describes a customer that dropped batch jobs against
the prior 60 rpm ceiling during a demand burst. The roadmap records a Sales request
to promote the batch endpoint during onboarding, motivated by trial churn attributed
to throughput limits.

### Thread 3: Documentation trailing the live API
The changelog added `carrier_reference` in v3.1.0. The support digest's TICK-4448
reports that this field, while live, is undocumented. The roadmap explicitly names
`carrier_reference` as the canonical example of the public reference trailing the
actual API by roughly one minor version.

## Top three issues by combined urgency

1. Free-tier webhook delivery drops, per TICK-4471, compounded by the fact that the
   corrective policy (an explicit documented free-tier volume cap) remains in the
   under-consideration column of the roadmap and is therefore undecided.
2. HMAC signing as a production-adoption blocker, per TICK-4460, reinforced by the
   roadmap commitment and the security top-risk designation.
3. The written confirmation of the v3.1.4 timezone fix requested in TICK-4431,
   which although low in technical severity is an outstanding owed communication.

## Points of agreement and unresolved questions

The three files reinforce each other most strongly on webhook signing: it is
simultaneously demanded by customers, flagged as a security risk, and committed on
the roadmap. The principal unresolved question is whether the forthcoming GraphQL
read API will carry a schema version scheme independent of the REST versioning;
this is raised as an open question in the changelog and left explicitly undecided
in the roadmap, with no source resolving it.

## Recommended next actions

1. Prioritize reproduction of the TICK-4471 free-tier drop and pair it with a
   decision on the documented volume cap.
2. Communicate the HMAC delivery timeline to the three customers in TICK-4460.
3. Issue written confirmation of the timezone fix to the affected Western Australia
   account referenced in TICK-4431.
4. Document the `carrier_reference` field to resolve TICK-4448 and reduce docs debt.
5. Incorporate batch-endpoint guidance into onboarding collateral per the Sales ask.
