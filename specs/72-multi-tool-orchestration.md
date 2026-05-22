---
task_category: multi-tool-orchestration
prompt_under_test: |
  You are given a fictional tool environment and a goal at
  corpus/multi-tool-orchestration/task.md. It defines a catalog of tools (with inputs,
  outputs, costs, and preconditions), a set of hard environment rules, and a goal.

  Produce the ORDERED sequence of tool calls (the "call plan") that achieves the goal at
  MINIMUM total cost while respecting EVERY precondition and hard rule. Do NOT execute
  anything - just produce the plan. For each step give: the tool with its concrete
  argument, and a one-line reason. After the plan, state the TOTAL COST (sum of the
  per-call costs).

  Constraints to honour:
    - Every precondition in the catalog must be satisfied at the time each call is made
      (e.g. you must have read a file before you can patch it; commit requires a prior
      successful patch AND the most recent run_tests to be PASS).
    - No redundant calls (do not read the same file twice, do not run the full suite when
      a single-file test run is enough, do not lint a file you never changed, do not call
      a tool whose result you already have).
    - The ordering must be dependency-correct: run_tests that satisfies commit must come
      AFTER the patch and immediately before the commit.

  No em dashes (use spaced hyphens). No emojis. After your plan, append the required
  output envelope (schemaVersion, tier, status, tool_budget_used) as separate lines.
variant_pool: 9
corpus: corpus/multi-tool-orchestration/
corpus_intent: |
  One task file (corpus/multi-tool-orchestration/task.md): a fictional tool catalog
  ("Quartzline") with 7 tools, each carrying a cost and preconditions, plus hard
  environment rules and a goal (locate + fix + verify + commit a one-line bug in
  normalize_path). This is a single-shot proxy for multi-tool agentic orchestration: the
  model PLANS the call sequence rather than executing it. The discriminators are
  dependency-aware ordering, full precondition satisfaction, and zero redundant calls
  (minimum cost).

  QUALITY PRINCIPLE (correctness-first). A plan that LOOKS complete but violates a
  precondition (patches before reading, commits before re-running tests, commits without
  a passing run_tests) is WORSE than a slightly costlier plan that is dependency-correct.
  The traps are: (a) calling list_modules() unnecessarily (search locates the file
  directly and has no list_modules precondition - list_modules is a wasted call here);
  (b) running run_tests BEFORE the patch and then NOT re-running after, so commit's "most
  recent run_tests was PASS after the patch" precondition fails; (c) running the FULL
  test suite instead of the single-file test (more cost); (d) ordering commit before the
  final run_tests; (e) patching before reading the file (apply_patch rejects with "stale
  base").

  ANSWER KEY (for the scoring Architect) - the canonical minimum-cost dependency-correct
  plan. Argument names for the located module/test are placeholders the model fills.

    Step 1: search("normalize_path")              cost 2
            -> locates the module file; satisfies read-before-patch when combined with a
               read, and avoids reading every module. (list_modules is NOT needed.)
    Step 2: read_file(<the located module>)        cost 1
            -> gets current contents to author the diff AND to satisfy apply_patch's
               read-before-patch precondition.
    Step 3: apply_patch(<module>, <one-line diff>) cost 3
            -> applies the trailing-slash fix; base is fresh from Step 2.
    Step 4: lint(<module>)                          cost 2
            -> lints ONLY the changed file before committing (the goal asks for this).
    Step 5: run_tests(<single-file test path>)      cost 5
            -> run AFTER the patch and BEFORE the commit; single-file run, not full suite;
               satisfies commit's "most recent run_tests was PASS" precondition.
    Step 6: commit("fix normalize_path trailing-slash handling")  cost 4
            -> both commit preconditions met (a patch succeeded + most recent run_tests
               PASS).

    TOTAL COST = 2 + 1 + 3 + 2 + 5 + 4 = 17.

    Acceptable minor variations: lint (Step 4) and run_tests (Step 5) may be swapped (lint
    has no ordering dependency relative to run_tests, only relative to having a changed
    file), as long as run_tests is the LAST call before commit and comes AFTER the patch.
    Swapping them keeps total cost 17. Putting lint after run_tests is FINE; putting
    run_tests before apply_patch (and not re-running) is NOT (breaks commit precondition).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The plan contains exactly these 6 tool calls: search, read_file, apply_patch, lint,
      run_tests, commit. Each appears exactly once. NO list_modules call (it is the
      redundancy trap).
    - read_file (or the search that surfaces contents) appears BEFORE apply_patch.
    - apply_patch appears BEFORE the run_tests that precedes commit.
    - run_tests appears immediately BEFORE commit (no tool call between them that would
      reset the "most recent run_tests" state - lint between is acceptable since lint does
      not change the most-recent-run_tests state; but the safest correct plan keeps
      run_tests last before commit).
    - commit is the FINAL call.
    - Stated TOTAL COST == 17.
    - A confidently-wrong plan: includes list_modules (cost +1, redundant), runs
      run_tests only before the patch, runs the full suite, or orders commit before the
      last run_tests.

  Scoring guidance:
    - Correctness (hard-fail eligible) = a dependency-correct plan where every
      precondition holds at call time and commit's two preconditions are satisfiable. Any
      precondition violation (patch-before-read, commit-before-passing-test) is
      Correctness=1.
    - Completeness = all goal steps covered (locate, read, patch, lint, test, commit).
    - Hallucination (hard-fail eligible) = inventing a tool not in the catalog, inventing
      a precondition that does not exist, or claiming a cost the catalog does not state.
    - Discipline = ZERO redundant calls (no list_modules, no full-suite run, no
      double-read, no lint of an unchanged file). Minimum cost 17. This is the
      load-bearing discriminator.
    - Reasoning quality = each step's one-line reason correctly cites the precondition or
      dependency it satisfies.
    - Source transparency = arguments reference the located module/test path.
    Voice match does NOT apply.
notes: |
  NEW task type, Chat B agentic battery (71, 72, 78, 79, 80). Multi-tool orchestration is
  delivered single-shot as a PLANNING proxy: the model produces the ordered call plan
  rather than executing it, which is fully scoreable in one shot. The discriminators are
  dependency-aware ordering, full precondition satisfaction, and minimum cost (zero
  redundant calls). The corpus encodes real preconditions (read-before-patch via "stale
  base"; commit requires a successful patch AND the most-recent run_tests to be PASS
  AFTER the patch) and per-call costs so the plan is objectively scoreable.

  The canonical optimal plan is 6 calls totalling cost 17: search -> read_file ->
  apply_patch -> lint -> run_tests -> commit (lint/run_tests order is flexible as long as
  run_tests is last before commit and after the patch). The traps are all redundancy or
  ordering errors: an unnecessary list_modules call (search already locates the file), a
  pre-patch-only run_tests that fails commit's precondition, a full-suite run instead of
  single-file, or committing before the final test. The answer key gives the exact plan,
  total cost 17, the acceptable swap, and grep-verifiable invariants. Correctness and
  Hallucination are hard-fail eligible; Discipline (zero redundant calls, minimum cost) is
  the load-bearing discriminator. Voice match does not apply. Standard four-phase
  /eval-pit flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x
  N=3, effort inert per the methodology). The corpus is the directory
  corpus/multi-tool-orchestration/.
