---
task_category: security-surface-enumeration
prompt_under_test: |
  You are given a single corpus file at
  corpus/security-surface-enumeration/codebase.md - a snapshot of a fictional
  ingestion service ("IngestService") with roughly 20 pseudo-Python modules.

  The security-relevant SINK is `runQuery(sql)` in module Dbgate, which executes
  raw SQL by string interpolation (a SQL-injection sink).

  Your task: enumerate EVERY untrusted (attacker-controlled) input that can reach
  runQuery(). For each, give the full taint path from the entry point to the sink.
  Be complete - a missed taint path is the failure this task measures.

  Output a numbered list. For each reachable input: the entry point, the full call
  path to runQuery(), and the variable that carries the taint into the SQL string.
  Do NOT list inputs that cannot reach the sink. Append the output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines after the list.
  No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/security-surface-enumeration/
corpus_intent: |
  One corpus file (corpus/security-surface-enumeration/codebase.md): ~20 fictional
  pseudo-Python modules for an ingestion service. The sink is Dbgate/runQuery, which
  executes string-interpolated SQL. The eval measures whether a run enumerates the
  COMPLETE set of attacker-controlled inputs that reach the sink, including one
  buried path where the taint arrives via a DESERIALIZED config field rather than a
  direct query parameter.

  QUALITY PRINCIPLE (completeness-first): the two direct interpolation paths are
  obvious; the scored signal is whether a run catches the buried config-field path.
  A run that lists the search and report paths but misses the partition_key path has
  found the shallow surface and dropped the dangerous one. Listing inputs that cannot
  reach runQuery (auth tokens, log messages, metrics names) is a precision error.

  ANSWER KEY (for the scoring Architect - the full enumerable list of inputs that
  reach the runQuery sink):

    DIRECT TAINT PATHS (obvious, one interpolation hop):
      T1. request.query["q"] (the /search query param). Path:
          httpHandler.handle -> Router.route("/search") ->
          Search.searchRecords(q) -> runQuery("... WHERE name = '" + q + "'").
      T2. request.query["range"] (the /report range param). Path:
          httpHandler.handle -> Router.route("/report") ->
          Report.buildReport(date_range) ->
          runQuery("... BETWEEN " + date_range).

    BURIED TAINT PATH (the discriminator - taint via a deserialized config field,
    no direct query param named partition_key anywhere):
      T3. request.body.config.partition_key (the /ingest body's config object).
          Path: httpHandler.handle -> Router.route("/ingest") ->
          Ingest.ingestBatch(body) -> ConfigMapper.mapConfig(body["config"])
          carries raw["partition_key"] into settings["partition_key"] UNSANITIZED
          -> Persist.persist(rows, settings) interpolates
          settings["partition_key"] into the table name -> runQuery("INSERT INTO "
          + table + ...). THIS is the buried item - it arrives by deserializing the
          attacker's JSON config and copying a field through a settings map, so a
          param-only or grep-for-query audit will miss it.

    NOT REACHABLE (precision traps - listing these as taint paths is a false
    positive): Authz.checkToken (authorization header - never reaches runQuery),
    Logger.log, Metrics.emit, Cache.cacheGet, Validator.validateRows,
    Compressor.compress, Scheduler.schedule, Notifier.notify, HealthZ.health,
    RateGate.limit, Settings.defaults (static), Serializer.toJson (output only).
    None of these flow into runQuery.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the run's output):
    - A correct run names "partition_key" AND "mapConfig" (or "config") AND
      "persist". grep -i "partition_key" MISSING means the buried config-field path
      was dropped - the primary scored signal.
    - A correct run names both direct paths: grep -i "searchRecords" (or the q
      param) AND "buildReport" (or the range param).
    - PRECISION: the output must NOT assert that checkToken / authorization header,
      Logger, Metrics, or Notifier reach runQuery. grep -i "checkToken\|
      authorization\|notify" listed AS a taint-to-sink path is a false positive.

  Scoring guidance:
    - Buried-item catch (load-bearing) = did the run find the partition_key
      config-field taint path (T3)? The single highest-signal bit.
    - Completeness = T1, T2 present + T3 present.
    - Precision (hallucination-eligible) = no NOT-REACHABLE module asserted as a
      taint path.
    - Reasoning quality = the T3 path is correctly traced through mapConfig's
      unsanitized copy into the settings map and persist's table-name interpolation.
    Voice match does NOT apply.
notes: |
  Chat A consistency-battery extension, eval 62 of 61-70. variant_pool 15 (3 models
  x N=5). THE SCORED SIGNAL IS WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate - NOT peak score. The question is whether one model family
  reliably catches the buried config-field taint path (T3, the partition_key arriving
  via a deserialized JSON config) on ALL 5 runs, or whether some runs in a family
  drop it. Low spread with 5/5 catch beats high variance with a stronger single run.

  The corpus (corpus/security-surface-enumeration/codebase.md) plants two obvious
  direct SQL-interpolation paths (the /search q param and /report range param) as the
  shallow surface, and ONE buried path: an /ingest request body whose deserialized
  config object carries a partition_key field, copied unsanitized through a settings
  map and interpolated into a table name at the sink. There is no direct query
  parameter named partition_key, so a parameter-only or grep-for-query audit misses
  it. Precision traps (auth tokens, logging, metrics, notifications) catch runs that
  pad the list with unreachable inputs. Standard four-phase /eval-pit flow against the
  frozen rubric/rubric.md. The corpus is the directory
  corpus/security-surface-enumeration/.
---

# Spec 62 - security-surface-enumeration

Given a fictional ~20-module ingestion service and a known SQL-injection sink
(`Dbgate/runQuery`, raw string-interpolated SQL), enumerate EVERY attacker-controlled
input that can reach the sink, with the full taint path for each.

This is a Chat A consistency-battery eval (variant_pool 15, N=5). The scored signal
is WITHIN-FAMILY SPREAD across the five runs plus per-model buried-item catch-rate,
not peak score. The discriminator is one buried taint path:
`request.body.config.partition_key` is deserialized from the /ingest request body's
config object, copied unsanitized through `ConfigMapper.mapConfig` into a settings
map, then interpolated into a table name by `Persist.persist` before hitting
`runQuery`. Because no direct query parameter named partition_key exists, a
parameter-only or grep-for-query audit drops it.

The two direct interpolation paths (the /search `q` param and the /report `range`
param) are the shallow surface every run should catch; finding them is necessary but
not sufficient. The corpus also plants precision traps - inputs that look
security-relevant (auth tokens, log messages, metrics, notifications) but never flow
into runQuery; asserting them as taint paths is a false positive. Standard four-phase
`/eval-pit` flow against the frozen `rubric/rubric.md`. The answer key in
`corpus_intent` lists every true path plus grep-verifiable invariants. Voice match
does not apply. The corpus is the directory `corpus/security-surface-enumeration/`.
