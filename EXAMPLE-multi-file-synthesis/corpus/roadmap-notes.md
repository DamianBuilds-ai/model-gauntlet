# Acme Logistics - Quarterly Roadmap Notes

Source file 3 of 3. Synthetic data for the multi-file-synthesis example eval.

## Committed this quarter
- Ship signed webhooks (HMAC). Security has flagged unsigned payloads as the top
  open risk. Target: v3.3.0.
- Publish the GraphQL read API as a public beta. REST stays the supported default.

## Under consideration (not committed)
- A free-tier webhook volume cap, made explicit in docs, to stop silent drops.
  Trade-off: may push small customers to paid earlier than we want.
- Separate versioning for the GraphQL schema. No decision yet.

## Known debt
- The public API reference trails the actual API by about one minor version. The
  `carrier_reference` field is the current example of an undocumented-but-live field.
- Webhook reliability has no published SLA. Support keeps fielding "is it down"
  tickets that are actually volume-cap drops.

## Stakeholder asks
- Sales wants the batch endpoint promoted in onboarding - several churned trials
  cited throughput limits.
- Support wants the timezone fix from v3.1.4 communicated to affected accounts in
  writing, not just shipped silently.
