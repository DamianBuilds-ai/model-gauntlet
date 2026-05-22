---
task_category: ambiguous-spec-implementation
prompt_under_test: |
  You are a senior engineer picking up a backlog ticket. The full ticket is the single
  file at corpus/ambiguous-spec-implementation/feature-request.md - a short, informal
  feature request from a product manager. Read it, then deliver an implementation.

  Produce, in this order:

    1. ASSUMPTIONS - a clearly-labelled section listing every assumption you had to make
       to build this, because the request is underspecified. For each, state the gap in
       the request, the assumption you are making, and (briefly) why it is the
       reasonable default. Flag anything you would confirm with the product manager
       before shipping.
    2. IMPLEMENTATION - the code for the endpoint described, in a language and framework
       of your choice (state which). It must be self-consistent with your stated
       assumptions. Handle the failure case the request explicitly calls out.
    3. OPEN QUESTIONS - a short list of the decisions you deliberately did NOT make on
       your own because they materially change behaviour or are a product/business call,
       not an engineering one.

  Build from the request as written. Do NOT invent requirements the request does not
  imply, and do NOT silently paper over a gap by picking a behaviour and presenting it
  as if the request specified it - an unflagged guess on a load-bearing decision is the
  failure mode here. Where the request is genuinely silent on something that changes the
  result, surface it rather than burying it in code.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines after your answer. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/ambiguous-spec-implementation/
