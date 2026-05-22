# Helios Weekly Status - Week 1

Author: Devin (Program manager)
Status: published

## Headline

Build is on track against the September 15 GA target (charter doc 01). No date change
this week.

## Workstream status

- Dashboard builder (doc 02): on track. First-widget render is hitting the 2-second
  bar in dev.
- Connectors (doc 03): on track for the three GA connectors. Dependent on the
  aggregation service (doc 09).
- Billing surface (doc 04): BLOCKED on the pricing-model decision (per-seat vs
  usage-based, docs 26 vs 39) and on the Free-tier row-cap conflict (10,000 vs 25,000,
  docs 05 vs 26).
- Auth (docs 09 vs 15): the auth method is still contested (SSO vs magic-link). This
  is now blocking the security review (doc 20) from starting.

## Beta

We have 12 beta customers actively using Helios this week. (Note: the sales doc 31
reports 8 beta customers; the difference is the 4 that churned during beta - see the
research notes doc 07, interview 6. The active count and the original count are being
reported inconsistently across docs.)

## Risks

See the risk register (doc 12). The top risk remains the aggregation service as the
shared upstream blocking both the builder and the connectors.
