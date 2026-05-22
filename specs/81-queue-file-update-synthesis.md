---
task_category: queue-file-update-synthesis
prompt_under_test: |
  You are given two files in corpus/queue-file-update-synthesis/:

    - QUILL_QUEUE.md - the current active-work queue for a fictional domain "Quill".
      It has a "## This Session" task list (some items checked, some not), and a
      "## Recently Completed" list.
    - session-summary.md - unstructured raw notes describing what actually happened
      in the session that just ended, in the order it happened.

  Update QUILL_QUEUE.md to reflect the session outcome. Apply these rules exactly:

    1. For every "## This Session" task that the summary says is DONE, check it off
       (change `- [ ]` to `- [x]`) and MOVE it into "## Recently Completed".
    2. Leave any task the summary says is still in-progress or untouched in
       "## This Session" as `- [ ]` (do NOT check it off).
    3. Add any NEW task that surfaced during the session (mentioned in the summary
       but NOT already in the queue) to "## This Session" as an unchecked item.
    4. QUEUE RULE: if "## Recently Completed" would end up with 5 or more items after
       you add the newly-done ones, ROTATE the OLDEST completed items out so that
       exactly 5 remain (keep the 5 most recent; the rotated-out items are removed
       from this file - assume they go to a separate log). The session's freshly-done
       items are the most recent and stay; drop the oldest pre-existing ones.
    5. Do NOT fabricate any task, status, or completion that the summary does not
       support. If the summary is silent about a task, its status does not change.

  Output the COMPLETE updated QUILL_QUEUE.md content as a single fenced code block,
  then the output envelope (schemaVersion, tier, status, tool_budget_used) as separate
  lines OUTSIDE the code block. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/queue-file-update-synthesis/
