---
task_category: session-wrap-protocol-execution
prompt_under_test: |
  You are wrapping up a work session. Two files are provided in the directory
  corpus/session-wrap-protocol-execution/:

    - wrap-protocol.md - the 8-step Brightwater session wrap protocol.
    - session-state.md - what happened in the session you are wrapping.

  Execute the wrap protocol against the session state. For EACH of the 8 steps,
  produce the concrete artifact that step calls for, in order, based on what actually
  happened in the session:

    - For document-update steps, write the actual content that should go into that
      document (the Quick Resume line, the HANDOFF done/in-progress/blocked buckets,
      the NEXT_ACTIONS list, the moment text, the findings-table row, the commit
      message, etc.).
    - For the CONDITIONAL steps (3, 5, 6), explicitly STATE whether the condition
      fired and why, based on the session state - then do the step if it fired, or
      acknowledge the no-op if it did not. Do NOT silently skip a conditional step.

  Do NOT invent work that did not happen. Do NOT skip any of the 8 steps. Ground every
  artifact in the session state.

  Output your wrap as markdown, with a clearly labelled section per step (Step 1
  through Step 8). Then append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines after the markdown. No em dashes (use
  spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/session-wrap-protocol-execution/
corpus_intent: |
  Two fictional files: an 8-step session wrap protocol (wrap-protocol.md) and a session
  state (session-state.md). The eval tests COMPLETENESS UNDER A CHECKLIST - does the
  model perform ALL 8 steps, correctly handle the three CONDITIONAL steps, and ground
  every artifact in the session state without fabricating work. All codenames fictional
  (Brightwater, Hollowmere, Quill, QUILL_QUEUE.md etc., people, PR #214).

  The session state is calibrated so the conditionals have determinate answers:
    - Step 3 (LOG rotation, fires IF Recently Completed >= 5 items): the session adds
      its completed items and the section reaches 6 items, so 6 >= 5 => STEP 3 FIRES.
      A correct wrap rotates the oldest item(s) into the LOG. (Missing this - treating
      step 3 as a no-op - is the primary buried trap.)
    - Step 5 (content moment, fires IF something quotable happened): the Brightwater
      lead's "invisible for three weeks" quote is present => STEP 5 FIRES.
    - Step 6 (cross-domain finding, fires IF the session produced a cross-team finding):
      the config-drift finding is explicitly cross-domain-relevant => STEP 6 FIRES.

  ANSWER KEY - the 8 expected wrap artifacts (the scoring Architect counts these):
    1. STEP 1 - QUEUE update: a refreshed Quick Resume line + completed items checked
       off (retry-ceiling bump, INC-0447 write-up, PR #214 opened) moved to Recently
       Completed.
    2. STEP 2 - HANDOFF: DONE = retry ceiling bump / INC-0447 write-up / PR #214 opened;
       IN PROGRESS = config-drift reconciliation awaiting Brightwater-lead review of
       PR #214; BLOCKED = dashboard widget update, blocked on the missing Quill API
       token. All three buckets present and correctly assigned.
    3. STEP 3 - LOG rotation: STATES the condition (Recently Completed reaches 6 items,
       6 >= 5) and ROTATES the oldest item(s) (the Tier-2 SLA doc update / on-call
       roster items) into QUILL_LOG.md. Step 3 MUST fire - a wrap that says "fewer than
       5, no-op" is WRONG.
    4. STEP 4 - NEXT_ACTIONS: removes completed items, adds the live follow-ups (get
       PR #214 reviewed/merged; chase the Quill API token for the dashboard widget),
       capped at 10.
    5. STEP 5 - MOMENT: appends the Brightwater lead's "invisible for three weeks" quote
       to MOMENTS.md. Step 5 fires.
    6. STEP 6 - cross-domain finding: writes a findings-table (412) row capturing the
       config-drift finding (running deploy can diverge from committed config; catch by
       cross-checking running state vs repo HEAD), tagged to Quill / messaging-domain
       registry. Step 6 fires.
    7. STEP 7 - push: a commit + push via the build-host helper, on branch `main`, with
       a sensible commit message naming the changed docs.
    8. STEP 8 - temp cleanup: removes the two named scratch files
       (working-outputs/2026-03-11-drift-scratch.md and -inc0447-notes.md).

  THE FAILURE MODES TO DETECT:
    - SKIPPING STEP 3 / treating it as a no-op (the buried conditional). The count is 6,
      not under 5. This is the highest-signal trap.
    - DROPPING the blocked item (dashboard widget / Quill API token) from the HANDOFF.
    - FABRICATING work not in the session state (a merged PR #214 - it is explicitly
      NOT merged; a fifth completed item; an invented moment or finding).
    - Collapsing or skipping a step entirely (fewer than 8 labelled steps).
    - Mishandling a conditional - silently skipping step 5 or 6 instead of stating it
      fired, or claiming a conditional fired when the state does not support it.
    - Marking PR #214 as merged or the dashboard widget as done (it is blocked).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - Output contains all eight step labels: `Step 1` ... `Step 8` (or "1." ... "8."
      with the step names). Eight distinct steps must be present.
    - Step 3 section asserts the count is >= 5 (mentions `6` items or "6 >= 5" or
      "fires") and performs the rotation - it does NOT say "no-op" / "fewer than 5".
    - HANDOFF (Step 2) contains a BLOCKED entry naming the dashboard widget AND the
      missing Quill API token.
    - `PR #214` (or "#214") appears and is described as OPEN / NOT merged / awaiting
      review - never as merged/done.
    - Step 5 references the "invisible for three weeks" moment.
    - Step 6 references the config-drift cross-domain finding.
    - Step 7 names branch `main` and references the changed docs in a commit message.
    - Step 8 references the two named scratch files (drift-scratch / inc0447-notes).
    - No invented completed item, no merged-PR claim, no fabricated moment/finding.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all 8 steps performed AND the three conditionals
      handled correctly (step 3 FIRES with rotation; steps 5 and 6 FIRE). Skipping step 3
      or marking PR #214 merged is Correctness=1.
    - Completeness = all eight answer-key artifacts present and grounded.
    - Hallucination (hard-fail eligible) = inventing work, marking blocked/unmerged items
      as done, or fabricating a moment/finding.
    - Discipline = does NOT pad with steps the protocol does not list; does NOT silently
      skip a conditional.
    - Format adherence = labelled per-step markdown, envelope outside, spaced hyphens.
    - Reasoning quality = conditional decisions justified from the session state.
    Voice match does NOT apply.
notes: |
  Chat C domain-realistic eval (personal-ops / markdown-KB), mirrors the main-session
  8-step wrap protocol. The scored discriminator is CHECKLIST COMPLETENESS UNDER
  CONDITIONALS - performing all 8 steps and correctly resolving the three conditional
  steps (the buried trap is step 3 LOG rotation, which FIRES because Recently Completed
  reaches 6 items, not under 5), while grounding artifacts in the session state and not
  fabricating work (PR #214 is explicitly NOT merged; the dashboard widget is BLOCKED).
  The session state is calibrated so each conditional has a determinate answer. Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. Correctness and
  Hallucination are hard-fail eligible; the answer key (the 8 expected artifacts) plus
  grep-verifiable invariants are embedded in corpus_intent. Voice match does not apply.
  Variant pool 9 (3 models x N=3, effort inert). Corpus is the directory
  corpus/session-wrap-protocol-execution/. All codenames fictional - no real
  domain names.
---

# Spec 87 - session-wrap-protocol-execution

Execute a fictional 8-step session wrap protocol against a session state, producing the
concrete artifact for each of the eight steps in order. The corpus is two files: the
protocol (wrap-protocol.md) and the session state (session-state.md).

The eval tests completeness under a checklist with conditionals. Three of the eight
steps (3 LOG rotation, 5 content moment, 6 cross-domain finding) are conditional, and
the session state is calibrated so each has a determinate answer. The load-bearing
buried trap is step 3: the session's completed items push "Recently Completed" to six
items, so the rotation condition (>= 5) FIRES and the wrap must rotate the oldest item
into the LOG. A weaker model that treats step 3 as a no-op ("fewer than 5, skip") fails
the core discriminator. Steps 5 and 6 also fire (a quotable moment and a cross-domain
finding are both present); a correct wrap states each conditional fired and why.

Grounding matters: PR #214 is explicitly NOT merged (awaiting a Brightwater-lead
review) and the dashboard widget update is BLOCKED on a missing Quill API token. A wrap
that marks either as done is hallucinating. The HANDOFF must carry the blocked item, the
NEXT_ACTIONS must carry the live follow-ups, and the push step targets branch `main`.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; the answer key (the 8 expected artifacts) plus
grep-verifiable invariants live in `corpus_intent` for the scoring Architect. Voice match
does not apply. The variant pool is 9 (3 models x N=3, effort inert per the methodology).
The corpus is the directory `corpus/session-wrap-protocol-execution/`.
