---
task_category: planning-decomposition
prompt_under_test: |
  You are given a project brief at
  corpus/planning-decomposition-at-scale/project-brief.md describing the build-out of
  an internal analytics-ingestion service. The brief lists 18 work items (T01 - T18),
  each with a set of HARD prerequisites: an item may not start until ALL of its listed
  prerequisites are complete.

  Produce a dependency-ordered execution plan: a single ordered list of every task ID,
  from first to last, such that no task ever appears before any of its prerequisites.

  Rules:
    1. The list must contain every task ID exactly once - all 18, no omissions, no
       duplicates, no invented IDs.
    2. For every task, ALL of its prerequisites must appear earlier in the list than the
       task itself.
    3. More than one valid ordering exists; any ordering that satisfies rule 2 is
       correct. You are NOT trying to match one specific sequence.
    4. Output the plan as a numbered list, one task per line, in the form:
         1. T01 - <the task's one-line description>
       Use the task's own description from the brief. Then, AFTER the numbered list,
       output a short "Dependency check" section listing, for each task that HAS
       prerequisites, the line "<task> requires <prereq list> - all satisfied at
       position N" confirming each prerequisite's position is earlier. This makes your
       ordering auditable.

  Output the numbered plan and the dependency-check section as plain markdown. After
  that, append the required output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/planning-decomposition-at-scale/
corpus_intent: 1 project brief with 18 tasks and a hard-prerequisite dependency graph
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a plan that places ANY task
  before one of its prerequisites is confidently-wrong - it reads as a clean ordered
  plan but would deadlock or fail if executed, which a downstream reader would trust. A
  plan that drops a task, duplicates one, or invents an ID is also wrong. An honest,
  fully-ordered, complete plan is the only correct output. Correctness (every precedence
  edge honoured) and Hallucination (no invented tasks/edges) are hard-fail eligible.

  Why at-scale / harder: 18 tasks, 26 precedence edges, multiple diamond dependencies
  (T04 needs both T02 and T03; T09 needs T04 and T07; T17 needs T10, T14 AND T16; T18
  needs T15, T16 AND T17). The deep transitive chains (T01 -> T02 -> T04 -> T09 -> T12
  -> T16 -> T17 -> T18) mean a model that orders greedily by "looks ready" without
  tracking the full closure will slip a late task too early. The headline signal is how
  many of the 26 edges survive in one long ordering, plus whether the model keeps the
  set complete (18 unique).

  ANSWER KEY - mechanically verifiable. The grader does NOT match a fixed sequence. The
  grader checks the model's ordering against this fixed EDGE LIST. For each edge
  (prereq -> dependent), confirm prereq appears at an EARLIER position than dependent in
  the model's list. All 26 must hold. Then confirm the list is exactly the 18 IDs T01 -
  T18, each once.

  THE 26 PRECEDENCE EDGES (prereq must precede dependent):
    T01 -> T02
    T01 -> T03
    T02 -> T04
    T03 -> T04
    T05 -> T06
    T02 -> T07
    T06 -> T08
    T07 -> T08
    T04 -> T09
    T07 -> T09
    T09 -> T10
    T04 -> T11
    T05 -> T11
    T09 -> T12
    T11 -> T12
    T03 -> T13
    T13 -> T14
    T08 -> T15
    T09 -> T15
    T12 -> T16
    T10 -> T17
    T14 -> T17
    T16 -> T17
    T15 -> T18
    T16 -> T18
    T17 -> T18

  ROOTS (no prerequisites, may appear anywhere before their dependents): T01, T05.
  TERMINAL: T18 must be LAST (it transitively depends on everything else).

  ONE VALID REFERENCE ORDERING (for the Architect's convenience - the model need NOT
  match it; ANY ordering passing all 26 edges is correct):
    T01, T05, T02, T03, T06, T07, T04, T13, T08, T09, T11, T14, T10, T12, T15, T16, T17,
    T18
  (Verified: 26/26 edges satisfied, 18 unique IDs, T18 last.)

  Scoring guidance: Correctness = number of the 26 precedence edges honoured (an
  ordering with even one inversion is functionally broken - score Correctness=1 only if
  multiple edges are violated or the set is incomplete; a single inversion is a serious
  Correctness hit but the Architect uses judgment on 1 vs 2). Completeness = all 18 IDs
  present exactly once AND the dependency-check section present and accurate.
  Hallucination (hard-fail) = inventing a task ID, an edge, or a prerequisite not in the
  brief. Format adherence = numbered list in the requested form + dependency-check
  section + envelope. Reasoning quality = the dependency-check section actually verifies
  positions rather than restating prerequisites. Discipline = did not reorder away from
  the constraints or silently drop the check section. Source transparency applies weakly
  (single brief). Voice match does NOT apply.

  Architect verification procedure: (1) extract the model's ordered ID list; (2) build a
  position map; (3) for each of the 26 edges assert pos[prereq] < pos[dependent], count
  failures; (4) assert the ID multiset equals {T01..T18}; (5) assert T18 is last; (6)
  confirm the dependency-check section's claimed positions match the actual list.
---

# Spec 59 - planning-decomposition-at-scale (dependency-ordered task plan from a 18-task brief)

Decompose a project brief at `corpus/planning-decomposition-at-scale/project-brief.md`
into a dependency-ordered execution plan. The brief defines 18 work items (T01 - T18)
connected by 26 hard prerequisite edges, including several diamond dependencies and a
deep transitive chain ending at the production-cutover task T18. The model must emit one
ordered list of all 18 IDs in which every prerequisite precedes its dependent, plus a
self-audit "Dependency check" section.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Grading is
mechanical and order-agnostic: the Architect checks the model's ordering against a fixed
26-edge precedence list (each prereq must appear before its dependent) and confirms the
list is exactly the 18 IDs once each, with T18 last. The correctness-first quality
principle bites because a single inversion produces a clean-looking plan that would
deadlock on execution. Correctness (edges honoured) and Hallucination (no invented
tasks/edges) are hard-fail eligible; Completeness (all 18, plus an accurate check
section) and Reasoning quality (the check section truly verifies positions) are the
load-bearing differentiators. Voice match does not apply. The corpus is the directory
`corpus/planning-decomposition-at-scale/`.
