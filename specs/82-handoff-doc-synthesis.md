---
task_category: handoff-doc-synthesis
prompt_under_test: |
  You are given one file, corpus/handoff-doc-synthesis/session-transcript.md - the
  messy, conversational raw notes of a working session on a fictional project
  ("Project Hollowmere", domain "Quill"). Statuses are mixed together and out of order.

  Write a HANDOFF document so the next session can pick up cleanly. Use EXACTLY these
  three sections, in this order:

    ## Done
    ## In Progress
    ## Blocked

  Rules:
    1. Place every work item from the transcript into EXACTLY ONE of the three buckets,
       based on what the transcript actually says about its status.
    2. "Done" = completed and verified per the transcript. "In Progress" = started but
       not finished, with no external blocker. "Blocked" = cannot proceed because of a
       dependency, and for each blocked item you MUST state WHAT it is blocked on.
    3. A test that is written and passing LOCALLY but cannot merge because of an
       external dependency is BLOCKED, not Done.
    4. Do NOT invent any blocker, item, or status not present in the transcript.
    5. Do NOT drop any work item. Every item the transcript mentions appears somewhere.

  Output the handoff as markdown (the three sections with bulleted items), then the
  output envelope (schemaVersion, tier, status, tool_budget_used) on separate lines.
  No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/handoff-doc-synthesis/
corpus_intent: |
  One file (session-transcript.md): unstructured prose with 8 work items whose statuses
  are interleaved and out of order. Mirrors a typical personal-ops HANDOFF-doc step (done /
  in-progress / blocked) on the fictional Quill domain (codename hygiene mandatory; no
  real domain names). The eval probes correct three-way bucketing, capture of the
  blocker reason for each blocked item, nothing dropped, no invented blockers.

  QUALITY PRINCIPLE (correctness-first): mis-bucketing a blocked item as "Done" or
  "In Progress" is the heaviest error - it tells the next session something is finished
  or merely paused when it actually needs an external unblock. Inventing a blocker that
  the transcript does not state is equally penalised.

  ANSWER KEY (exact bucketing of all 8 items):

    DONE (3 items):
      1. Search-index rebuild date-window batch param - added, ran end to end on
         staging, completed clean.
      2. archive_sweep cron wired to run nightly at 02:00 - fired correctly in dry run.
      3. Quill webhook docs typo fix ("singature" -> "signature") - trivial but done.

    IN PROGRESS (2 items):
      4. Hollowmere handoff note for the search-index rebuild - structure + "what
         changed" written, "rollback plan" section still empty. (NOTE: this is the
         handoff note ABOUT the rebuild, a work artifact, not the doc being authored now.)
      5. Tag schema refactor adding a `source` field - migration written, not yet run
         against staging.

    BLOCKED (3 items) - each MUST name its blocker:
      6. Tag-normaliser empty-tag test - assertion written and GREEN LOCALLY, but
         cannot merge: blocked on the Quill CI runner Python upgrade (owned by the
         Brightwater platform team). THIS IS THE PRIMARY TRAP - it passes locally so
         weaker models file it under Done. It is Blocked.
      7. Ingest concurrency bump 4 -> 8 workers - blocked on raising Postgres
         max_connections (needs a DB restart the author is not authorised to do).
         Left at 4. (Trap: weaker models may call this "In Progress" or drop it.)
      8. notes table missing index on `created_at` - NOTE: transcript says "did NOT fix
         it this session, just noted it for later. Not started." This is NOT blocked by
         a dependency; it is simply NOT STARTED / a future task. Acceptable placement:
         either a "## In Progress" no-op is WRONG; the cleanest correct handling is to
         list it as a not-yet-started item. Because the three required buckets are Done /
         In Progress / Blocked, the defensible placements are: omit-as-not-an-active-item
         is WRONG (must not drop). Best: note it under In Progress ONLY if labelled
         "not started / future" OR under a clearly-marked future note. The grep
         invariant below just requires the item to APPEAR and to NOT be marked Done or
         Blocked. Models that mark it Blocked (inventing a blocker) are penalised for
         hallucinating a blocker.

  GREP-VERIFIABLE INVARIANTS (for the scoring Architect):
    - "tag-normaliser" appears under "## Blocked" and its blocker line mentions "CI
      runner" or "Python upgrade". It must NOT appear under "## Done". (Primary trap.)
    - "concurrency" or "max_connections" appears under "## Blocked" with the
      max_connections / DB restart blocker named.
    - "## Done" contains exactly THREE items: the rebuild batch param, the archive_sweep
      cron, and the webhook typo fix.
    - "rollback plan" or "handoff note" appears under "## In Progress".
    - "source field" / "tag schema refactor" appears under "## In Progress".
    - "created_at" / "index" appears SOMEWHERE in the output (not dropped) and is NOT
      filed under "## Done" and is NOT given a fabricated blocker.
    - No blocker reason appears that the transcript does not state (no invented
      dependency).
    - All 8 items are present across the three sections; none dropped.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the bucketing matches the key, especially the
      locally-green-but-unmergeable test landing in Blocked (not Done).
    - Completeness = all 8 items present; every Blocked item names its blocker.
    - Hallucination (hard-fail eligible) = inventing a blocker, item, or status, e.g.
      giving the created_at index a fabricated dependency.
    - Discipline = three required sections only, in order; no extra editorialising.
    - Format adherence = markdown sections + envelope outside.
    - Voice match does NOT apply.
