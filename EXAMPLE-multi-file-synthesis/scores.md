# Sealed scoring - EXAMPLE-multi-file-synthesis

Scored against `rubric/rubric.md` (frozen v1). Pass 1 is sealed: each variant was
scored dimension-by-dimension with the identity in `variants/key.md` NOT yet opened.
The reveal happens in `tally.md`.

## Applicable dimensions for this task

This is a multi-file SYNTHESIS task (not a drafting/voice task and not pure
retrieval). Dimensions scored and their weights (from the frozen rubric):

| # | Dimension | Weight | Applies here? |
|---|-----------|--------|---------------|
| 1 | Correctness | 3.0 | yes (hard-fail eligible) |
| 2 | Completeness | 2.0 | yes |
| 3 | Format adherence | 1.5 | yes |
| 4 | Scope discipline | 1.5 | yes |
| 5 | Reasoning quality | 2.5 | yes (cross-file connection is the core ask) |
| 6 | Hallucination | 2.5 | yes (hard-fail eligible) |
| 7 | Voice match | 2.0 | NO - excluded from denominator (not a voice task) |
| 8 | Helpfulness | 1.25 | yes (judgment task) |
| 9 | Discipline | 1.25 | yes (judgment task) |
| 10 | Source transparency | 1.0 | yes |

Denominator = sum of applied weights = 3.0 + 2.0 + 1.5 + 1.5 + 2.5 + 2.5 + 1.25 +
1.25 + 1.0 = 16.5. Voice match (2.0) is excluded.

Scale anchors (mandatory): 1 fails the dimension, 2 partial with meaningful gaps,
3 meets the bar, 4 strong, 5 exemplary.

---

## Per-variant scores

### Variant A
| Dim | Score |
|-----|-------|
| Correctness | 5 |
| Completeness | 5 |
| Format adherence | 4 |
| Scope discipline | 5 |
| Reasoning quality | 4 |
| Hallucination | 5 (no fabrication) |
| Helpfulness | 4 |
| Discipline | 5 |
| Source transparency | 4 |

Weighted total = (5*3.0 + 5*2.0 + 4*1.5 + 5*1.5 + 4*2.5 + 5*2.5 + 4*1.25 + 5*1.25
+ 4*1.0) / 16.5 = (15 + 10 + 6 + 7.5 + 10 + 12.5 + 5 + 6.25 + 4) / 16.5 = 76.25 /
16.5 = **4.62**.
Binary gate: PASS (envelope present, no em dashes, in scope).
Qualitative: Captures all three cross-file threads and ties every recommended
action to a ticket or roadmap item. Tight and accurate with light source labels.
Slightly less visually scannable than D but loses nothing on substance.

### Variant B
| Dim | Score |
|-----|-------|
| Correctness | 2 |
| Completeness | 3 |
| Format adherence | 4 |
| Scope discipline | 3 |
| Reasoning quality | 3 |
| Hallucination | 1 (HARD FAIL - fabricates SOC 2 audit, v3.2.1 hotfix, GraphQL pricing) |
| Helpfulness | 2 |
| Discipline | 2 |
| Source transparency | 2 |

Binary gate: PASS (envelope present), BUT Hallucination = 1 is a hard-fail.
Weighted total not ranked (eliminated). For transparency the raw weighted total
would be (2*3.0 + 3*2.0 + 4*1.5 + 3*1.5 + 3*2.5 + 1*2.5 + 2*1.25 + 2*1.25 + 2*1.0)
/ 16.5 = (6 + 6 + 6 + 4.5 + 7.5 + 2.5 + 2.5 + 2.5 + 2) / 16.5 = 39.5 / 16.5 = 2.39,
but it CANNOT win (Hallucination hard-fail per rubric section 3).
Qualitative: Reads fluently and would pass a careless review, which is exactly why
it is dangerous. It invents a SOC 2 deadline, a phantom v3.2.1 hotfix, and GraphQL
pricing - none in the corpus. The textbook reason sealed scoring weights
hallucination as a hard-fail.

