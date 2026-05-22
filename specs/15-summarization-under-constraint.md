---
task_category: summarization-under-constraint
prompt_under_test: |
  You are given a single engineering post-mortem at
  corpus/summarization-under-constraint/postmortem.md (about 2000 words) describing an
  outage at a company called Tessellate.

  Write a summary of the post-mortem in 150 words or fewer. This is a HARD cap: the
  body of your summary must not exceed 150 words. The summary MUST cover all three of
  these points, and only these:
    1. What broke and the customer impact (what was unavailable, and for how long).
    2. The root cause (be accurate about WHY it happened - what the actual triggering
       value was and why it had the effect it did).
    3. The single most important remediation the team committed to.

  Constraints:
    - Plain language. Explain it so a non-engineer manager could follow it. Do not use
      unexplained jargon (no bare "429", "canary", "rate limiter" without a plain-
      language gloss).
    - Prose only. Write flowing sentences in one or more short paragraphs. Do NOT use
      bullet points, numbered lists, or headings inside the summary.
    - Faithful only. Include only what the post-mortem actually says. Do not add
      severity judgments, blame, recommendations, or causes the document does not state.
    - State your final word count on a separate line after the summary (e.g. "Word
      count: 138").
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/summarization-under-constraint/
corpus_intent: 1 post-mortem article (~2000 words)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a fluent summary that
  subtly distorts the root cause is WORSE than a plainer one that gets it right. The
  post-mortem's load-bearing subtlety is that a rate-limit value of ZERO meant "reject
  every request", NOT "no limit / unlimited" - the document explicitly flags "zero means
  off" as the trap that fooled people in the room. A weaker model that writes "the limit
  was accidentally removed" or "set to unlimited" has produced a confident, plausible,
  and WRONG summary that inverts the cause. Reward the faithful summary; penalise the
  plausible-but-inverted one hardest. Faithfulness failures here are a Correctness
  problem; adding claims the article does not make is a Hallucination problem.

  NEW task type. Tests hard-constraint adherence (the 150-word cap and prose-only / no-
  bullets rule are objectively checkable), faithfulness under compression, and resistance
  to adding unsupported claims. Single ~2000-word source.

  ANSWER KEY / what a faithful summary must get right (for the scoring Architect):
    - WHAT BROKE: the checkout service was fully down for 47 minutes during evening
      peak; customers could browse and add to cart but could not pay. (~18,000 attempts
      rejected; low-six-figure revenue loss - optional given the word budget.)
    - ROOT CAUSE (the critical fidelity point): a config change meant to RAISE the
      per-customer limit to 10,000 instead committed 0 (a dropped leading digit), and
      the limiter treated 0 as "reject all requests", not "unlimited". It slipped
      through because CI checked the value was a valid non-negative integer but did not
      range-check it, and the canary stage masked the spike. A summary that says the
      limit was "removed", "disabled", "set to unlimited", or "set too high" has
      INVERTED the cause and is confidently-wrong.
    - TOP REMEDIATION: add a range check to the rate-limiter config validation (reject
      any limit below a sane floor) - explicitly the highest-priority / primary fix. A
      summary that elevates a lower-priority item (incident-channel diff posting,
      playbook step, dashboard panel) as THE main fix has missed the document's own
      ranking.
    - MUST NOT ADD: blame on an individual, a security angle (there was none), data
      loss (there was none), or a claim that the two-person rule should change (the
      doc explicitly says it should NOT). Adding any of these is an unsupported claim.

  Scoring guidance: Format adherence is unusually load-bearing here and objectively
  checkable - count the words (over 150 = constraint violation, weigh heavily; a small
  overage of a few words is a softer ding than a 200-plus-word answer), and check for
  prose-only (any bullet/numbered list/heading inside the summary is a violation).
  Correctness = root-cause fidelity (the zero-means-reject point) plus covering all
  three required points. Completeness = all three points present. Hallucination
  (hard-fail) = adding claims the article does not make (security, data loss, blame).
  Discipline = staying inside the word cap and the no-bullets / faithful-only rules.
  Helpfulness = is it actually usable by a non-engineer manager (plain language, jargon
  glossed). Reasoning quality = correct identification of the SINGLE top remediation.
  Voice match does NOT apply.
---

# Spec 15 - summarization-under-constraint (hard word cap + faithful compression)

Summarize a ~2000-word fictional outage post-mortem
(`corpus/summarization-under-constraint/postmortem.md`) in 150 words or fewer, covering
exactly three required points (what broke and the impact, the accurate root cause, and
the single top remediation), in plain jargon-free prose with no bullet points. The
source is rich and detailed precisely so a weaker model is tempted to blow the word cap,
add claims the article never makes (a security angle, data loss, individual blame), or
distort the load-bearing root cause - the post-mortem itself flags that a limit value of
zero meant "reject everything", NOT "unlimited", and that the "zero means off" intuition
is the exact trap.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a fluent summary that inverts the cause
("the limit was removed / set to unlimited") is worse than a plainer one that gets it
right. Format adherence (the objectively-checkable 150-word cap and prose-only rule),
Correctness (root-cause fidelity plus the three required points), and Hallucination
(no added claims) are the load-bearing dimensions; Discipline covers staying inside the
constraints. Voice match does not apply. The corpus is the directory
`corpus/summarization-under-constraint/`.
