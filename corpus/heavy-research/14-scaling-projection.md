# Scaling Projection - Three-Year Volume and Concurrency

Synthetic corpus doc 14 of 16. The data team's projection of how load grows, which
the platform must absorb. Synthetic numbers.

## Volume

- Today: ~1 TB of analytical data.
- Year 1: ~2 TB.
- Year 2: ~3.5 TB.
- Year 3: ~5+ TB (the ~5x growth referenced in doc 01).

The newer benchmark (doc 06) tested at 5 TB, which is why it is the more relevant
latency source for the year-3 picture; the older benchmark (doc 05) tested at 2 TB,
roughly today's scale, another reason to discount it for a three-year decision.

## Concurrency

- Today: ~15 concurrent dashboard users at peak.
- Year 3 projection: ~50 concurrent users at peak (matches the 50-user concurrency
  scenario in benchmark doc 06).

## Implication for the decision

The platform must hold interactive latency at 5 TB AND ~50 concurrent users by year
3. Per doc 06:
- Lumen holds p95 under that concurrency via autoscaling, no ops effort.
- Strato can match it ONLY with manual cluster tuning - recurring ops load the small
  team cannot easily absorb (docs 07, 08).
- Beacon degrades most under exactly this concurrency, the heaviest-use scenario for
  the business (doc 13).

The scaling trajectory makes the year-3 concurrency picture the decisive performance
lens, not the single-query speed the stale benchmark (doc 05) emphasised.
