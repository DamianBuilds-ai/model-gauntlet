---
task_category: config-drift-detection
prompt_under_test: |
  You are given three configuration files for a fictional service called "Harbor",
  one per environment, in the directory corpus/config-drift-detection/:
    - harbor.dev.yaml
    - harbor.staging.yaml
    - harbor.prod.yaml

  Each file contains the same set of configuration keys (same structure, same key
  paths), but some VALUES differ between environments. Your task is CONFIGURATION
  DRIFT DETECTION.

  Produce a complete list of EVERY configuration key whose value drifts (differs)
  across the three environments. For each drifting key, give its full dotted key path
  (e.g. `server.max_connections`) and the value it holds in dev, staging, and prod.

  CRITICAL nuance: report a key as drifting if its EFFECTIVE value differs between any
  two environments. Two values that are written differently but mean exactly the same
  thing (for example a duration written as `30s` in one file and `30000ms` in another -
  these are the same 30 seconds) are NOT a real drift; if you list such a key you MUST
  explicitly note that the values are semantically equal and flag it as a textual /
  unit-formatting inconsistency, NOT a behavioural drift. Do not silently treat a
  unit-reformatted-but-equal value as a genuine value drift, and do not silently ignore
  it either - call it out as the special case it is.

  Some keys are intentionally identical across all three environments (host, port,
  timeouts that genuinely match, queue settings). Do NOT report keys that are identical
  across all three.

  Output a markdown table with columns: key path | dev | staging | prod | drift type
  (where drift type is "value drift" for a genuine behavioural difference, or
  "unit-formatting (semantically equal)" for the textual-only case). After the table,
  append the required output envelope (schemaVersion, tier, status, tool_budget_used)
  on separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/config-drift-detection/
corpus_intent: |
  Three fictional environment config files (corpus/config-drift-detection/
  harbor.dev.yaml, harbor.staging.yaml, harbor.prod.yaml), each ~30 keys across the
  same structure (service, server, database, cache, queue, logging, features, limits).
  Most keys drift in obvious, behaviourally-real ways (pool sizes, connection caps,
  rate limits, log levels). The buried discriminator is ONE key whose value is written
  differently in one file but means exactly the same thing - server.read_timeout is
  `30s` in dev and prod but `30000ms` in staging. 30 seconds == 30000 milliseconds, so
  this is a textual / unit-formatting inconsistency, NOT a behavioural value drift.

  THE BURIED ITEM (the scored discriminator): server.read_timeout. dev=30s,
  staging=30000ms, prod=30s. A weak model does one of two failing things: (a) silently
  reports it as a normal value drift (3 different-looking strings) without recognizing
  30s == 30000ms - a false categorization; or (b) sees the strings differ and either
  over-reports or, when "normalizing", silently drops it from the drift list entirely
  with no note. The correct behaviour is to surface read_timeout AND label it as a
  unit-formatting (semantically equal) inconsistency, not a genuine value drift. Catch
  rate on this single nuanced item across the 5 runs of a family is the load-bearing
  signal.

  QUALITY PRINCIPLE (correctness-first): completeness on the genuine drifts AND correct
  categorization of the one semantic-equal pair both matter. Missing a genuine drift is
  a recall miss; mis-categorizing read_timeout as a real value drift (or silently
  dropping it) is the high-signal failure. Inventing a drift on an identical key is a
  precision/hallucination error.

  ANSWER KEY (for the scoring Architect). The keys that GENUINELY DRIFT across the three
  environments (value differs and the difference is behaviourally real) are exactly
  these 14:

    1. service.tier            dev=dev        staging=staging   prod=prod
    2. server.max_connections  dev=256        staging=512       prod=1024
    3. database.host           dev=harbor-db-dev.internal  staging=harbor-db-staging.internal  prod=harbor-db-prod.internal
    4. database.pool_size      dev=10         staging=20        prod=40
    5. database.max_idle_conns dev=5          staging=5         prod=10   (dev==staging, prod differs - still a drift)
    6. database.ssl_mode       dev=disable    staging=require   prod=require
    7. cache.host              dev=harbor-cache-dev.internal  staging=harbor-cache-staging.internal  prod=harbor-cache-prod.internal
    8. cache.max_entries       dev=10000      staging=50000     prod=200000
    9. logging.level           dev=debug      staging=info      prod=warn
    10. logging.format         dev=text       staging=json      prod=json   (dev differs)
    11. logging.sample_rate    dev=1.0        staging=0.5       prod=0.1
    12. features.enable_audit_log  dev=false  staging=true      prod=true   (dev differs)
    13. limits.rate_limit_rps  dev=100        staging=500       prod=2000
    14. limits.burst           dev=200        staging=1000      prod=4000

  PLUS exactly ONE semantic-equal / unit-formatting case (must be surfaced AND labelled
  as NOT a behavioural drift):

    15. server.read_timeout    dev=30s        staging=30000ms   prod=30s    => 30s == 30000ms, unit-formatting only, NOT a value drift.

  Keys that are IDENTICAL across all three (must NOT be reported as drift): service.name,
  service.region, server.host, server.port, server.write_timeout, server.idle_timeout,
  server.graceful_shutdown, database.driver, database.port, database.conn_max_lifetime,
  database.statement_timeout, cache.backend, cache.port, cache.ttl, queue.* (all five),
  logging.destination, features.enable_batch_ingest, features.enable_metrics,
  features.enable_tracing, limits.max_payload_bytes.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output table lists `server.read_timeout` AND the row/note classifies it as
      semantically equal / unit-formatting, NOT a plain value drift. Grep the output for
      `read_timeout` co-occurring with one of: `semantically equal`, `unit`, `30s == 30000ms`,
      `same`, `equal`. If `read_timeout` is listed as a normal value drift with no equality
      note, the buried item is MISSED.
    - `30000ms` appears in the output exactly in the read_timeout row.
    - The output reports 14 genuine value drifts (the list above). Count of genuine-drift
      rows == 14 is full recall.
    - `server.max_connections` row shows 256 / 512 / 1024.
    - `database.ssl_mode` row shows disable / require / require.
    - `limits.rate_limit_rps` row shows 100 / 500 / 2000.
    - No row reports an identical-across-all-three key (e.g. `queue.prefetch`,
      `server.port`, `cache.ttl`) as a drift. Any such row is a false positive
      (precision error).

  Scoring guidance:
    - Correctness (hard-fail eligible) = the 14 genuine drifts identified with correct
      per-env values AND read_timeout correctly categorized as semantic-equal.
    - Completeness = all 14 genuine drifts present (recall).
    - Hallucination (hard-fail eligible) = reporting an identical-across-all key as a
      drift, or inventing a value not present in the files.
    - Discipline = correct categorization of the one semantic-equal pair; not silently
      dropping it and not mislabelling it as a value drift.
    - Voice match does NOT apply.
