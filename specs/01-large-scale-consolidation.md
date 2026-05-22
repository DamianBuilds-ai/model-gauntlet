---
task_category: large-scale-consolidation
prompt_under_test: |
  You are given a single corpus file containing 40 short work-session thread
  snippets (decisions, bugs, status notes, blocked items, follow-ups) for a
  fictional company "Acme". Many threads cross-reference each other.

  Consolidate ALL 40 threads into ONE structured summary that a team lead could
  read in a few minutes. The summary MUST:
    1. Group the threads into coherent themes (do NOT produce 40 bullet points -
       the value is in the grouping and the cross-thread connections).
    2. Within each theme, trace the dependency chains (e.g. "X is blocked on Y
       which is blocked on Z") where the threads reference each other.
    3. Produce a single prioritized "top open risks / next actions" list, each item
       citing the thread numbers that motivate it.
    4. Distinguish decided items, in-progress items, and blocked/unowned items.
  Do not invent threads or facts not present in the corpus. If something is unowned
  or undecided, say so. Output envelope required (schemaVersion, tier, status,
  tool_budget_used). No em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/large-scale-consolidation.md
notes: |
  PRIORITY PROBE. This is the scale-cranked analog of a smaller consolidation eval.
  Purpose: find the SCALE THRESHOLD where the top-tier model (Opus) pulls ahead of
  the cheaper models on large consolidation. At small item counts (a handful of items)
  cheaper models consolidate fine; the hypothesis is that as the item count and
  cross-thread dependency density rise, the cheaper models start to (a) drop threads,
  (b) miss cross-references, or (c) flatten the dependency chains into a flat list. This
  eval uses 40 deliberately interlinked threads to stress exactly that. Run the FULL
  9-variant model-only pool (3 models x N=3 - Haiku x3, Sonnet x3, Opus x3; effort
  treated as inert per the methodology) - the whole point is to see where the MODELS
  separate at scale. Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding. Watch
  specifically for: dropped threads (Completeness), missed dependency chains (Reasoning
  quality), and over-flattening (Reasoning quality). Compare the practical winner here
  against the practical winner of any smaller consolidation eval to locate the threshold.
---

# Spec 01 - large-scale-consolidation (the 40-thread probe)

This is the priority probe in the queue. See the `notes` field above for the
scale-threshold hypothesis it is designed to test. The corpus is a single file with
40 small, varied, cross-referencing session threads at
`corpus/large-scale-consolidation.md`.

The eval runs through the standard `/eval-pit` four-phase flow against the frozen
`rubric/rubric.md`. Because this is a consolidation/judgment task, the applicable
dimensions include Reasoning quality (heavily - the cross-thread dependency tracing
is the core signal), Completeness (did it keep all 40 threads or silently drop
some), Helpfulness, and Discipline. Voice match does not apply.
