---
task_category: adr-authoring
prompt_under_test: |
  You are given one file, corpus/adr-authoring/decision-thread.md - the raw transcript
  of a team discussion for a fictional project ("Hollowmere"). Author an Architecture
  Decision Record (ADR) capturing the decision that was MADE in that thread.

  Use EXACTLY this ADR structure, in this order:

    # ADR - <short title of the decision>
    ## Status
    ## Context
    ## Decision
    ## Alternatives considered
    ## Consequences

  Rules:
    1. Capture ONLY the decision that was actually MADE and LOCKED in the thread. The
       thread also raises other topics that were explicitly DEFERRED or left open - do
       NOT author decisions for those. They do not belong in this ADR (mention them at
       most as out-of-scope/parked, never as decided).
    2. "## Alternatives considered" must list every option that was weighed for THIS
       decision, with the reason each was accepted or rejected.
    3. "## Consequences" must capture both the positive and the negative/cost
       consequences the thread surfaced for the chosen option.
    4. Do NOT invent any option, trade-off, or consequence the thread does not state.
    5. "## Status" should read "Accepted" (the decision was locked).

  Output the ADR as markdown, then the output envelope (schemaVersion, tier, status,
  tool_budget_used) on separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/adr-authoring/
corpus_intent: |
  One file (decision-thread.md): a messy two-part discussion for the fictional
  Hollowmere project (codename hygiene mandatory; no real domain names). Part one reaches
  ONE locked decision (render-cache storage). Part two raises two MORE topics (ingest
  concurrency bump; metrics backend choice) that are explicitly PARKED / "not today".
  Mirrors a typical personal-ops ADR-authoring step. The eval probes: capture the made decision
  with its alternatives and consequences, and resist scope creep into the parked topics.

  QUALITY PRINCIPLE (correctness-first): the load-bearing discriminator is SCOPE. An ADR
  that also "decides" the concurrency bump or the metrics backend - topics the thread
  explicitly deferred - is a confidently-wrong artifact: it records decisions that were
  never made. That is worse than an ADR that omits a minor consequence. Inventing an
  alternative or a trade-off the thread did not state is equally penalised.

  ANSWER KEY (the exact decision + its parts):

    THE ONE DECISION MADE: the render-cache moves to a SHARED REDIS instance, treated as
    a BEST-EFFORT accelerator (never on the critical path), with FALL-THROUGH to a live
    render on a cache miss OR a Redis outage. Status = Accepted/Locked.

    CONTEXT (from the thread): the render-cache is currently in-process; every deploy
    restarts the workers and cold-starts the cache, making the first post-deploy
    requests slow; support flagged this twice this month.

    ALTERNATIVES CONSIDERED (all three MUST appear, each with its accept/reject reason):
      A. Keep in-process (status quo) - REJECTED: simplest / zero new infra, but every
         deploy cold-starts the cache and post-deploy requests are slow.
      B. Shared Redis - CHOSEN: survives deploys, shared across workers; costs a 1-2ms
         network hop per read and a new operational dependency (monitoring + backup).
         The 1-2ms hop is negligible vs a ~200ms render miss.
      C. Local on-disk cache per worker - REJECTED: survives deploys and no network hop,
         but each worker has its own copy so the shared hit ratio drops (defeats the
         point of the cache) and disk eviction is fiddly.

    CONSEQUENCES (both signs, MUST appear):
      Positive: cache survives deploys (no more cold-start pain); shared hit ratio kept;
        Redis never on the critical path so an outage degrades gracefully to live render.
      Negative/cost: a 1-2ms network hop per cache read; a NEW operational dependency
        (Redis) that must be monitored and backed up.

    OUT OF SCOPE (must NOT be authored as decisions):
      - Ingest concurrency 4 -> 8: explicitly PARKED for next sprint (needs a Postgres
        max_connections change + load test first). PRIMARY SCOPE-CREEP TRAP.
      - Metrics backend (Prometheus vs hosted): explicitly "a whole separate discussion,
        not today". SECONDARY SCOPE-CREEP TRAP.

  GREP-VERIFIABLE INVARIANTS (for the scoring Architect):
    - "## Status" section reads "Accepted".
    - "Redis" appears in the "## Decision" section as the chosen storage.
    - "best-effort" / "fall-through" / "live render" appears (the never-on-critical-path
      design point is captured).
    - "## Alternatives considered" names all THREE options: in-process, Redis, on-disk
      (or per-worker disk). Each has an accept/reject reason.
    - "## Consequences" contains BOTH the 1-2ms hop / new dependency (negative) AND the
      survives-deploys / kept-hit-ratio (positive).
    - "concurrency" / "max_connections" does NOT appear as a DECISION; if mentioned at
      all it is flagged parked/out-of-scope. (Primary scope-creep trap.)
    - "Prometheus" / "metrics backend" does NOT appear as a DECISION; flagged
      out-of-scope at most. (Secondary scope-creep trap.)
    - No invented alternative or consequence (e.g. a 4th option, an unstated cost).

  Scoring guidance:
    - Correctness (hard-fail eligible) = the Redis best-effort-with-fall-through decision
      is captured accurately; the parked topics are NOT recorded as decisions.
    - Completeness = all three alternatives with reasons + both-sign consequences present.
    - Hallucination (hard-fail eligible) = inventing an option/trade-off, or authoring a
      decision for a parked topic.
    - Discipline = exact ADR section structure, in order; no scope creep.
    - Format adherence = markdown ADR + envelope outside.
    - Voice match does NOT apply.