corpus_intent: |
  Two files. QUILL_QUEUE.md (6 "This Session" tasks, all unchecked; 4 "Recently
  Completed" items). session-summary.md (unstructured prose describing what happened).
  This mirrors a typical personal-ops session-end QUEUE update but on the fictional "Quill"
  domain (codename-hygiene mandatory; no real domain names appear). The eval probes
  faithful synthesis: correctly bucket what got done vs not, surface the new task,
  apply the 5-item rotation rule, and fabricate nothing.

  QUALITY PRINCIPLE (correctness-first): a queue that LOOKS tidy but checks off a task
  the summary did not finish (the tag-normaliser test), or invents a completion, is
  WORSE than one that honestly leaves an ambiguous item unchecked. Over-claiming done
  status is the heaviest penalty.

  ANSWER KEY (exact expected end-state of QUILL_QUEUE.md):

    From the summary, these mappings are the truth:
    - "ingest retry backoff caps at 30s" = DONE (matches queue item 1).
    - "archive_sweep cron nightly 02:00" = NOT done (summary: "did NOT get to ... untouched").
    - "tag-normaliser empty-tag test" = NOT done (summary: only scaffold, assertion
      not written, "still in progress, not done"). MUST stay unchecked. This is the
      primary trap - weaker models check it off because a test was "started".
    - "Brightwater migration runbook new column order" = DONE (matches queue item 4).
    - "Hollowmere handoff note for search-index rebuild" = NOT done (summary: "still pending").
    - "duplicate-row warning in the notes table" = DONE (summary: added unique
      constraint, backfilled, warning gone) - matches queue item 6.
    - NEW task surfaced: "add a date-window batch param to the search-index rebuild
      script" (timed out on pre-2023 archives) - was NOT in the queue, MUST be added
      to "## This Session" as unchecked.

    Therefore "## This Session" AFTER must contain exactly THREE unchecked items:
      - [ ] Add a `tag-normaliser` unit test for the empty-tag case
      - [ ] Wire the `archive_sweep` cron to run nightly at 02:00
      - [ ] Draft the Hollowmere handoff note for the search-index rebuild
      - [ ] Add a date-window batch param to the search-index rebuild script (NEW)
    (i.e. FOUR items total: the three carried-over not-done items PLUS the one new item.
    The exact wording of items may vary slightly; the SET of four concepts is the key.)

    The three freshly-DONE items move to "## Recently Completed":
      - [x] Fix the ingest retry backoff so it caps at 30s
      - [x] Update the Brightwater migration runbook with the new column order
      - [x] Investigate the duplicate-row warning in the notes table (fixed via unique constraint)

    "## Recently Completed" had 4 pre-existing items + 3 new = 7. ROTATION RULE caps at
    5: keep the 5 MOST RECENT. The 3 freshly-done are most recent and stay. Of the 4
    pre-existing, keep the 2 most recent (listed last in the original = "Document the
    Quill webhook signature format" and "Patch the timezone bug in archive_sweep
    timestamps") and DROP the 2 oldest ("Rename legacy_ingest() to ingest_v2()" and
    "Add the confidence field to the tag schema"). Final Recently Completed = exactly
    5 items.

  GREP-VERIFIABLE INVARIANTS (for the scoring Architect):
    - The string "tag-normaliser" appears in "## This Session" as `- [ ]` (UNCHECKED).
      It must NOT appear under "## Recently Completed". (Primary trap.)
    - "archive_sweep cron" / "02:00" appears unchecked in This Session.
    - "Hollowmere handoff" appears unchecked in This Session.
    - "date-window" or "batch param" appears as a NEW unchecked item in This Session
      (recall of the surfaced task).
    - "ingest retry backoff" appears as `- [x]` under Recently Completed.
    - "Brightwater migration runbook" appears as `- [x]` under Recently Completed.
    - "duplicate-row" or "unique constraint" appears as `- [x]` under Recently Completed.
    - "## Recently Completed" contains EXACTLY 5 `- [x]` items.
    - "legacy_ingest" / "ingest_v2" does NOT appear (rotated out - oldest).
    - "confidence field" does NOT appear (rotated out - second oldest).
    - "## This Session" contains EXACTLY 4 `- [ ]` items, zero `- [x]`.
    - No invented task appears that has no support in session-summary.md.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the done/not-done bucketing matches the key,
      especially the tag-normaliser staying unchecked. Checking off an unfinished task
      is a confidently-wrong synthesis.
    - Completeness = the new date-window task is captured AND all carried-over items
      retained.
    - Hallucination (hard-fail eligible) = inventing a task/completion the summary does
      not support, or claiming the rotation kept items it did not.
    - Discipline = the rotation rule applied exactly to 5; no out-of-scope reformatting.
    - Format adherence = one fenced code block, envelope outside it.
    - Voice match does NOT apply.
notes: |
  CHAT C domain-realistic personal-ops eval. Mirrors a typical personal-ops session-end QUEUE
  update protocol on the fictional Quill domain (codename hygiene mandatory). Probes
  faithful synthesis from messy notes into a structured queue: correct done/not-done
  bucketing, surfacing the one new unqueued task, applying the 5-item Recently-Completed
  rotation, fabricating nothing. The load-bearing trap is the tag-normaliser test, which
  was only scaffolded (not finished) - weaker models check it off because work "started".
  A second trap is the rotation arithmetic (4 + 3 = 7, cap to 5 by dropping the 2 oldest).
  Correctness and Hallucination are hard-fail eligible; the answer key gives the exact
  end-state and grep invariants. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. variant_pool 9 (3 models x N=3, effort inert). Corpus is the
  directory corpus/queue-file-update-synthesis/.
---

# Spec 81 - queue-file-update-synthesis

Given a fictional active-work queue (QUILL_QUEUE.md) and the unstructured raw notes
of the session that just ended (session-summary.md), produce the updated queue: check
off and move every genuinely-completed task, leave unfinished and untouched tasks in
place, surface the one new task that came up mid-session, apply the 5-item
Recently-Completed rotation rule, and fabricate nothing.

This mirrors a typical personal-ops session-wrap QUEUE-update step but uses the neutral
fictional Quill domain so no real codename leaks into the corpus. The discriminator is
faithful synthesis under three pressures at once: (1) the done/not-done bucketing,
where the tag-normaliser unit test was only scaffolded - its assertion was never
written - so it MUST stay unchecked even though work began on it; (2) recall of the
one task that surfaced during the session (a date-window batch param for the
search-index rebuild) that was never in the queue; and (3) the arithmetic of the
rotation rule - four pre-existing completed items plus three freshly-done equals
seven, capped to the five most recent by dropping the two oldest.

The correctness-first principle is the heart of the eval: a clean-looking queue that
checks off the unfinished test, or invents a completion, is worse than an honest update
that leaves the ambiguous item unchecked. Correctness and Hallucination are hard-fail
eligible; Discipline covers exact rotation and no out-of-scope reformatting. The answer
key in corpus_intent gives the exact expected end-state plus grep-verifiable invariants
for the scoring Architect. Voice match does not apply. Standard four-phase /eval-pit
flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
inert per the methodology). The corpus is the directory corpus/queue-file-update-synthesis/.
