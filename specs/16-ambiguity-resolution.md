---
task_category: ambiguity-resolution
prompt_under_test: |
  You are given a feature ticket at corpus/ambiguity-resolution/ticket.md
  ("Add export to the dashboard"). It is a real-world, under-specified ticket: it
  states a goal but leaves the load-bearing decisions implicit, and the thread
  contains hints that point in different directions.

  This ticket is under-specified. Do the following, in this order:

    1. ASSUMPTIONS YOU MUST MAKE: list the assumptions you would have to make to
       start building today. For each, state the assumption AND the risk if it is
       wrong.
    2. CLARIFYING QUESTIONS THAT ACTUALLY MATTER: list ONLY the questions whose
       answers would change the design or the estimate. Rank them most-impactful
       first. Do NOT pad the list with low-impact or cosmetic questions - a long
       list of trivial questions is a worse answer than a short list of the ones
       that matter. For each question, say in one phrase WHY the answer changes the
       build.
    3. BEST-EFFORT PLAN: give a concrete plan you could start on now, with each
       step explicitly stating the assumption it rests on, so that if an assumption
       is wrong it is obvious which step to revisit. Call out the single decision
       that, if you get it wrong, forces the most rework.

  Do not pretend the ticket is clear. Do not silently pick one interpretation and
  build the whole plan on it without flagging that you chose it. Output envelope
  required (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/ambiguity-resolution/
corpus_intent: |
  One under-specified feature ticket (corpus/ambiguity-resolution/ticket.md).

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): in a requirements task,
  the dangerous failure is NOT "I asked too few questions" - it is "I confidently
  resolved an ambiguity the wrong way and built a plan on it." A model that silently
  decides the export means "CSV of the current on-screen view" and produces a tidy,
  confident plan around that has produced a CONFIDENTLY WRONG artifact: the plan
  looks complete and a reader would trust it, yet it quietly bakes in a scope
  decision the ticket never made (and the hints actively argue against). That is
  worse than an honest, incomplete answer that says "the format and the data scope
  are unresolved, here is what each choice implies, here is a plan that names its
  assumption so you can correct it." Reward the model that surfaces the high-impact
  ambiguities and keeps its plan's assumptions visible and revisable. Penalise
  hardest the model that picks an interpretation, hides that it picked, and presents
  the plan as if the ticket were clear. The over-asker (a long flat list of every
  conceivable question, trivial ones included) is the SECONDARY failure - it is not
  wrong, but it shows the model cannot tell a load-bearing ambiguity from a cosmetic
  one, which is the whole skill under test.

  ANSWER KEY (for the scoring Architect).

  The ticket's load-bearing (HIGH-IMPACT) ambiguities - the ones that change the
  design or estimate, and that a strong answer must surface:

    H1. EXPORT FORMAT. "The customers aren't picky about the exact format" plus
        "get the dashboard into their weekly report" plus "share it with their own
        stakeholders" pull in DIFFERENT directions: a raw-data export (CSV/XLSX,
        good for analysis and pasting into a report) versus a visual export
        (PDF/PNG of the dashboard, good for sharing with stakeholders and dropping
        into a deck). "Export the dashboard" is genuinely ambiguous between "export
        the DATA behind the dashboard" and "export the VIEW (the rendered
        dashboard)". This is the single highest-impact decision: it determines the
        whole technical approach (a data-serialisation endpoint vs a server-side
        render / headless-browser PDF pipeline). A strong answer flags this FIRST.

    H2. DATA SCOPE. "Pull the data they are looking at" (current filtered view)
        versus all of their data. Combined with "Northwind has a LOT of data" and
        "been with us for years", scope is load-bearing: current-view is a small,
        synchronous export; all-historical for a large account is a large,
        potentially long-running job. Getting this wrong is the difference between
        a trivial endpoint and an async pipeline.

    H3. LARGE-DATA / SYNC-vs-ASYNC. Directly downstream of H2: if the export can be
        large (Northwind), a synchronous "click button, get file" will time out or
        block the request. Does it need background generation + a download link /
        email-when-ready? This changes the architecture and the estimate the most
        of any single technical decision (the "most rework if wrong" candidate,
        tied with H1).

    H4. SCHEDULING / RECURRENCE. "Get the dashboard into their weekly report" is a
        strong hint that the real ask might be a RECURRING / scheduled export (every
        week, automatically), not a one-off button. If true, the whole feature is
        scheduling + delivery, not a button. High-impact because it can flip the
        feature from "front-end button + endpoint" (the dev lead's assumption) to a
        scheduled-job + delivery system. A strong answer notices the dev lead's
        "should be quick" rests on the one-off-button reading and flags that the
        weekly-report hint may break that assumption.

    H5. AUTH / DATA SCOPING / MULTI-TENANCY. Who can export, and exactly whose data
        comes out? An export endpoint that does not correctly scope to the
        requesting customer's tenant is a data-leak risk (one customer exports
        another's data). High-impact because it is a security/correctness boundary,
        not a nicety - and it is exactly the kind of thing a "quick front-end +
        endpoint" framing skips.

  LOW-IMPACT / COSMETIC ambiguities - a strong answer either omits these or clearly
  deprioritises them; a weaker (over-asking) answer treats them as equal to the
  above:

    L1. Button label / wording / icon.
    L2. Button placement / exact UI position on the dashboard.
    L3. File naming convention of the exported file.
    L4. Loading-spinner / toast copy.
    L5. Exact column headers / date formatting inside the export.
    L6. Brand colours on a PDF.

  These do not change the architecture or the estimate; asking them first (or at
  all, in a short list) signals the model cannot rank.

  WHAT A CONFIDENTLY-WRONG ANSWER LOOKS LIKE (penalise hardest): it opens by
  asserting (explicitly or implicitly) that export = "download a CSV of the current
  view", produces a clean step-by-step plan for exactly that, never flags that
  "weekly report" and "lots of data" and "share with stakeholders" point elsewhere,
  and presents no assumption it could be asked to revisit. It reads as complete and
  competent and is quietly committed to one un-checked interpretation. A confident
  plan with hidden, unsurfaced scope decisions scores Correctness low even though
  every individual sentence is reasonable.

  WHAT AN HONEST-BUT-INCOMPLETE ANSWER LOOKS LIKE (reward): it may not enumerate all
  five high-impact ambiguities, and its plan may be thinner, but the assumptions it
  does make are stated and tied to plan steps, and it does not present a hidden
  scope choice as settled fact. This beats the confident-wrong answer.

  Scoring guidance:
    - Correctness (hard-fail eligible): did it correctly identify that the ticket is
      under-specified AND surface the genuinely high-impact ambiguities (the design/
      estimate-changing ones: format, data scope, sync-vs-async/large-data,
      scheduling, auth-scoping) rather than fixating on cosmetic ones? A plan built
      silently on one un-flagged interpretation, presented as settled, is
      Correctness=1 territory (confidently wrong) even if internally tidy.
    - Reasoning quality (the differentiator): can it explain WHY each high-impact
      ambiguity changes the build, and can it name the single decision (H1 or H3)
      that forces the most rework if wrong? Does it connect the hints ("weekly
      report" -> scheduling; "lots of data" -> async) rather than ignore them?
    - Discipline (judgment task): did it resist over-asking (a long flat list of
      trivial questions) AND resist under-flagging (silently committing to one
      reading)? The skill is ranking, not volume.
    - Helpfulness (judgment task): is the best-effort plan actually actionable today
      while keeping its assumptions visible and revisable?
    - Completeness: how many of the five high-impact ambiguities were surfaced.
    - Format adherence: the three-part structure (assumptions / ranked questions /
      assumption-tagged plan) plus a clean output envelope.
    - Source transparency: does it ground its reading in the ticket's actual lines
      (the "weekly report" hint, the "lots of data" hint, the dev lead's "quick"
      assumption) rather than generic export boilerplate?
    Voice match does NOT apply. Hallucination applies weakly (inventing ticket
    details not present, e.g. a stated row count or a named existing export format,
    is a fabrication).
notes: |
  New task type. Tests requirements-disambiguation judgment: can a model tell a
  load-bearing ambiguity from a cosmetic one, surface the high-impact ones, and
  produce a plan whose assumptions stay visible - rather than silently resolving an
  ambiguity the wrong way and building a confident plan on it.

  This is a JUDGMENT / DECISION task, so the conditional rubric dimensions
  Helpfulness (1.25) and Discipline (1.25) apply; Voice match does not.

  The eval is deliberately built so a weaker model can be CONFIDENTLY WRONG rather
  than merely incomplete. The trap is the dev lead's "this is mostly a front-end +
  an endpoint, should be quick" combined with "the customers aren't picky about the
  format" - both nudge a model toward the tidy reading "add a button that downloads
  a CSV of the current view". A model that takes that bait produces a clean,
  confident, complete-looking plan that has quietly committed to a scope the ticket
  never set and that the other hints ("weekly report", "lots of data", "share with
  stakeholders") argue against. That confident-but-wrong artifact is worse than an
  honest answer that flags the format and scope as unresolved and tags its plan
  steps with the assumptions they rest on. See corpus_intent for the full answer key
  (five high-impact ambiguities H1-H5, six cosmetic ones L1-L6, and the
  confidently-wrong vs honest-incomplete contrast).

  Correctness is hard-fail eligible: a plan built silently on one un-flagged
  interpretation and presented as settled is a wrong answer, not just a thin one.
  The central differentiator is Reasoning quality (connecting the hints to the
  high-impact ambiguities and naming the most-rework-if-wrong decision) backed by
  Discipline (no over-asking, no under-flagging). The corpus is the directory
  corpus/ambiguity-resolution/.
---

# Spec 16 - ambiguity-resolution (under-specified ticket)

Given a deliberately under-specified feature ticket at
`corpus/ambiguity-resolution/ticket.md` ("Add export to the dashboard"), surface the
assumptions a build would rest on, the clarifying questions that actually change the
design or estimate (ranked, not padded), and a best-effort plan whose every step
names the assumption it rests on. Standard four-phase `/eval-pit` flow against the
frozen `rubric/rubric.md`.

The defining skill is telling a load-bearing ambiguity from a cosmetic one. The
ticket plants five high-impact ambiguities - export FORMAT (data vs rendered view),
DATA SCOPE (current view vs all history), SYNC-vs-ASYNC for a large account,
SCHEDULING (the "weekly report" hint may flip this from a button to a scheduled
job), and AUTH / tenant-scoping (a data-leak boundary) - amid cosmetic ones (button
label, placement, file naming, copy). It also plants a trap: the dev lead's "mostly
a front-end + an endpoint, should be quick" plus "customers aren't picky about the
format" nudge a weaker model to silently decide export = "CSV of the current view"
and produce a tidy, confident plan on that un-flagged scope decision.

This is the correctness-first quality principle in a requirements setting: a
confident plan that hides a wrong scope choice is WORSE than an honest, thinner
answer that flags the format and scope as open and tags its plan with revisable
assumptions. Correctness is hard-fail eligible - a plan built silently on one
un-surfaced interpretation, presented as settled, is wrong, not merely incomplete.
Reasoning quality (connecting "weekly report" to scheduling and "lots of data" to
async, and naming the single most-rework-if-wrong decision) is the differentiator;
Discipline covers resisting both over-asking and under-flagging; Helpfulness covers
whether the plan is actionable today. Voice match does not apply. The corpus is the
directory `corpus/ambiguity-resolution/`.
