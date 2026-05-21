# Risk Register

Synthetic corpus doc 7 of 15. The running risk list. References other docs by RISK id.

| ID | Risk | Owner | Status |
|----|------|-------|--------|
| RISK-1 | Billing panel surfaces financial data; needs security sign-off before launch | Priya | open, gate not yet cleared |
| RISK-2 | API endpoint-category tagging not started and unassigned; long pole for the API Volume panel | Marcus | open, escalating |
| RISK-3 | CSV export demand from customers but it is out of v1 scope; expectation risk at launch | Sam | open, mitigation = GTM messaging |
| RISK-4 | Aggregation service is a single point of failure for two of three panels | Marcus | open, monitored |
| RISK-5 | Timeline is tight; projected month-end calc is the agreed first cut if we slip | Dana | accepted, contingency defined |

## Notes

- RISK-2 is the one most likely to actually move the launch date. The tagging work
  has no named engineer. Until it is assigned and scoped it is unestimable. This is
  the item the Consolidator should rank highest in next-actions.
- RISK-1 (security gate) is a hard launch blocker but is a known, well-understood
  process. It is on the critical path but not unestimable like RISK-2.
- RISK-4 is structural and accepted - there is no plan to remove the single point of
  failure for v1; it is just monitored closely.
- RISK-5 contingency: if anything slips, cut the projected month-end usage calc from
  the API Volume panel first (this matches the decision in doc 09). Do not cut a
  whole panel.
