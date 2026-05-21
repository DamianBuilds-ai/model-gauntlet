# Data Pipeline / Aggregation Service Notes

Synthetic corpus doc 6 of 15. Engineering notes on the shared upstream the panels
depend on. This is the spine of the dependency graph.

## The aggregation service

Pulse does not query production databases directly (ruled out on load grounds, see
doc 02). Instead a new aggregation service rolls up seat and API data nightly into a
read-optimised store that Pulse panels query. This service is the shared upstream
dependency for BOTH the Seat Usage panel (doc 02) and the API Volume panel (doc 03).

If the aggregation service slips, both of those panels slip with it. It is the
highest-leverage item in the project.

## Status

Aggregation service core rollup: in progress, roughly 70 percent done. On track for
the freeze.

API endpoint-category tagging (the extra step the API Volume panel needs, doc 03):
NOT started. This is the long pole. Owner is Marcus's team but unassigned to a
specific engineer as of writing - this is itself a risk (see doc 07 RISK-2).

## Auth note

Pulse access uses Northwind's existing SSO. A customer logs into Pulse with the same
single sign-on they already use for the main Northwind product - no separate Pulse
login. This was decided to avoid building a new auth surface. (Note: a later doc in
this set states the auth decision differently - the planning record genuinely
conflicts and a Consolidator must catch it.)

## Dependency summary (as eng sees it)

1. Aggregation core -> blocks Seat Usage panel + API Volume panel.
2. Endpoint-category tagging -> blocks the API Volume breakdown specifically.
3. Neither blocks the Billing panel (that has its own Zentro dependency, doc 11).
