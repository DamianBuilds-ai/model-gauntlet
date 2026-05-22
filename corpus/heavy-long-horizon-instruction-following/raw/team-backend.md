# Backend team - raw changelog for v9.0

Backend entries. We tend to write longer explanations because the changes are
load-bearing. Dates in our own format. We mark beta features explicitly.

## Shipped

- BE-12: Cardinal Query Planner. This is the big one. We replaced the old
  rule-based query planner with a cost-based planner that estimates row counts
  from table statistics and picks join orders accordingly. On the benchmark suite
  it cuts p95 query latency by roughly forty percent. New feature. Landed May 3rd.

- BE-77: Streaming export (beta). You can now stream large result sets as
  newline-delimited JSON instead of buffering the whole result. It is behind a
  beta flag and the response shape may change. Tag it beta. Shipped April 30th.

- BE-340: Connection pooling rewrite. The pool now scales connections per-tenant
  with a fair-share limiter so one noisy tenant cannot starve the pool. This is an
  improvement to existing behavior. May 1st.

- BE-1001: New `cardinal export --format parquet` CLI flag. You can export query
  results directly to Parquet from the CLI now. New feature. April 29th.

- BE-58: Deprecated the v1 query API (`/api/v1/query`). It still works in v9.0 but
  is deprecated and will be REMOVED in v10.0. Migrate to `/api/v2/query`. This is
  a deprecation. Announced May 2nd.

- BE-59: Deprecated the legacy `cardinal-cli` binary in favour of the new
  `cardinal` binary. The old binary is deprecated now and will be REMOVED in
  v9.4. Deprecation. May 2nd.

- BE-410: The `/api/v2/query` endpoint now requires a `tenant_id` field in the
  request body where it was previously optional. This is a breaking change for any
  client that omitted it. Also as part of the same ticket we ADDED a new
  `explain=true` query parameter that returns the query plan as JSON - that part
  is a new feature. So BE-410 is both a breaking change (mandatory `tenant_id`)
  and a feature (the `explain` parameter). Landed May 1st.

- BE-205: Improved error messages on query timeouts. The timeout error now names
  the slowest stage of the plan. Improvement. April 28th.

- BE-900: Reduced cold-start time for the query engine by precompiling the plan
  cache. Improvement. April 27th.

## Internal

- BE-1300: internal-only - migrated the internal metrics pipeline to the new
  telemetry bus. Not public-facing, do not include.

- BE-1301: internal-only - refactored the test harness. Not public.

## Untriaged

- Bumped the default statement timeout from 30s to 45s. We have not filed a ticket
  for this yet but it shipped. No ticket id.

## Notes on dates

We slipped twice; the final ship date shows as "May 3rd" here and "3 May" in the
platform changelog, same day. We write "behavior" and "optimize" American-style.
The deprecation removal versions (v10.0 for the v1 query API, v9.4 for the old
CLI) are firm - support needs those exact versions in the notes.