notes: |
  CHAT C domain-realistic personal-ops eval. Mirrors a typical personal-ops ADR-authoring step
  on the fictional Hollowmere project (codename hygiene mandatory). Probes capturing the
  ONE locked decision (render-cache to shared Redis, best-effort, fall-through to live
  render) with all three weighed alternatives and both-sign consequences, while
  RESISTING scope creep into the two topics the thread explicitly parked (ingest
  concurrency bump; metrics backend). The load-bearing discriminator is scope: an ADR
  that records a parked topic as decided is confidently-wrong. Correctness and
  Hallucination are hard-fail eligible. The answer key gives the exact decision parts
  and grep invariants. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. variant_pool 9 (3 models x N=3, effort inert). Corpus is the
  directory corpus/adr-authoring/.
---

# Spec 84 - adr-authoring

Given the raw transcript of a team decision discussion (decision-thread.md), author an
Architecture Decision Record that captures the one decision actually made, with its
alternatives and consequences, and resists scope creep into the topics the thread
explicitly parked. This mirrors a typical personal-ops ADR step on the neutral fictional
Hollowmere project so no real codename leaks.

The thread reaches exactly one locked decision: the render-cache moves to a shared Redis
instance, treated as a best-effort accelerator that is never on the critical path, with
fall-through to a live render on a cache miss or a Redis outage. Three options were
weighed (in-process status quo, shared Redis, per-worker on-disk cache) each with a
stated reason, and both positive and cost consequences surfaced (survives deploys and
keeps the shared hit ratio, versus a 1-2ms network hop and a new operational
dependency to monitor and back up).

The load-bearing discriminator is scope. After the render-cache decision is locked, the
thread raises two more topics - bumping ingest concurrency from 4 to 8, and choosing a
metrics backend - and both are explicitly deferred ("park it for next sprint", "a whole
separate discussion, not today"). A correct ADR records neither as a decision. A model
that "helpfully" decides the parked topics produces a confidently-wrong artifact that
claims decisions were made when they were not. The correctness-first principle holds:
inventing an option, a trade-off, or a decision is worse than omitting a minor detail.

Correctness and Hallucination are hard-fail eligible; Discipline covers the exact ADR
section order and the no-scope-creep requirement. The answer key in corpus_intent gives
the exact decision, its alternatives, its consequences, and grep-verifiable invariants
for the scoring Architect. Voice match does not apply. Standard four-phase /eval-pit
flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
inert per the methodology). The corpus is the directory corpus/adr-authoring/.
