---
task_category: heterogeneous-precision-battery
prompt_under_test: |
  You are given a single target file at
  corpus/heterogeneous-precision-mixed-domain/release-prep.md - a Hollowmere
  release-prep bundle. It contains four edit surfaces in one document: a prose
  section, a Python code snippet, a markdown data table, and a bullet list.

  Apply the following ten change requirements to that file EXACTLY in ONE shot.
  Each requirement is precise and has exactly one correct result. Apply ONLY
  what is listed. Do NOT reformat, reorder, re-align, normalise, or "improve"
  anything the spec does not name. Do NOT touch any other line.

  CHANGE REQUIREMENTS (apply all ten):

    R1. PROSE. In section "1. Release notes prose", REMOVE the word "basically"
        from the sentence that contains it. Leave the rest of the sentence
        intact (only the word, and the single space adjacent to it, is removed
        - the surrounding punctuation and words stay).

    R2. CODE. In section "2. Pipeline config snippet", in the Python dict,
        RENAME the key `max_batch_size` to `batch_size_limit`. Leave its value
        (100) unchanged. Do not touch any other key.

    R3. TABLE. In section "3. Service health table", CONVERT every value in the
        `last_check` column from DD/MM/YYYY format to ISO format (YYYY-MM-DD).
        Example: `14/03/2026` becomes `2026-03-14`. Apply to all five rows.

    R4. LIST. In section "4. Rollout checklist", REORDER the bullets so they
        appear in this order: staging-soak, canary-1pct, canary-25pct,
        post-cutover-verify, prod-cutover. (Swap the last two from the current
        order.) Keep the bullet text otherwise identical.

    R5. PROSE. In section "1. Release notes prose", REMOVE the word "very" from
        the sentence that contains "carefully verify". Leave the rest of the
        sentence intact.

    R6. CODE. In section "2. Pipeline config snippet", CHANGE the value of
        `flush_interval_ms` from `250` to `500`. Do not change any other value.

    R7. TABLE. In section "3. Service health table", COMPUTE the sum of all
        `latency_ms` values across the five rows and APPEND a new row at the
        END of the table with: `TOTAL | <sum> | - | -` where `<sum>` is the
        computed integer total. Use the same column layout as the existing
        rows.

    R8. LIST. In section "4. Rollout checklist", APPEND one new bullet at the
        END of the list: `- rollback-drill`. Use the same `- key` bullet
        format as the existing entries.

    R9. PROSE. In section "1. Release notes prose", REPLACE the phrase
        "super important" with "critical". Change only those two words.

    R10. TABLE. In section "3. Service health table", in the `courier` row
         only, SET the `error_rate_pct` value from `0.21` to `0.15`. Change
         only that one cell. Leave courier's latency and last_check unchanged
         (apart from the R3 date conversion that applies to all rows).

  Output the COMPLETE updated file content, from its first line to its last
  line, as a single fenced code block, with all ten changes applied and nothing
  else altered. After the code block, append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines OUTSIDE the
  code block. No em dashes (spaced hyphens). No emojis. Do not add commentary
  inside the file content.