notes: |
  Chat A consistency battery (61-70). variant_pool 15 (3 models x N=5). The SCORED
  SIGNAL for this eval is WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate: did all 5 runs of a model family surface server.read_timeout
  AND correctly label it as semantically equal (30s == 30000ms, unit-formatting only),
  or did some runs gamble and either report it as a plain value drift or silently drop
  it. Peak score on a single run is not the question; consistency of catching the one
  nuanced item across 5 runs is.

  This is a config-drift-detection task: three fictional Harbor env files
  (corpus/config-drift-detection/) with ~30 keys each. 14 keys genuinely drift in
  behaviourally-real ways (pool sizes, rate limits, log levels, ssl modes). One key -
  server.read_timeout - is written 30s / 30000ms / 30s, which is the same duration in
  different units: the buried discriminator that separates models that reason about
  effective value from models that diff strings. Identical keys (queue.*, ports, ttl)
  are precision traps - reporting them is a false positive. Answer key gives the exact
  14-drift list plus the semantic-equal pair plus grep-verifiable invariants. Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. Codenames are neutral
  fictional (Harbor). Voice match does not apply.
---

# Spec 66 - config-drift-detection

Given three environment configuration files for a fictional service (dev, staging,
prod), each carrying the same ~30 keys, enumerate EVERY key whose effective value
drifts across the environments - and correctly distinguish a genuine behavioural drift
from a value that is merely written in a different unit but means exactly the same
thing.

The corpus (`corpus/config-drift-detection/harbor.{dev,staging,prod}.yaml`) plants 14
genuine drifts (max_connections 256/512/1024, pool_size 10/20/40, rate_limit_rps
100/500/2000, log levels debug/info/warn, ssl_mode disable/require/require, and so on).
Buried among them is ONE nuanced item: `server.read_timeout` reads `30s` in dev and
prod but `30000ms` in staging. Thirty seconds equals thirty thousand milliseconds, so
this is a unit-formatting inconsistency, NOT a behavioural drift. The correct answer
surfaces read_timeout AND labels it as semantically equal; the failure modes are
reporting it as a plain value drift (false categorization) or, when "normalizing",
silently dropping it (a recall hole with no note).

Identical-across-all-three keys (the queue block, ports, cache.ttl, idle timeouts) are
precision traps - reporting any of them as a drift is a false positive.

This is a Chat A consistency-battery eval. Standard four-phase `/eval-pit` flow against
the frozen `rubric/rubric.md`. The scored signal is within-family SPREAD across the 5
runs plus per-model catch-rate on the single buried semantic-equal item, not peak score
on one lucky run. The variant pool is 15 (3 models x N=5, effort inert per the
methodology). The answer key in `corpus_intent` gives the exact 14-drift list, the one
semantic-equal pair, the identical-key exclusion set, and grep-verifiable invariants for
the scoring Architect. Codenames are neutral fictional (Harbor). Voice match does not
apply.
