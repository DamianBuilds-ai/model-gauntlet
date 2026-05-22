---
task_category: edge-case-enumeration
prompt_under_test: |
  You are given a single corpus file at
  corpus/edge-case-enumeration/spec-and-callers.md - the spec, current
  implementation, and 6 call sites of a fictional `parseTariff(raw)` function
  ("Quill" billing module). parseTariff takes a raw "<rate>/<unit>" string and
  returns a Tariff { rate, unit }.

  Your task: enumerate EVERY edge case parseTariff must handle, grounded in BOTH
  the spec rules (R1-R7) AND the inputs the 6 callers actually pass. For each edge
  case, state the input that triggers it, the expected correct behaviour, and
  whether the current implementation handles it. Be complete - a missed edge case
  is the failure this task measures.

  Output a numbered list of distinct edge cases. Do NOT invent edge cases the spec
  and callers do not support. Append the output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines after the list. No em dashes (use
  spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/edge-case-enumeration/
corpus_intent: |
  One corpus file (corpus/edge-case-enumeration/spec-and-callers.md): a parseTariff
  spec with 7 rules, the current implementation, and 6 call sites whose inputs
  exercise the rules. The eval measures whether a run enumerates the COMPLETE set of
  edge cases, including one buried case that neither the null guard nor a naive
  empty-string guard catches: a WHITESPACE-ONLY input ("  ") that is empty AFTER
  trim but non-empty as raw.

  QUALITY PRINCIPLE (completeness-first): the null case, the missing-separator case,
  the comma-separator case, and the negative-rate case are all signposted by the
  callers and easy to find. The scored signal is whether a run catches the
  whitespace-only / empty-after-trim case - it is NOT null (R4 misses it) and NOT
  empty-raw (a `raw === ""` check misses it), so a run reasoning only from the null
  guard or a naive empty check will drop it. Inventing edge cases the spec/callers
  do not support (e.g. unicode normalization, locale decimal commas beyond R7) is a
  precision error.

  ANSWER KEY (for the scoring Architect - the full enumerable list of edge cases):

    OBVIOUS / SIGNPOSTED edge cases (each tied to a caller and a rule):
      E1. null / undefined raw -> R4, return default { rate: 0, unit: "flat" }.
          Triggered by caller 2 (csvLoader, blank CSV cell). Handled by impl.
      E2. No "/" separator -> R5, malformed; unitPart is undefined and rate parses
          from the whole string. Triggered by caller 5 (spotQuote "9.99"). NOT
          properly rejected by impl (returns unit: undefined).
      E3. Comma thousands separator -> R7, "1,200.00/kWh". Triggered by caller 4
          (legacyFeed). Handled by impl via the comma strip.
      E4. Negative rate -> R2, "-3.00/credit" is INVALID per spec. Triggered by
          caller 6 (negativeAdjust). NOT rejected by impl (returns rate: -3).

    BURIED edge case (the discriminator):
      E5. WHITESPACE-ONLY raw "  " (empty-after-trim-but-non-empty-raw). Triggered
          by caller 3 (manualEntry, admin types only spaces). It is NOT null so R4's
          guard misses it; it is NOT an empty raw string so a `raw === ""` check
          misses it. After R6 trim it becomes "", split("/") yields [""],
          parseFloat("") is NaN, and unitPart is undefined - producing a silent
          { rate: NaN, unit: undefined } that no current guard catches. THIS is the
          buried item.

    ALSO ACCEPTABLE (lower-weight, derivable but not the discriminator):
      E6. Empty unit part after "/" (e.g. "12.50/") -> R3 violated, unit must be
          non-empty. (Derivable from R3; credit if listed, not penalized if folded
          into E2/E5.)

    PRECISION TRAPS (inventing these is a false positive): unicode normalization of
    the rate, locale-specific decimal separators beyond the R7 comma rule, multiple
    "/" separators changing unit semantics (the spec says unit is the substring
    after the FIRST "/", but this is defined behaviour, not an unhandled edge unless
    the run grounds it), scientific notation. None are supported as REQUIRED edge
    cases by the spec or callers.

  GREP-VERIFIABLE INVARIANTS (for the Architect, against the run's output):
    - A correct run names the whitespace-only / empty-after-trim case: grep -i
      "whitespace\|after trim\|trimmed.*empty\|only spaces\|\"  \"". MISSING this is
      the dropped buried item - the primary scored signal.
    - A correct run names: null/undefined (grep -i "null\|undefined"), the
      missing-separator case (grep -i "no.*slash\|missing.*separator\|no /\|without
      a slash"), the comma case (grep -i "comma\|thousands\|1,200"), and the
      negative-rate case (grep -i "negative").
    - PRECISION: no asserted REQUIRED edge case for unicode normalization or
      scientific notation. grep -i "unicode\|scientific notation" asserted as a must
      -handle edge is a false positive.

  Scoring guidance:
    - Buried-item catch (load-bearing) = did the run find the whitespace-only /
      empty-after-trim case (E5)? The single highest-signal bit.
    - Completeness = E1, E2, E3, E4 present + E5 present.
    - Precision (hallucination-eligible) = no invented unsupported edge case
      asserted as required.
    - Reasoning quality = E5 is correctly explained as distinct from both the null
      guard (R4) and a naive empty-string check.
    Voice match does NOT apply.
notes: |
  Chat A consistency-battery extension, eval 63 of 61-70. variant_pool 15 (3 models
  x N=5). THE SCORED SIGNAL IS WITHIN-FAMILY SPREAD across the 5 runs PLUS per-model
  buried-item catch-rate - NOT peak score. The question is whether one model family
  reliably catches the buried whitespace-only / empty-after-trim edge case (E5) on
  ALL 5 runs, or whether some runs drop it. Low spread with 5/5 catch beats high
  variance with a stronger single run.

  The corpus (corpus/edge-case-enumeration/spec-and-callers.md) is a parseTariff
  spec (7 rules), its implementation, and 6 call sites. Four obvious edge cases are
  each signposted by a caller (null CSV cell, missing separator, comma thousands
  separator, negative rate). ONE buried case is planted via the manual-entry caller:
  a whitespace-only input "  " that is neither null (so R4 misses it) nor an empty
  raw string (so a naive empty check misses it), becoming empty only after the R6
  trim and yielding a silent NaN/undefined Tariff. Precision traps (unicode,
  scientific notation) catch runs that pad the list with unsupported edge cases.
  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. The corpus
  is the directory corpus/edge-case-enumeration/.
---

# Spec 63 - edge-case-enumeration

Given a fictional `parseTariff(raw)` spec (7 rules), its implementation, and 6 call
sites, enumerate EVERY edge case the function must handle, grounded in both the spec
rules and the inputs the callers actually pass.

This is a Chat A consistency-battery eval (variant_pool 15, N=5). The scored signal
is WITHIN-FAMILY SPREAD across the five runs plus per-model buried-item catch-rate,
not peak score. The discriminator is one buried edge case: a WHITESPACE-ONLY input
("  ") supplied by the manual-entry caller. It is not null (so the R4 null guard
misses it) and not an empty raw string (so a naive `raw === ""` check misses it); it
becomes empty only after the R6 trim, yielding a silent { rate: NaN, unit: undefined }
that no current guard catches.

The four signposted edge cases (null CSV cell, missing "/" separator, comma thousands
separator, negative rate) are the shallow set every run should catch; finding them is
necessary but not sufficient. The corpus also invites precision traps - inventing
unicode-normalization or scientific-notation handling as required edge cases is a
false positive, since neither the spec nor any caller supports them. Standard
four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The answer key in
`corpus_intent` lists every true edge case plus grep-verifiable invariants. Voice
match does not apply. The corpus is the directory `corpus/edge-case-enumeration/`.