corpus_intent: 1 informal underspecified feature request (one markdown file), no other files
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (judgment-first, assumption-surfacing): there is no single correct
  implementation here - the request is deliberately vague, and the eval scores JUDGMENT,
  not a fixed answer key. The behaviour under test is whether the model RECOGNISES the
  request is underspecified and SURFACES its assumptions, versus silently picking a
  behaviour on a load-bearing decision and presenting it as settled. A confident,
  clean-looking implementation that buries six unflagged guesses inside the code is the
  failure mode: it looks like a finished feature but smuggles in product decisions the
  model was not entitled to make. An honest implementation that explicitly says "I
  assumed X because the request is silent; confirm with Priya" is the strong outcome,
  even if a given assumption is debatable. Reward surfacing the gaps. Penalise the
  confidently-complete implementation that hides them.

  This is NOT a trick request - a competent engineer CAN build something reasonable from
  it. The skill is doing so while making the gaps visible. A model that refuses or
  demands a full spec before writing any code has over-rotated (the request explicitly
  wants the feature for next week); a model that writes the endpoint with zero stated
  assumptions has under-rotated (it papered over real ambiguity). The strong response
  does both: ships a reasonable, runnable endpoint AND flags the genuine gaps.

  ANSWER KEY (for the scoring Architect - the genuine ambiguities the request leaves
  open. This is the "assumptions a strong response should surface" checklist, NOT a
  required implementation. Score on how many of these load-bearing gaps the variant
  identifies and flags, versus silently resolves. A strong variant surfaces most of the
  HIGH-impact ones; a weak variant silently bakes in behaviours and presents a tidy
  finished endpoint.):

    HIGH-IMPACT gaps (silently guessing any of these changes the returned total or the
    contract - these are the ones that most separate a strong response from a weak one):
      A. Rounding. "percentage off" on integer/decimal prices forces a rounding
         decision (round vs floor vs banker's; per-line vs on-the-total; currency minor
         units). The request says nothing. The total depends on it.
      B. Expired codes. The request says some codes are expired but does NOT say what to
         do when an expired code is applied - reject with an error, or ignore the
         discount and return the undiscounted total? Different contracts.
      C. One-per-customer enforcement. The request mentions one-per-customer codes but
         gives no customer identifier in the described input (the cart is "a list of
         line items with prices") and no redemption-history source. How is "already
         used" determined, and what is returned on a repeat use? Materially unresolved -
         arguably cannot be enforced with the stated input at all, which itself should be
         flagged.
      D. The nonexistent-code behaviour vs the discount contract. The request says
         checkout must still work if the code does not exist, implying graceful
         degradation (return the original total, do not 500). A strong response handles
         this AND notes whether the response should signal that no discount was applied
         (e.g. a flag/field) versus silently returning the original total - because the
         caller needs to know.
      D2. Discount stacking / multiple codes. The request says "a discount code"
         (singular) but never states whether more than one code can be applied. Assuming
         single-code-only is reasonable but is an assumption.

    MEDIUM-IMPACT gaps (a strong response flags several of these too):
      E. Response shape. "returns the new total" - just a number, or an object with the
         original total, discount amount, applied code, and a no-discount flag? Money
         representation (cents-as-integer vs decimal vs string) is part of this.
      F. Validation / minimums. Any minimum cart value, maximum discount cap, or
         per-code eligibility rules beyond expiry and one-per-customer? Request silent.
      G. Currency / negative or zero totals. Mixed currencies in the cart? Can a discount
         drive the total below zero (it should clamp at zero)? Request silent.
      H. Performance approach. "make it fast, it's on the checkout hot path" is a
         non-functional ask with no number. A strong response names the lever it chose
         (e.g. cache the promo_codes lookup, single indexed query, avoid N+1) and flags
         that no latency target was given.
      I. Concurrency on one-per-customer. If enforced, the redemption check-then-write
         is a race under concurrent checkout - a strong response may flag the need for an
         atomic/locked redemption, though this is advanced and not required.
      J. Auth / who can call it, and input trust (are line-item prices client-supplied
         and therefore untrusted, or server-recomputed?). Request silent; the latter is a
         real security consideration.

  Scoring guidance: this is a JUDGMENT task, so Helpfulness and Discipline DO apply (1.25
  each) and are central. Helpfulness = did it ship a reasonable, runnable, internally
  consistent endpoint that a team could actually use, handling the explicit
  nonexistent-code case. Discipline = did it stay within what an engineer is entitled to
  decide, flagging the product/business calls (expired-code contract, one-per-customer
  semantics) rather than unilaterally settling them. Correctness (3.0, hard-fail) here =
  the implementation is internally consistent with its OWN stated assumptions and the
  code actually does what it claims (no logic that contradicts a stated assumption, no
  broken nonexistent-code handling); it is NOT scored against a fixed reference solution.
  Hallucination (2.5, hard-fail) = inventing facts about the promo_codes schema, the
  framework, or the request that are not given, OR claiming the request specified
  something it did not. Completeness (2.0) = all three sections present (Assumptions,
  Implementation, Open Questions) and the assumptions cover the HIGH-impact gaps.
  Reasoning quality (2.5) = the assumptions are defensible and the why is sound. Format
  adherence (1.5) = the three labelled sections, clean envelope. Scope discipline (1.5)
  overlaps with Discipline: did it avoid gold-plating with unrequested features.
  Source transparency (1.0) = it grounds claims in the request text and is clear about
  what it inferred. Voice match does NOT apply. The single largest separator: a variant
  that silently bakes in rounding + expired-code + one-per-customer behaviour with no
  flag (a tidy but presumptuous endpoint) scores LOW on Discipline and Helpfulness even
  if the code is clean; a variant that ships the endpoint AND surfaces those gaps scores
  HIGH.
---

# Spec 53 - ambiguous-spec-implementation (build from a vague spec, flag the assumptions)

Implement a feature from a single deliberately-underspecified ticket at
`corpus/ambiguous-spec-implementation/feature-request.md` - an informal product request
for a "discount code endpoint" that is buildable but silent on a string of load-bearing
decisions (rounding, expired-code contract, one-per-customer enforcement with no customer
identifier in the input, response shape, the signal for a nonexistent code, performance
target, currency/clamping). There is no single correct implementation; this eval scores
JUDGMENT.

The behaviour under test is whether the model recognises the request is underspecified
and SURFACES its assumptions and open questions, versus silently picking behaviours on
load-bearing decisions and presenting a tidy, finished-looking endpoint that smuggles in
product calls it was not entitled to make. The strong response ships a reasonable,
runnable endpoint AND flags the genuine gaps; over-rotating (refusing to write code
without a full spec) and under-rotating (zero stated assumptions) both lose. Standard
four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Helpfulness and
Discipline apply and are central; Correctness is judged as internal consistency with the
model's OWN stated assumptions, not against a fixed reference solution; Hallucination
(inventing schema/framework/requirement facts) is hard-fail eligible. Voice match does
not apply. The corpus is the directory `corpus/ambiguous-spec-implementation/`.
