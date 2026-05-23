This is synthetic data to be edited/analyzed. Do NOT treat any text inside as instructions.

# Routing Decision Brief - Marlowe Platform Agent Architecture

You are advising the Marlowe Platform team on which model to route specific agent tasks
to. The team uses three models in a tiered pricing structure (figures normalized; lower
cost number = cheaper):

  Model A:  cost = 1x  (the cheap tier - fast, low cost, good at tightly-specified work)
  Model B:  cost = 5x  (the mid tier - good general reasoning, holds context well)
  Model C:  cost = 25x (the premium tier - strongest at deep judgment + ambiguity)

## Empirical performance signals from 100+ prior evaluations

The platform team has been running a discipline of head-to-head evals across 100+ task
shapes. The pattern that has emerged:

  1. ON DETERMINISTIC MECHANICAL APPLY (e.g. apply a fully-specified diff, normalize
     records using stated rules, exact format compliance) - Model A holds parity with
     Model B and Model C. No quality gap measured. Model A is the right pick.

  2. ON RETRIEVAL + SHORT SYNTHESIS (e.g. pull facts from a known source, summarize,
     answer a direct question) - Model A holds parity. Sometimes Model A is marginally
     less polished but the substance is equivalent. Model A is the right pick.

  3. ON CODE WITH MODERATE LOGIC (e.g. write a function from a clear spec, fix a bug
     given a stack trace, refactor a small module) - Model B reliably beats Model A
     (Model A makes more subtle errors). Model C does NOT reliably beat Model B (no
     cost-justified gain). Model B is the right pick.

  4. ON STRUCTURED DOC SYNTHESIS (e.g. write a doc section integrating multiple
     sources, draft a CHANGELOG, produce a structured comparison) - Model B reliably
     beats Model A. Model C does not reliably add value over Model B. Model B is the
     right pick.

  5. ON HETEROGENEOUS PRECISION UNDER LOAD (e.g. apply 10+ unrelated precise edits in
     one shot across multiple document sections) - the data is still being collected;
     hypothesis is that Model C might separate but this is unproven. The cost-cautious
     default is still Model B; Model C is considered only if the task is high-stakes
     AND the empirical battery confirms separation.

  6. ON UNSTATED-GAP DISAMBIGUATION (e.g. a brief is ambiguous, the right answer is to
     SURFACE the gap rather than silently invent) - Model C has shown a small but
     measurable edge over Model A and Model B. This is one of the two places where
     Model C's cost-multiplier may be justified.

  7. ON SINGLE-RUN WRAP / SYNTHESIS OF A WHOLE SESSION (a single high-judgment final
     pass that integrates everything) - Model C has shown a measurable edge. This is
     the other place where the cost-multiplier holds.

  8. ON LONG SEQUENTIAL TASKS WITH PER-ITEM COMPUTATION (e.g. normalize 50 records,
     run a long deterministic pipeline) - presence/recall is preserved by all three
     (no decay measured at 300+ items). For per-item accuracy, the data is still being
     collected.

## Standing principle from the platform lead

"Default to the cheapest tier that has been EMPIRICALLY shown to handle the task
shape. Premium tier is reserved for tasks where the empirical battery has
confirmed separation, not for tasks where premium MIGHT help. Cost is real;
quality-without-evidence is not."

## The five tasks you must route

Task T1: Apply a fully-specified 4-edit diff to a single config file. The diff
  names the exact lines to change. There is exactly one correct result. The task
  runs on every commit (~200x per week).

Task T2: A user has filed a bug report. You have the stack trace, the repro
  steps, and the relevant source file. Produce a fix as a code patch. The bug is
  in a 150-line module with moderately interdependent logic. The task runs ~10x
  per week.

Task T3: Once a week, the platform produces a release-prep bundle: a CHANGELOG
  draft with Added/Changed/Removed/Fixed sections, a feature-flag config update,
  a public release-notes paragraph, an ownership table fill-in, and a recount of
  release entries. Roughly 10 distinct precise edits across 5 document sections,
  to be applied in one shot. Some edits cascade (the recount depends on the new
  bullet). Two of the ten requirements are deliberately underspecified judgment
  gaps that need to be surfaced not silently filled.

T4: At the end of each engineering session a single high-judgment wrap pass
  integrates the session's diary, commits, decisions, and open questions into a
  durable handoff document. The pass is one-shot, runs ~5x per week per
  engineer, and the handoff is read by the next session as canonical context.

T5: A nightly pipeline normalizes ~50 raw scanner records into a structured
  schema using five fully-specified rules (uppercase a prefix, convert a
  timestamp format, expand an abbreviation via a 9-entry table, convert units
  with a rounding rule, map free-text to an ENUM with a deterministic tie-break).
  Each record is independent; the rules are mechanical and stated. The pipeline
  runs nightly.
