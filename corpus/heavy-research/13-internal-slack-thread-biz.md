# Internal Slack Thread Capture - Business / Analytics Users Channel

Synthetic corpus doc 13 of 16. A capture of the business-side discussion. Different
priorities from engineering - they care about dashboards and predictability.

**@analytics-manager:** from the business side, what we care about is: dashboards
load fast for our 40-ish internal users, and the bill is predictable so I can budget.

**@finance:** predictable bill is a real plus for whatever option we pick. The
consumption model on Lumen worries me for budgeting (doc 07 says it gets steep at our
year-3 volume). Beacon's flat pricing is the easiest to forecast.

**@analytics-manager:** but Beacon is slower on the big interactive dashboards right?
that is literally our heaviest use case. If our 40 users hit a slow dashboard daily
that is a real productivity hit.

**@finance:** and compliance said Beacon has that EU BI-layer gap (doc 09). So
predictable-but-slow-and-non-compliant is not actually a win.

**@analytics-manager:** so the dream is managed + predictable-ISH + fast + EU-clean.
Lumen is fast (with the high-perf tier) and EU-clean with that documented metadata
caveat, but the bill is variable. That seems like the least-bad set of tradeoffs for
us honestly.

**@finance:** if we can model and cap the Lumen spend, I can live with variability for
the performance and compliance wins.

## Signal to extract

Business priorities (dashboard latency for ~40 concurrent users + budget
predictability + EU compliance) push toward Lumen once Beacon is ruled out on latency
AND the compliance gap. The one Lumen downside the business feels is bill variability,
which is a manageable concern, not a disqualifier.
