---
task_category: multi-constraint-satisfaction
prompt_under_test: |
  You are given a Python module at
  corpus/multi-constraint-satisfaction/processor.py - the withdrawal processor
  for a fictional "Acme Wallet" - and a list of twelve constraints at
  corpus/multi-constraint-satisfaction/constraints.md that the refactored module
  must satisfy.

  Refactor the process(account_id, amount, idempotency_key) method so that ALL
  TWELVE listed constraints (C1 through C12) hold SIMULTANEOUSLY. Several of the
  constraints interact or near-conflict (for example, the atomicity constraint
  tensions with the no-network-call-under-lock constraint, the idempotency
  constraint tensions with the record-every-attempt constraint, and the
  per-account-concurrency constraint tensions with a naive global lock). You must
  hold all twelve at once - do NOT satisfy some at the expense of others.

  Rules:
    - Do not change the collaborator interfaces (ledger, fraud_client, audit_log)
      described in constraints.md.
    - Output the complete refactored module as a single Python code block.
    - After the code, include a short checklist mapping each constraint C1..C12 to
      the line(s) or construct in your code that satisfies it, so the satisfaction
      is verifiable. Do not claim a constraint is satisfied if your code does not
      actually satisfy it - a confidently-wrong "satisfied" claim is worse than
      omitting the claim.
    - Do not introduce new constraint violations while fixing others.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/multi-constraint-satisfaction/
