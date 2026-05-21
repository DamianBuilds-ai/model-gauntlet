# Three-Year Cost Analysis

Synthetic corpus doc 7 of 16. An internal finance-built model of three-year total
cost of ownership for each platform at Riverbend's projected growth (5x volume).
Numbers are illustrative and synthetic.

## Modelling assumptions

- Data volume grows ~5x over three years (per doc 01).
- Total cost of ownership = license + infrastructure + PEOPLE (ops time costed at a
  blended engineer rate). People cost is where self-managed options get expensive.

## Three-year TCO (illustrative, relative)

- **Lumen Cloud:** highest raw platform spend (consumption pricing scales with the 5x
  volume growth and gets steep in years 2 to 3) but NEAR-ZERO added people cost (no
  ops). Net three-year TCO: medium-high.
- **Strato DB:** lowest platform spend (no license, just infrastructure) BUT the
  highest people cost - it needs meaningful ops time to run, tune, and keep available
  (doc 08 quantifies this). For a 3-engineer team that ops load is disproportionately
  expensive and risky. Net three-year TCO: medium, but with the LARGEST hidden people
  cost and the most variance.
- **Beacon Analytics:** predictable flat pricing, no separate BI tool to buy (a real
  saving), low ops. Net three-year TCO: lowest and most predictable of the three -
  BUT remember the latency limitation (doc 06) is the reason it is cheap-to-run, not
  a free lunch.

## The trap to avoid

The Lumen one-pager (doc 02) says "pay only for what you use," which SOUNDS cheap. At
5x volume growth the consumption model is NOT cheap by year three. Do not conclude
"managed = expensive, self-managed = cheap" - once people cost is included, Strato's
apparent cheapness erodes substantially. The honest framing: Lumen trades higher
platform spend for zero ops; Strato trades low platform spend for high, risky ops
load; Beacon is cheapest but slowest.
