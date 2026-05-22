---
task_category: tone-voice-rewrite
prompt_under_test: |
  You are given a single blunt, frustrated internal message at
  corpus/tone-voice-rewrite/blunt-pr-rant.md - an engineer venting in a private DM about
  a colleague's pull request. It is harsh in tone but contains several concrete technical
  complaints and one explicit request (the "ask").

  Rewrite the message so it is diplomatic and professional - suitable to post in a shared
  team channel where the colleague being discussed could read it. Requirements:
    1. Preserve ALL of the concrete technical facts. Every specific issue raised must
       survive the rewrite, with its specifics intact (file names, function names, the
       nature of each defect). Do not generalise a specific defect into a vague "some
       issues".
    2. Preserve the core ask. The original asks for a specific action - keep that request
       explicit and unambiguous. Do not drop it, and do not soften it into a non-request.
    3. Shift the TONE only: remove the blame, sarcasm, exasperation, and personal jabs.
       Make it constructive and collegial.
    4. Do NOT over-soften into vague mush. "There may be a few things worth a look" is a
       failure - the rewrite must still clearly communicate that these are real,
       specific, blocking problems, just stated professionally. Diplomatic does not mean
       non-committal.
    5. Do not invent new technical issues, new severities, or facts not present in the
       original.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em dashes
  (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/tone-voice-rewrite/blunt-pr-rant.md
corpus_intent: |
  One blunt internal message containing four concrete technical complaints plus one
  explicit ask, to be rewritten diplomatically WITHOUT losing any fact or the request.
  Quality here is correctness-first (no-wrong-answers): a polished, friendly rewrite that
  silently drops a technical fact, generalises a specific defect into vagueness, or
  softens the explicit ask into a non-request is WORSE than a blunter rewrite that keeps
  everything intact - because the polished-but-lossy version reads as complete and a
  reader would trust it carries the original meaning when it does not. The two failure
  poles a weaker model can be CONFIDENTLY WRONG on: (a) OVER-SOFTENING - turning "this is
  a double-charge liability sitting in plain sight" into "there might be a small edge case
  worth considering", or turning the explicit "have a word with them / pair them with
  someone senior" ask into "maybe we could chat sometime", which guts the message while
  looking diplomatic; and (b) FACT LOSS - collapsing the four distinct issues (missing
  migration down(), missing transaction around charge+insert, the N+1 in the serializer,
  zero tests on the refund branch) into a generic "a few code quality things", dropping
  the specifics (file/function names, why each matters) that make the complaints
  actionable. A confident wrong answer ships a warm, professional-sounding message that a
  reader would happily post - but it has quietly lost a blocking defect or defanged the
  request. That is the differentiator, not prose polish. The reverse failure also exists:
  a rewrite that preserves every fact but stays harsh / blaming has not done the task
  either (tone was the point). The win is BOTH - genuine tone shift AND full fidelity.
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a subtly-wrong-but-plausible
  rewrite that distorts the message is WORSE than a blunter-but-faithful one. A rewrite
  that keeps every technical fact and the explicit ask while being only moderately
  diplomatic is correct; a rewrite that sounds beautifully professional but has dropped
  the refund-tests issue, or generalised the four defects into "a few things", or turned
  the ask into a vague suggestion, is confidently-wrong output that a reader would post
  believing it carries the original meaning. Reward faithful-and-diplomatic. Penalise the
  polished-but-lossy rewrite hardest.

  NEW task type. Tests tone transformation under a strict fidelity constraint - genuine
  register shift (harsh -> diplomatic) WITHOUT content loss and WITHOUT over-softening
  into non-commitment. Single source message. The differentiation is whether a model can
  change the TONE while holding the FACTS and the ASK rigid - most models can do one or
  the other; the split is doing both.

  ANSWER KEY (for the scoring Architect - what a correct rewrite MUST preserve):

  The FOUR concrete technical facts (all four must survive, each with its specifics; a
  rewrite missing any one is incomplete, and one generalised into vagueness is a
  Correctness miss):
    1. MIGRATION NOT REVERSIBLE - the migration 0047_add_idempotency_key.py has no down()
       method, so a prod rollback would require hand-writing SQL (ties back to a prior
       "March incident" they vowed not to repeat). The file name and the missing-down()
       specific should survive; "the migration isn't reversible" is acceptable, "some
       migration concerns" is too vague.
    2. NO TRANSACTION AROUND CHARGE + WRITE - the new charge_card() path does not wrap the
       Stripe charge and the DB insert in a single transaction, so a charge-succeeds /
       insert-fails sequence takes the customer's money with no order record (a
       double-charge / lost-order liability). The "not atomic / no transaction" specific
       and the money-without-record consequence should survive.
    3. N+1 QUERY REGRESSION - OrderSummary.line_items lazy-loads inside the serializer
       loop, so a 50-item order fires ~50 queries; violates the team's
       select_related/prefetch_related agreement for serializers. The N+1 nature should
       survive (file/field name is a bonus; "a query-performance regression in the
       serializer" is acceptable, "performance could be better" is too vague).
    4. NO TESTS ON THE REFUND BRANCH - issue_refund() (the money-moving-the-other-way
       path) has zero test coverage, while the happy path is tested; violates the hard
       rule against shipping money-moving code untested. The "refund path has no tests"
       specific should survive.

  The ONE explicit ASK (must remain an explicit, actionable request - not softened into a
  non-request): before the next review, either (a) have a word with Riley, OR (b) pair
  Riley with a senior engineer on the next payments PR. Either phrasing of the same ask is
  fine; dropping it, or reducing it to "maybe we could touch base", is a fail on
  Completeness / Correctness.

  Scoring guidance:
    - Correctness (hard-fail eligible) = did every technical fact survive ACCURATELY and
      did the ask remain an actual request. A rewrite that INVERTS or distorts a fact
      (e.g. says the transaction issue is "minor" when it is a money liability, or says
      tests exist when the point is they do not) scores 1. Over-softening that guts a fact
      into meaninglessness is a Correctness miss, not just a Voice nicety.
    - Completeness = all four issues present AND the ask present. Missing one issue or the
      ask drops the score.
    - Voice match (APPLIES here - this is a voice/tone task) = against the implicit anchor
      "diplomatic, professional, collegial, team-channel-safe". Score the genuineness of
      the tone shift: 5 = reads as a respectful peer raising blocking issues; 3 = polite
      but still a bit pointed; 1 = still blaming/sarcastic OR swung so far into mush it no
      longer reads as raising real problems. Note: over-softening hits BOTH Voice (false
      register - "nice" is not the same as "professional and clear") AND Correctness (fact
      defanged).
    - Hallucination (hard-fail eligible) = inventing a fifth issue, a severity not stated,
      a name/system not present, or fabricating that something was already fixed/agreed.
    - Helpfulness + Discipline (APPLY - this has a judgment character): Helpfulness = is
      the rewrite actually usable as-is in a team channel. Discipline = did it stay a
      rewrite (not editorialise, not add an unrequested apology on Sam's behalf, not
      escalate beyond the stated ask).
    - Source transparency applies weakly (single source). Format adherence = clean
      rewritten message plus the required envelope.
---

# Spec 19 - tone-voice-rewrite (diplomatic register, full fidelity)

Rewrite one blunt, frustrated internal engineering message at
`corpus/tone-voice-rewrite/blunt-pr-rant.md` into a diplomatic, team-channel-safe form -
while preserving all four concrete technical complaints (a non-reversible migration, a
missing transaction around a charge-and-write, an N+1 in a serializer, and an untested
refund branch) and the one explicit ask (have a word with the colleague, or pair them
with a senior on the next payments PR), and without over-softening any of it into vague
non-commitment.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a model that keeps every
fact and the ask while only moderately diplomatic is correct, whereas a model that
produces a beautifully professional message that has quietly dropped a blocking defect or
defanged the request has produced output a reader would post believing it carries the
original meaning when it does not - which is worse than a blunter, faithful rewrite.
Correctness and Hallucination are hard-fail eligible. The decisive split is between a
rewrite that achieves a genuine tone shift AND full fidelity versus one that trades one
for the other - over-softening into mush at one pole, or preserving facts but staying
harsh at the other. Voice match APPLIES here (the tone shift is the task). The corpus is
the single message file.