corpus_intent: 1 module to refactor plus 1 constraints file listing 12 simultaneous requirements
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-STRESS PROBE (simultaneous-constraint load / forgetting-under-load). This
  tests the failure mode where a model, while focusing on satisfying some
  constraints, silently drops or violates others - the cross-matching load is
  holding all twelve in working memory at once while they tension against each
  other. At small constraint counts every model holds them; the hypothesis is that
  with twelve interacting constraints the cheaper models satisfy a subset and
  quietly break the rest (recall failure) or claim satisfaction they did not
  achieve (precision failure). Run the full 9-variant model-only pool (Haiku x3,
  Sonnet x3, Opus x3; effort treated as inert per the methodology). Aggregate the
  3 passes per model (mean weighted total); flag any model whose 3 passes diverge
  by more than 0.5 as a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  satisfaction claim is worse than an unmet constraint honestly flagged. A model
  that asserts "C4 satisfied" while its fraud check still runs under the lock has
  produced code an engineer would ship believing it correct - worse than a model
  that says "I could not hold C4 with C3". The discriminator is the COUNT of
  constraints actually satisfied in the code (verified against the code, not the
  model's self-report), with self-reported-but-violated constraints penalised
  hardest.

  SATISFIABILITY: all twelve constraints ARE simultaneously satisfiable - a
  reference solution exists (per-account lock for atomicity + parallelism, fraud
  check before the lock, replay short-circuit before any audit record, success
  audit inside the lock after the debit, propagating exceptions via a structure
  that still records the attempt). There is no mutually-exclusive pair. A model
  that claims two constraints conflict and drops one is wrong - they all hold.

  ANSWER KEY (for the scoring Architect - the 12 constraints as a verifiable
  checklist; mark each SATISFIED or VIOLATED by reading the model's refactored
  code, NOT its self-report):

    C1 - INPUT VALIDATION: amount <= 0 raises ValueError before any other work.
         VIOLATED if zero or negative amounts are processed or a different
         exception type is used. (Starting code: VIOLATED - no validation.)
    C2 - BALANCE CHECK: amount > balance raises InsufficientFunds; never overdraws.
         (Starting code: SATISFIED in spirit but unguarded - see C3.)
    C3 - ATOMIC READ-MODIFY-WRITE: get_balance and debit are atomic w.r.t.
         concurrent same-account calls (both under one lock, no TOCTOU gap).
         VIOLATED if the balance is read outside the lock then debited inside, or
         no lock guards the pair. (Starting code: VIOLATED - read is outside the
         lock.)
    C4 - NO NETWORK UNDER LOCK: fraud_client.check does NOT run while the
         read-modify-write lock is held. VIOLATED if check() is called inside the
         locked region. (Starting code: VIOLATED - check() is under the lock.)
         This is the C3-vs-C4 tension; the resolution is fraud-check-first, then
         lock only the read+debit.
    C5 - IDEMPOTENCY: a repeat call with the same idempotency_key does NOT debit
         again and returns the same result. VIOLATED if the key is ignored or a
         replay debits a second time. (Starting code: VIOLATED - _seen never used.)
    C6 - RECORD EVERY ATTEMPT: audit_log.record is called once for every executing
         call including fraud-rejected and insufficient-funds / invalid outcomes,
         but NOT for an idempotent replay (the replay returns the cached result
         without a second record). VIOLATED if only successes are recorded, OR if a
         replay records a duplicate entry. (Starting code: VIOLATED - records only
         success.) This is the C5-vs-C6 tension.
    C7 - NO DEBIT ON FRAUD REJECT: fraud False returns a rejected result with no
         debit. VIOLATED if a debit can occur after a False fraud check. (Starting
         code: SATISFIED.)
    C8 - NO PARTIAL STATE ON FAILURE: no "ok" audit entry is written for a
         withdrawal whose debit did not complete; success audit follows the debit.
         VIOLATED if the success record is written before/independently of the
         debit such that a post-read failure leaves a false "ok". (Starting code:
         BORDERLINE - audit is outside the lock after debit; acceptable, but a
         refactor that records "ok" before debiting VIOLATES.)
    C9 - PER-ACCOUNT CONCURRENCY: different accounts proceed in parallel; no single
         global lock serialises all withdrawals. VIOLATED if one shared
         threading.Lock guards all accounts. (Starting code: VIOLATED - single
         self._lock for everything.) This is the C3-vs-C9 tension; resolution is a
         per-account lock (e.g. a dict of locks).
    C10 - RETURN SHAPE: success dict has status == "ok", amount, account_id, AND
          idempotency_key echoed; fraud reject has status == "rejected". VIOLATED
          if idempotency_key is missing from the success result or the status
          strings are wrong. (Starting code: VIOLATED - idempotency_key not echoed.)
    C11 - NO BUSY-WAIT / NO SLEEP: no time.sleep, no polling loop. VIOLATED if
          time.sleep or a spin loop remains. (Starting code: VIOLATED - time.sleep(0)
          placeholder present.)
    C12 - NO SWALLOWED EXCEPTIONS: ValueError and InsufficientFunds propagate; no
          bare except or except Exception: pass hides errors. VIOLATED if a
          try/except suppresses the raised exceptions (e.g. a finally that returns,
          or a bare except). (Starting code: SATISFIED - no swallowing.) This is the
          C6/C8-vs-C12 tension - a try/finally for audit must not suppress the raise.

  Net: the starting code VIOLATES C1, C3, C4, C5, C6, C9, C10, C11 (8 of 12) and
  satisfies C2, C7, C8, C12 (4 of 12). A correct refactor satisfies all 12. The
  score tracks how many of the 12 a model's refactor genuinely holds.

  Scoring guidance:
    - Completeness (weight 2.0) = count of the 12 constraints the refactored code
      actually satisfies (verified by reading the code). 12/12 is exemplary; each
      genuinely-unmet constraint drops the score. This is the primary discriminator.
    - Correctness (hard-fail eligible) = does the refactor run as valid Python and
      preserve the happy-path behaviour. A refactor that satisfies constraints but
      breaks the basic withdrawal flow fails Correctness.
    - Hallucination (hard-fail eligible) = claiming a constraint is satisfied when
      the code does NOT satisfy it (the canonical confidently-wrong here), or
      inventing a collaborator method that does not exist. A self-report that says
      "all 12 satisfied" over code that holds 8 is the heaviest penalty.
    - Reasoning quality = did the model correctly resolve the four tensions (C3/C4,
      C5/C6, C3/C9, C8/C12) rather than satisfying one side and breaking the other.
      This is where Opus is hypothesised to separate - holding all twelve at once.
    - Discipline = stayed in scope (refactored process(), did not change
      collaborator interfaces, did not invent constraints).
    - Format adherence = output envelope + a single code block + the per-constraint
      verification checklist.
    - Source transparency = the checklist maps each constraint to the construct
      that satisfies it.
    Constraint-satisfaction count and zero false satisfaction-claims are the scored
    discriminators. Voice match does NOT apply.
---

# Spec 23 - multi-constraint-satisfaction (the twelve-simultaneous-constraints probe)

The simultaneous-constraint analog of the cross-reference probe: can a model hold
twelve interacting requirements in working memory at once and satisfy ALL of them
in one refactor, rather than satisfying a subset and silently breaking the rest.

The corpus (`corpus/multi-constraint-satisfaction/`) is a deficient withdrawal
processor for a fictional "Acme Wallet" (`processor.py`) plus a list of twelve
constraints (`constraints.md`) the refactor must satisfy. The constraints are
engineered with four genuine tensions - atomic read-modify-write versus no network
call under the lock, idempotency versus record-every-attempt, per-account
concurrency versus a naive global lock, and guaranteed audit versus no swallowed
exceptions - so a model cannot satisfy one side of a tension by sacrificing the
other. All twelve ARE simultaneously satisfiable (a reference solution exists with
no mutually-exclusive pair); the starting code satisfies only 4 of the 12.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong "constraint
satisfied" claim over code that does not satisfy it is worse than an honestly
flagged miss, because it is code an engineer would ship believing it correct.
Completeness (the COUNT of constraints genuinely satisfied, verified against the
code rather than the self-report) and Hallucination (false satisfaction claims)
are the scored discriminators - not the elegance of the prose, since elegance is
where Opus tied Sonnet on the earlier consolidation eval. Reasoning quality
captures whether the model resolved the four tensions correctly. The variant pool
is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
directory `corpus/multi-constraint-satisfaction/`.
