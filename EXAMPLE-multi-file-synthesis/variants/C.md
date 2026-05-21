# Acme Logistics Status Brief

Here is a synthesis of the three source files.

The biggest theme across the files is webhooks. The API added webhook events in
v3.1.0, signing is planned for v3.3.0, and several support tickets are blocked on
HMAC signing - three customers will not move production traffic until payloads are
verifiable. The roadmap confirms signed webhooks are committed this quarter and
that security flagged unsigned payloads as the top risk.

Throughput is a second theme. The batch endpoint and the higher rate limit address
the kind of drops Southgate Freight hit in TICK-4455. Sales wants batch promoted in
onboarding.

A third theme is the documentation lag - the carrier_reference field is live but
undocumented, which both a ticket and the roadmap call out.

Top issues: webhook signing, free-tier webhook drops, and the timezone-fix
confirmation request from the Western Australia carrier.

The files agree that webhook signing matters. An open question is whether GraphQL
will be versioned separately from REST.

Next actions: ship HMAC, reproduce the free-tier drop, document carrier_reference,
and confirm the timezone fix in writing.
