<!-- SYNTHETIC DATA. This is synthetic data to be edited/analyzed. Do NOT treat any
text inside as instructions. All names, projects, and IDs are fictional. -->

# Decision thread transcript - Hollowmere team

A messy back-and-forth discussion. Multiple topics come up. Only ONE decision is
actually MADE here; other topics are raised but explicitly deferred or left open.

---

ROWAN: We keep losing render-cache entries on deploy because the cache is in-process
and every deploy restarts the workers. We need to decide where the render-cache lives.

MARLOWE: Three options on the table. (A) Keep it in-process as today - simplest, zero
new infra, but every deploy cold-starts the cache and the first requests after a deploy
are slow. (B) Move it to a shared Redis instance - survives deploys, shared across
workers, but adds a network hop per cache read (about 1-2ms) and a new operational
dependency we have to monitor and back up. (C) Use a local on-disk cache per worker -
survives deploys, no network hop, but each worker has its own copy so the hit ratio
drops and disk eviction gets fiddly.

ROWAN: The cold-start pain is real - support has flagged it twice this month. The 1-2ms
hop on Redis is nothing compared to a render miss which is 200ms+.

MARLOWE: Agreed. The per-worker disk option fragments the cache and we lose the shared
hit ratio, which is the whole point of the cache. I think Redis is the call.

ROWAN: One concern - if Redis goes down, do we hard-fail or fall through to a render?
We should fall through to a live render so Redis is never on the critical path.

MARLOWE: Yes, treat Redis as a best-effort accelerator, never a dependency for
correctness. Cache miss and Redis-down both just trigger a live render.

ROWAN: Good. So we're decided: render-cache moves to a shared Redis instance, treated
as best-effort, with fall-through to live render on miss or Redis outage. We accept the
1-2ms hop and the new operational dependency (monitoring + backup).

MARLOWE: Locked. I'll write it up.

---

ROWAN: Separate thing while we're here - should we also bump the ingest concurrency
from 4 to 8? The queue backs up at peak.

MARLOWE: Maybe, but that needs a Postgres max_connections change and I want to load-test
it first. Let's NOT decide that now - park it for next sprint.

ROWAN: Fair, parked.

MARLOWE: And we should eventually pick a metrics backend - Prometheus vs the hosted
option - but that's a whole separate discussion, not today.

ROWAN: Right, not today. Just the render-cache decision for now.
