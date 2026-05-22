---
task_category: greenfield-code-gen
prompt_under_test: |
  You are given a precise specification at corpus/greenfield-code-gen/spec.md for a
  single Python class: a thread-safe token-bucket rate limiter. Implement the class
  EXACTLY to the spec.

  Requirements:
    1. Match the documented public signatures exactly: the constructor
       TokenBucket(capacity, refill_rate, now=time.monotonic), and the methods
       try_acquire(tokens=1) -> bool and acquire(tokens=1) -> None (blocking).
    2. Handle every stated edge case: lazy time-based refill (tokens accrue at
       refill_rate per second, computed on read, never via a background thread),
       the burst cap (the bucket NEVER holds more than capacity tokens no matter how
       long it sits idle), reject-vs-block semantics (try_acquire returns False and
       does NOT mutate state on insufficient tokens; acquire sleeps until enough
       tokens accrue then deducts), the request-larger-than-capacity case (a request
       for more tokens than capacity can NEVER be satisfied - try_acquire returns
       False, acquire raises ValueError rather than blocking forever), and argument
       validation (capacity > 0, refill_rate > 0, tokens >= 1, all else raises
       ValueError).
    3. Make it thread-safe: concurrent callers must not double-spend tokens. Use a
       lock around the read-refill-deduct sequence.
    4. Write idiomatic Python. Inject the clock via the now callable so the class is
       testable without real sleeping. Do not add features the spec does not list
       (no metrics, no async variant, no decorator sugar).
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/greenfield-code-gen/spec.md
corpus_intent: |
  One spec file describing one class. Quality here is correctness-first: there is a
  single right behaviour for every stated edge case, and a subtly-wrong-but-plausible
  implementation is WORSE than an incomplete-but-correct one. The trap cases a weaker
  model can be CONFIDENTLY WRONG on (not merely incomplete): (a) refill math that
  accrues tokens as rate * elapsed but forgets to cap at capacity, so an idle bucket
  silently over-fills and grants a burst larger than the contract allows; (b)
  try_acquire that deducts-then-checks (or otherwise mutates state) on the reject
  path, leaking tokens; (c) the request-larger-than-capacity case implemented as a
  blocking acquire that loops forever instead of raising ValueError - a plausible
  reading that deadlocks; (d) computing refill from wall-clock time.time() instead of
  the injected monotonic now, or not persisting the last-refill timestamp, so refill
  is wrong across calls; (e) a lock that wraps only the deduct but not the
  read-refill, leaving a check-then-act race. A confident wrong answer ships a class
  that looks complete and passes a naive happy-path test but violates the burst cap or
  deadlocks - that is the differentiator, not missing methods.
notes: |
  New task type. Greenfield implementation from an exact spec (no source to port, no
  bug to find - pure construct-to-contract). Differentiates on algorithm correctness
  (lazy refill + burst cap math), edge-case fidelity (the five trap cases in
  corpus_intent), thread-safety reasoning (lock placement around read-refill-deduct,
  not just deduct), and idiomatic Python (clock injection actually used, no
  spec-creep features). Correctness is hard-fail eligible - an implementation that
  over-fills past capacity or deadlocks on the oversized-request case is wrong, not
  just stylistically weaker. Hallucination is hard-fail eligible - inventing a
  threading or time API that does not exist (for example a nonexistent Lock method)
  fabricates a standard-library call. Reasoning quality covers whether the variant
  explains the read-refill-deduct ordering and the cap. Source transparency: does it
  note which spec edge cases drove which lines. Voice match does not apply.
---

# Spec 10 - greenfield-code-gen

Implement the thread-safe token-bucket rate limiter described in
`corpus/greenfield-code-gen/spec.md`. Standard four-phase flow against the frozen
rubric. This is a construct-to-contract task: a single correct behaviour exists for
every edge case, so Correctness and Hallucination (no invented threading or timing
APIs) are the load-bearing, hard-fail-eligible dimensions. Reasoning quality covers
the refill-and-cap math and the lock-placement argument; Completeness covers whether
all five trap edge cases are handled. The decisive split is between a class that is
confidently wrong (over-fills the burst cap, deadlocks on an oversized request, or
leaks tokens on the reject path) and one that is correct, since a plausible-looking
wrong limiter is worse than a smaller correct one. Voice match does not apply.