### Variant C
| Dim | Score |
|-----|-------|
| Correctness | 4 |
| Completeness | 3 |
| Format adherence | 1 |
| Scope discipline | 4 |
| Reasoning quality | 4 |
| Hallucination | 5 (no fabrication) |
| Helpfulness | 3 |
| Discipline | 2 |
| Source transparency | 3 |

Binary gate: FAIL - the required output envelope frontmatter (schemaVersion, tier,
status, tool_budget_used) is absent. Per rubric section 2 a gate FAIL eliminates
the variant from winner contention regardless of content quality.
Weighted total not ranked (eliminated on the binary gate).
Qualitative: The substance is honestly decent - accurate, no fabrication, identifies
the right themes. It is eliminated purely because it ignored the explicit envelope
instruction. A clean illustration that following the contract is itself scored: good
content does not rescue a gate FAIL.

### Variant D
| Dim | Score |
|-----|-------|
| Correctness | 5 |
| Completeness | 5 |
| Format adherence | 5 |
| Scope discipline | 5 |
| Reasoning quality | 5 |
| Hallucination | 5 (no fabrication) |
| Helpfulness | 5 |
| Discipline | 5 |
| Source transparency | 5 |

Weighted total = 5.0 across the board = **5.00**.
Binary gate: PASS.
Qualitative: The strongest output. The cross-file thread table makes the
connective tissue immediately legible, the top-3 ranking explicitly reasons about
COMBINED urgency (active impact plus decided-or-undecided fix path) rather than just
restating ticket severity, and every action cites its evidence. Exemplary on the
core ask of synthesis-over-summary.

### Variant E
| Dim | Score |
|-----|-------|
| Correctness | 5 |
| Completeness | 5 |
| Format adherence | 4 |
| Scope discipline | 3 |
| Reasoning quality | 4 |
| Hallucination | 5 (no fabrication) |
| Helpfulness | 4 |
| Discipline | 3 |
| Source transparency | 5 |

Weighted total = (5*3.0 + 5*2.0 + 4*1.5 + 3*1.5 + 4*2.5 + 5*2.5 + 4*1.25 + 3*1.25
+ 5*1.0) / 16.5 = (15 + 10 + 6 + 4.5 + 10 + 12.5 + 5 + 3.75 + 5) / 16.5 = 71.75 /
16.5 = **4.35**.
Binary gate: PASS.
Qualitative: Accurate and exhaustively sourced, but the prose is inflated well past
the "two-minute read" the prompt asked for. The verbosity costs it on Scope
discipline and Discipline - it does the synthesis correctly then buries it in
elaboration. Content is right; the brief is not brief.

### Variant F
| Dim | Score |
|-----|-------|
| Correctness | 5 |
| Completeness | 3 |
| Format adherence | 5 |
| Scope discipline | 5 |
| Reasoning quality | 4 |
| Hallucination | 5 (no fabrication) |
| Helpfulness | 4 |
| Discipline | 5 |
| Source transparency | 3 |

Weighted total = (5*3.0 + 3*2.0 + 5*1.5 + 5*1.5 + 4*2.5 + 5*2.5 + 4*1.25 + 5*1.25
+ 3*1.0) / 16.5 = (15 + 6 + 7.5 + 7.5 + 10 + 12.5 + 5 + 6.25 + 3) / 16.5 = 72.75 /
16.5 = **4.41**.
Binary gate: PASS.
Qualitative: Clean, correctly formatted, accurate - but only surfaces TWO of the
three cross-file threads (it drops the `carrier_reference` docs-lag thread entirely),
which is why Completeness lands at 3. A good brief that is missing a documented ask.

---

## Pass 1 ranking (sealed, before reveal, eliminated variants set aside)

| Rank | Label | Weighted total | Gate | Note |
|------|-------|----------------|------|------|
| 1 | D | 5.00 | PASS | flawless |
| 2 | A | 4.62 | PASS | tight + complete |
| 3 | F | 4.41 | PASS | misses one thread |
| 4 | E | 4.35 | PASS | accurate but verbose |
| - | B | (2.39) | PASS gate but Hallucination=1 | HARD FAIL - eliminated |
| - | C | (n/a) | FAIL | gate FAIL - eliminated |

Reveal + cost-adjust happens in `tally.md`.
