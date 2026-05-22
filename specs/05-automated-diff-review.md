---
task_category: automated-diff-review
prompt_under_test: |
  You are given a pull-request diff at corpus/automated-diff-review/pr.diff for a
  fictional Go web service. Review it as a senior engineer would.

  Produce a structured review that:
    1. Lists each issue you find, classified by severity (blocker / major / minor),
       with the specific line or hunk it occurs in and WHY it is a problem.
    2. Distinguishes correctness/security bugs from style nits - lead with the
       dangerous ones.
    3. For each blocker, states the concrete fix in one sentence.
    4. Ends with an approve / request-changes verdict and a one-line justification.
  Do not invent issues that are not in the diff, and do not flag correct code as
  buggy. Output envelope required (schemaVersion, tier, status, tool_budget_used).
  No em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/automated-diff-review/pr.diff
notes: |
  New task type. The diff contains several planted issues: a SQL-injection via string
  concatenation in GetUser, a swallowed error (user, _ := scanUser), an off-by-one
  in ListTopUsers (for i := 0; i <= limit writes past a slice of length limit), and a
  missing nil/empty check on the session map lookup in Profile. A strong review catches
  all four and ranks the injection + the panic-prone loop + nil deref as blockers. Watch
  for: missed security issue (Correctness), false positives flagging correct code
  (Hallucination/Correctness), and severity mis-ranking (Reasoning/Helpfulness). This
  is a judgment task so Helpfulness and Discipline apply. Voice match does not.
---

# Spec 05 - automated-diff-review

Review the synthetic PR diff at `corpus/automated-diff-review/pr.diff`. Standard
four-phase flow against the frozen rubric. Correctness (catching the real bugs) and
Hallucination (not inventing nonexistent issues, not flagging correct lines) are the
hard-fail-eligible dimensions. Reasoning quality covers severity ranking; Helpfulness
covers whether the fixes are actionable. Voice match does not apply.