---

# Spec 72 - multi-tool-orchestration (single-shot call-plan proxy)

Given a fictional tool catalog (tools with costs and preconditions), a set of hard
environment rules, and a goal, produce the ordered, dependency-correct, minimum-cost
sequence of tool calls that achieves the goal without violating any precondition.

The gauntlet is single-shot, so multi-tool agentic orchestration is delivered as a
PLANNING proxy: the model emits the call plan (tool + concrete argument + one-line
reason per step) and the total cost, rather than executing live. This is fully
objectively scoreable - the plan either honours the preconditions and minimises cost or
it does not.

The discriminators are dependency-aware ordering (read before patch; the
commit-satisfying run_tests after the patch and last before commit), full precondition
satisfaction (commit needs a prior successful patch AND a passing most-recent
run_tests), and zero redundant calls. The traps are an unnecessary list_modules call
(search already locates the target), a pre-patch-only run_tests that fails commit's
precondition, a wasteful full-suite run, or committing before the last test. The
canonical optimal plan is 6 calls at total cost 17.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
(dependency-correct, all preconditions hold) and Hallucination (no invented tools or
preconditions) are hard-fail eligible; Discipline - zero redundant calls, minimum cost
17 - is the load-bearing discriminator. The answer key in `corpus_intent` gives the exact
plan, the acceptable lint/run_tests swap, total cost 17, and grep-verifiable invariants.
Voice match does not apply. The variant pool is 9 (3 models x N=3, effort inert per the
methodology). The corpus is the directory `corpus/multi-tool-orchestration/`.