variant_pool: 15
corpus: corpus/heterogeneous-precision-mixed-domain/
corpus_intent: |
  One target file (corpus/heterogeneous-precision-mixed-domain/release-prep.md):
  a release-prep bundle with FOUR edit surfaces in one artifact - a prose
  section, a Python code snippet, a markdown data table, and a bullet list.
  The eval asks for a single-shot apply of TEN unrelated precise requirements
  that span all four domains, deliberately ordered to MAXIMIZE
  context-switching (prose -> code -> table -> list -> prose -> code -> table
  -> list -> prose -> table - no two adjacent requirements share a domain).

  THE HETEROGENEOUS-PRECISION-BATTERY: MIXED-DOMAIN VARIANT. This is eval 104
  of the heterogeneous-precision battery (101-105). Where 102 turns the COUNT
  of requirements up (12 same-shape ops) and 103 turns INTERDEPENDENCE up, 104
  isolates the DOMAIN-SWITCHING cost. Each individual requirement is trivial
  in isolation (rename one key, change one value, append one bullet, remove
  one word, convert five dates, sum five integers, swap two bullets, replace
  two words). The hardness comes ONLY from juggling ten precise things across
  four different cognitive domains in one shot - a model must hold the prose
  rules while doing the code edit, hold the date format while computing the
  sum, etc. If Opus wins HERE but not on 102, the edge is context-switch
  tolerance not raw capacity.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): all-or-fail per
  requirement. A model that applies nine of ten correctly but drops R7 (the
  sum) scores Completeness 9/10, but for the primary metric
  (all-requirements-correct rate) this is a MISS. The drop-distribution metric
  records WHICH requirement each failing run missed - random drops vs
  always-the-same-domain. Over-reach (touching a line the spec did not name)
  is equally a miss: a run that "improves" the code snippet by re-ordering
  the dict keys, or normalises the prose, fails Discipline.

  ANSWER KEY (for the scoring Architect - the exact end-state after applying
  R1-R10). Verify by comparing the model's output line-by-line against the
  original corpus file.

    R1 (prose, remove word): the sentence "This release is built on top of
       the v2.3.x line and will be super important for the upcoming quarter,
       since downstream consumers basically depend on the new batching
       guarantees" loses the word "basically" - in the AFTER state the
       sentence reads "...since downstream consumers depend on the new
       batching guarantees" (note R9 also rewrites "super important" to
       "critical" in the SAME sentence - the final sentence is "This release
       is built on top of the v2.3.x line and will be critical for the
       upcoming quarter, since downstream consumers depend on the new
       batching guarantees").

    R2 (code, rename key): the Python dict line currently reading
       `"max_batch_size": 100,` becomes `"batch_size_limit": 100,`. No other
       key changes.

    R3 (table, date format): all five `last_check` cells become ISO format:
       gateway 2026-03-14; ledger 2026-03-12; courier 2026-03-15; beacon
       2026-03-11; almanac 2026-03-13. The DD/MM/YYYY format appears ZERO
       times in the AFTER state.

    R4 (list, reorder): the bullets in section 4 appear in this order:
       staging-soak; canary-1pct; canary-25pct; post-cutover-verify;
       prod-cutover. (R8 then appends rollback-drill as the sixth bullet.)

    R5 (prose, remove word): the sentence "Operators should very carefully
       verify the staging soak before promoting to production" loses "very"
       - the AFTER sentence reads "Operators should carefully verify the
       staging soak before promoting to production".

    R6 (code, value change): the dict line `"flush_interval_ms": 250,`
       becomes `"flush_interval_ms": 500,`.

    R7 (table, computed total): a new row is APPENDED at the end of the
       table reading `| TOTAL | 319 | - | - |`. The sum of the five
       latency_ms values (42 + 88 + 65 + 51 + 73) = 319. The integer 319
       must appear in this exact row.

    R8 (list, append): the bullet `- rollback-drill` is APPENDED as the
       LAST bullet in section 4 (after the R4 reorder). The list ends with
       rollback-drill.

    R9 (prose, replace phrase): the words "super important" become
       "critical" in the sentence noted under R1.

    R10 (table, single cell): the courier row's `error_rate_pct` cell
        becomes `0.15` (was `0.21`). All other table cells in non-courier
        rows are unchanged (except R3 dates and R7 appended TOTAL row).

    Everything else in the file (headings, blank lines, code-fence markers,
    untouched table cells, untouched code keys, untouched bullets, untouched
    prose) is BYTE-IDENTICAL to the original.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - `basically` appears ZERO times (R1).
    - `batch_size_limit` appears exactly once; `max_batch_size` appears ZERO
      times (R2).
    - `2026-03-14`, `2026-03-12`, `2026-03-15`, `2026-03-11`, `2026-03-13`
      each appear exactly once; the substring `/03/2026` appears ZERO times
      (R3).
    - The bullet order in section 4 matches: `staging-soak` then `canary-1pct`
      then `canary-25pct` then `post-cutover-verify` then `prod-cutover` then
      `rollback-drill` (R4 + R8).
    - The substring `very carefully` appears ZERO times; `carefully verify`
      still appears once (R5).
    - `"flush_interval_ms": 500,` appears exactly once;
      `"flush_interval_ms": 250,` appears ZERO times (R6).
    - The literal substring `| TOTAL | 319 | - | - |` appears exactly once
      (R7). The integer 319 in this row is mandatory; any other integer = miss.
    - `- rollback-drill` appears exactly once as the last bullet (R8).
    - `super important` appears ZERO times; `critical for the upcoming
      quarter` appears exactly once (R9).
    - The courier row contains `0.15` in its error_rate_pct cell; `0.21`
      appears ZERO times in the AFTER state (R10).
    - The table still has its original column headers (`service`,
      `latency_ms`, `error_rate_pct`, `last_check`); no header was renamed.
    - The Python dict still contains `service_name`, `retry_policy`, and
      `region` keys unchanged (no over-reach on the code edit surface).

  DROP-DISTRIBUTION TRACKING SPEC (for the Architect): for each of the 5 runs
  per family, record which of R1-R10 (if any) was missed. Tally per family:
  total runs all-correct (primary metric); mean requirements-satisfied (/10);
  per-requirement miss rate (which domain leaks - prose, code, table, or
  list); and whether misses cluster on a specific domain (e.g. a family that
  always drops the sum R7 vs random drops). Compare miss-patterns across
  families: if Opus's misses (if any) are random while Sonnet/Haiku cluster
  on domain-switches (e.g. miss R6 right after R5, or miss R7 after R6), that
  is the context-switch signal.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all ten requirements applied exactly
      AND nothing else changed. A miss on any single requirement = the run
      fails the primary all-correct metric.
    - Completeness = how many of R1-R10 are present (/10).
    - Hallucination (hard-fail eligible) = inventing an 11th edit, changing
      a value the spec did not give, mutating an out-of-scope cell/line, or
      claiming "done, nothing else changed" when the output drifted.
    - Format adherence = the complete file as one fenced code block,
      envelope outside it, same syntax as the original.
    - Discipline = applied ONLY the ten named edits and left every other
      byte identical (no reformat, no re-sort beyond R4, no extra-key
      rename, no untouched-cell drift). Load-bearing for this eval.
    - Reasoning quality = SKIP-eligible (this is a precise apply, not a
      judgment task); if reasoning is shown, it should not invent scope.
    Voice match does NOT apply.
