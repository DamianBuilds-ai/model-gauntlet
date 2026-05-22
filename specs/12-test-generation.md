---
task_category: test-generation
prompt_under_test: |
  You are given a Python module at corpus/test-generation/money.py - a small
  money/rounding utility with several public functions. Write a pytest test suite for
  it.

  Requirements:
    1. Cover the documented BEHAVIOUR of every public function, including the edge
       cases each one's docstring calls out (banker's rounding at the .5 boundary,
       splitting a total into N shares with the remainder distributed deterministically
       so the shares sum back to the original, parsing of dollar strings, and the
       handling of negative amounts).
    2. Assert the CORRECT expected values. A test that asserts a wrong expected value
       is worse than a missing test - it bakes a bug in. Reason about what each
       function actually returns before writing the assertion (especially banker's
       rounding, where round-half-to-even means 2.5 cents -> 2 and 3.5 cents -> 4, and
       the split function, where the shares must sum exactly to the input).
    3. Do NOT test private helpers (any name beginning with an underscore). Test only
       the public surface.
    4. Use plain pytest (functions named test_*, plain assert, parametrize where it
       reduces duplication). Do not introduce mocks or fixtures the module does not
       need.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/test-generation/money.py
corpus_intent: |
  One module with several public functions and one private helper. Quality is
  correctness-first: the suite must assert TRUE expected values, and a confidently
  wrong assertion (a green test encoding a false expectation) is WORSE than an omitted
  case. The traps a weaker model is likely to be confidently wrong on (not merely
  incomplete): (a) banker's rounding - the module uses round-half-to-even, so a model
  that assumes round-half-up will assert round_cents(2.5)==3 (wrong; it is 2) and
  round_cents(3.5)==4 (right by luck), encoding a false belief that passes on one case
  and would fail on the module; the discriminating test pins BOTH 2.5 and 3.5; (b)
  split_amount - the remainder must be distributed so the shares sum exactly to the
  total (splitting 100 cents 3 ways yields [34, 33, 33], not [33, 33, 33] which loses
  a cent, nor [33.33, 33.33, 33.33]); a model that asserts an even split is
  confidently wrong; (c) negative amounts - the docstrings define behaviour for
  negatives (round toward even still, split distributes the remainder on the negative
  side), and a model may assume a guard that does not exist; (d) parse_dollars edge
  inputs (whitespace, a leading dollar sign, more than two decimal places) where the
  documented behaviour is specific. The instruction-following gate also bites here:
  testing the private _normalise helper is an explicit violation. An incomplete suite
  that covers fewer cases but asserts every one correctly beats a broad suite with a
  wrong banker's-rounding or even-split assertion.
notes: |
  New task type. Test authoring against a module with non-obvious numeric edge cases.
  Differentiates on coverage (does it test every public function and the called-out
  edge cases), edge-case correctness (the banker's-rounding .5 boundary and the
  remainder-distribution invariant in split_amount are where a model encodes a false
  expectation), assertion correctness (asserting the TRUE return value, not the
  intuitive-but-wrong one), and scope discipline (NOT testing the private _normalise
  helper, which is an explicit instruction and feeds the binary instruction-following
  gate). Correctness is hard-fail eligible - a suite whose assertions encode wrong
  expected values is wrong, not merely thin, and is worse than a smaller all-correct
  suite. Hallucination is hard-fail eligible - testing a function that does not exist
  in money.py or importing a symbol the module does not export. Reasoning quality
  covers whether the variant reasons out the expected value before asserting. Voice
  match does not apply. The corpus is corpus/test-generation/money.py.
---

# Spec 12 - test-generation

Write a pytest suite for `corpus/test-generation/money.py`. Standard four-phase flow
against the frozen rubric. The module has several public functions with non-obvious
numeric edge cases (round-half-to-even, deterministic remainder distribution in an
N-way split, negative-amount handling, dollar-string parsing) and one private helper
that must NOT be tested. Correctness is hard-fail eligible - the decisive split is
between a suite that asserts TRUE expected values and one that encodes a false
expectation (for example asserting round-half-up at the .5 boundary, or an even split
that loses a cent), since a green test baking in a wrong expectation is worse than an
omitted case. Hallucination (testing a nonexistent function) is hard-fail eligible,
and testing the private `_normalise` helper trips the binary instruction-following
gate. Reasoning quality covers whether the variant computes the expected value before
asserting it; Completeness covers edge-case coverage. Voice match does not apply.
