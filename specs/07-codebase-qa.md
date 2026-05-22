---
task_category: codebase-qa
prompt_under_test: |
  You are given a small synthetic codebase across three files under
  corpus/codebase-qa/ (app.py, queue_store.py, worker.py) and a question at
  corpus/codebase-qa/question.md. Answer the question by reading the code.

  Requirements:
    1. Trace the actual call path through the files. Cite the specific file and
       function for every claim you make.
    2. Answer the quantitative part exactly: given max_retries=3, how many total
       times is a failing job's handler attempted before the job is gone? Reason
       about the initial attempt plus the attempts < max_retries re-enqueue check.
    3. State what happens to a job after it exhausts retries, and whether any recovery
       path exists in the code as written.
    4. Do NOT invent code, functions, or a dead-letter queue that is not present.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/codebase-qa/
notes: |
  New task type. Tests multi-file code comprehension with an exact-count sub-question
  (a classic place cheaper models go off-by-one). Correct answer: the job is handled,
  fails (attempts -> 1, 1 < 3 so re-enqueued), handled again (attempts -> 2, re-enqueued),
  handled again (attempts -> 3, 3 < 3 is false so NOT re-enqueued and dropped) - so 3
  total handler attempts, then dropped silently with no dead-letter queue and no recovery
  path. Watch for: wrong count (Correctness hard-fail), inventing a dead-letter queue
  (Hallucination hard-fail), and missing the "no recovery" conclusion (Completeness).
  Source transparency matters (cite files/functions). Voice match does not apply.
---

# Spec 07 - codebase-qa

Answer the synthetic code-comprehension question in `corpus/codebase-qa/question.md`
against the three-file codebase under `corpus/codebase-qa/`. Standard four-phase flow
against the frozen rubric. Correctness (the exact attempt count) and Hallucination
(no invented dead-letter queue) are hard-fail eligible. Source transparency (citing
the right file/function) is load-bearing. Voice match does not apply. The corpus is
the directory `corpus/codebase-qa/`.