notes: |
  Eval 104 of the heterogeneous-precision battery (101-105). The headline
  hypothesis: Opus may win only when ONE shot demands precision across MANY
  DIFFERENT things at once, scored all-or-fail. 102 turns COUNT up (12 ops
  same shape); 104 isolates DOMAIN-SWITCHING by spanning 10 ops across four
  cognitive domains (prose, code, table, list) ordered to maximize
  context-switching - no two adjacent requirements share a domain. Each
  individual op is trivial; the hardness is in juggling all ten across the
  domain gear-changes in one shot. If Opus wins HERE but not on 102, the
  edge is context-switch tolerance not raw capacity. If Opus does not win
  here, this falsifies one more Opus niche.

  DIFFICULTY SELF-CHECK (the eval-48 lesson): would a weak model (Haiku)
  genuinely drop a requirement here? Honest prediction: YES, plausibly.
  Ten precise requirements across four domains in one shot, with the most
  cognitively-distinct ops (R7 the integer sum, R3 the five-row date
  conversion, R1+R5+R9 the three separate prose touches in the same
  section) are exactly the kind of load where a weak model under
  one-shot pressure either drops the sum, mishandles one of the five date
  conversions, or forgets one of the three prose edits. The corpus is
  intentionally designed so that the prose section hosts THREE separate
  requirements (R1, R5, R9) - a model that processes prose in one pass and
  forgets to revisit is likely to drop one. Per the gameplan: if Haiku
  would reliably hold all ten across 5 runs, the eval is a ceiling tie;
  the design above (mixed-domain ordering + three prose touches + one
  computed value + five-cell conversion) is calibrated to bite.

  HINT-FREE compliance (the eval-43 lesson): the corpus contains ZERO
  comments naming any requirement, ZERO structural tells, ZERO
  suspicious section labels. The four sections are numbered 1-4 because
  that is natural for a release-prep doc; the bullets and table rows
  are ordinary content. The synthetic-data disclaimer at top is generic.
  Codenames: Hollowmere (project), Veldt Systems (company), Marlowe
  (metrics shipper) - all neutral fictional names per repo hygiene.
  Variant pool 15 (N=5, drop-rate question). Corpus dir:
  corpus/heterogeneous-precision-mixed-domain/.
---

# Spec 104 - heterogeneous-precision-mixed-domain (the context-switch probe)

Given a single artifact bundling four edit surfaces (prose, code, table,
bullet list) and ten precise requirements ordered to maximize context-switching
between domains, apply all ten in ONE shot exactly - each individual op is
trivial, the test is holding all ten across the cognitive gear-changes. This
is eval 104 of the five-eval heterogeneous-precision battery (101-105).

The eval isolates DOMAIN-SWITCHING cost. Where eval 102 turns the COUNT of
requirements up (12 same-shape ops) and 103 turns INTERDEPENDENCE up, 104
keeps the count at 10 but ORDERS them prose -> code -> table -> list -> prose
-> code -> table -> list -> prose -> table so no two adjacent requirements
share a domain. A model that handles each domain in batches (do all prose
first, then all code, etc.) is making the eval easier than the spec asks - the
spec ordering forces constant gear-changes within a single one-shot apply. If
Opus wins HERE but not on 102, the edge is context-switch tolerance not raw
capacity.

The corpus (`corpus/heterogeneous-precision-mixed-domain/release-prep.md`) is
one Hollowmere release-prep bundle with a prose release-notes section, a
Python pipeline-config snippet, a five-row markdown service-health table, and
a five-bullet rollout checklist. The ten requirements are intentionally
designed so the prose section hosts THREE separate edits (R1 remove a word, R5
remove another word, R9 replace a phrase), the table hosts THREE separate
edits (R3 convert five dates, R7 compute and append a total row, R10 set one
cell), the code hosts TWO (R2 key rename, R6 value change), and the list
hosts TWO (R4 reorder, R8 append). A model that scans the prose section once
and moves on is likely to drop one of R1/R5/R9; the computed sum R7 is a
cognitive shift mid-table-edit. The traps are all over-reach (touching an
unnamed cell, key, or line) or drop (missing one of the ten).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
The correctness-first quality principle holds: all-or-fail per requirement
for the primary metric; over-reach is equally a miss; the drop-distribution
metric records WHICH requirement each failing run missed so the scoring
Architect can compare random-drop families to domain-clustering families.
Correctness and Hallucination are hard-fail eligible; Discipline (apply ONLY
the ten named edits, change nothing else) is load-bearing. Voice match does
not apply. The variant pool is 15 (3 models x N=5, effort inert per the
methodology). The corpus is the directory
`corpus/heterogeneous-precision-mixed-domain/`.