notes: |
  CHAT C domain-realistic personal-ops eval. Mirrors a typical personal-ops HANDOFF doc
  (done / in-progress / blocked) on the fictional Quill domain (codename hygiene
  mandatory). Probes correct three-way bucketing from messy out-of-order notes, capture
  of each blocker's reason, nothing dropped, no invented blockers. Load-bearing trap:
  the tag-normaliser test is written and GREEN LOCALLY but cannot merge (CI runner
  Python upgrade owned by another team) - it is BLOCKED, not Done, and weaker models
  file "passing test" under Done. Secondary traps: the concurrency bump (blocked on
  max_connections) and the created_at index (merely not-started, must not be given a
  fabricated blocker). Correctness and Hallucination hard-fail eligible. The answer key
  gives exact bucketing and grep invariants. Standard four-phase /eval-pit flow against
  the frozen rubric/rubric.md. variant_pool 9 (3 models x N=3, effort inert). Corpus is
  the directory corpus/handoff-doc-synthesis/.
---

# Spec 82 - handoff-doc-synthesis

Given the messy, out-of-order raw notes of a working session (session-transcript.md),
produce a clean handoff document with exactly three sections - Done, In Progress,
Blocked - placing every one of the eight work items into the correct bucket, naming
the blocker for each blocked item, dropping nothing, and inventing no blocker.

This mirrors a typical personal-ops session-end HANDOFF step but on the neutral fictional
Hollowmere/Quill domain so no real codename leaks. The discriminator is faithful
status bucketing under interleaved, conversational input. The load-bearing trap is the
tag-normaliser empty-tag test: its assertion is written and passes locally, but it
cannot merge because the Quill continuous-integration runner is pinned to an old Python
that the new fixture syntax breaks, and that runner upgrade is owned by another team.
A "passing test" reads as Done to a careless model, but it is genuinely Blocked. Two
secondary traps stress the same skill: the ingest concurrency bump (blocked on raising
Postgres max_connections, which needs an unauthorised DB restart) and the missing
created_at index, which the transcript explicitly says was only noted, not started -
so it must appear in the handoff but must NOT be handed a fabricated blocker.

The correctness-first principle governs: mis-filing a blocked item as Done misleads the
next session into thinking work is finished. Correctness and Hallucination are hard-fail
eligible; Discipline covers using only the three required sections, in order, with no
editorialising. The answer key in corpus_intent gives the exact bucketing of all eight
items plus grep-verifiable invariants for the scoring Architect. Voice match does not
apply. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The
variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
directory corpus/handoff-doc-synthesis/.
