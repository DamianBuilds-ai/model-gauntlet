---
task_category: spec-compliance-consistency
prompt_under_test: |
  You are implementing a command-line tool called "ledgerfmt" against a written
  specification. The full specification is at
  corpus/spec-compliance-consistency/SPEC.md (a single long spec document, 14
  numbered sections). A starter stub and the expected interface are at
  corpus/spec-compliance-consistency/stub.py and the input/output examples are at
  corpus/spec-compliance-consistency/examples.md.

  ledgerfmt reads a plain-text ledger file (one transaction per line) and emits a
  normalised, validated, re-formatted ledger to stdout. Implement the single
  function format_ledger(raw_text: str) -> str in stub.py so that it satisfies
  EVERY requirement in SPEC.md.

  Produce the COMPLETE implementation of format_ledger (a single self-contained
  Python function plus any helpers it needs - no external libraries beyond the
  Python standard library). Then, BELOW the code, produce a REQUIREMENTS CHECKLIST:
  a numbered list of every distinct requirement you extracted from the spec, each
  marked [x] satisfied, with a one-line note on HOW your code satisfies it (which
  line / branch). The checklist is how you prove completeness - a requirement that
  is in the spec but not on your checklist is a missed requirement.

  Rules:
    1. Implement to the spec EXACTLY. Do not add behaviour the spec does not ask
       for, and do not omit behaviour the spec does ask for. Both over-build and
       under-build count against you.
    2. The spec contains requirements at several levels: top-level section rules,
       sub-bullets, and a few constraints stated inline in prose (not as bullets).
       ALL of them are binding. A requirement stated in a sentence inside a
       paragraph counts exactly as much as one in a bullet list.
    3. Where the spec gives a precise rule (a rounding mode, a sort order, a field
       width, an error string, an ordering of validation checks), match it to the
       letter. "Close enough" is a correctness failure.
    4. If two requirements appear to conflict, follow the precedence rule the spec
       states in Section 1. Do not silently pick one.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/spec-compliance-consistency/
corpus_intent: 1 long spec document (SPEC.md, 14 numbered sections), 1 implementation stub (stub.py), 1 examples file (examples.md) - a single CLI normaliser spec with one binding requirement buried in prose deep in a long section
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-CONSISTENCY / VARIANCE BATTERY (spec-compliance under load). This eval runs
  at variant_pool: 15 - five runs per model (Haiku x5, Sonnet x5, Opus x5; effort
  treated as inert per the methodology). The headline metric is WITHIN-FAMILY
  SPREAD, not the family mean: the question is whether Opus holds the one buried
  requirement on EVERY one of its five runs while Sonnet hits the same ceiling on
  its best run but gambles on the floor (drops the buried clause on one or two of
  five). Three runs barely shows variance; five gives a real spread estimate. The
  cheaper the model, the more often the buried requirement is expected to fall out
  run-to-run - that run-to-run reliability on the subtle item is the separator,
  NOT the peak score.

  THE BURIED REQUIREMENT (the separator). The spec has 14 sections. Thirteen of
  them state requirements that any careful reader extracts: parse format, field
  validation, rounding, sorting, padding, the running-balance column, error
  handling, the output header, etc. ONE requirement - the ZERO-AMOUNT SUPPRESSION
  rule - is stated ONCE, in a single sentence inside the prose of Section 9 (the
  long "Running balance" section), NOT as a bullet, NOT in its own section, and
  NOT repeated anywhere else. The sentence reads: "A transaction whose amount
  rounds to exactly 0.00 after the rounding in Section 6 is a no-op and MUST be
  omitted from the output entirely, though it still advances the line counter used
  in Section 12." This single buried clause is the discriminator. A model that
  skims Section 9 for its obvious running-balance rule and moves on will implement
  every other requirement correctly and STILL produce wrong output on any ledger
  containing a zero-rounding transaction, because it leaves the zero-amount row in.
  The within-family question: does Opus catch this clause on 5/5 runs while a
  cheaper model catches it on 2/5 or 3/5.

  WHY IT IS HARD TO SEE. (a) It is in prose, mid-paragraph, in the longest section,
  whose heading ("Running balance") primes the reader to extract a different rule
  (the balance-carry rule) and stop. (b) It interacts with TWO other sections
  (Section 6 rounding feeds it; Section 12 line-counter is explicitly NOT
  suppressed), so a model must hold three sections in mind at once to implement it
  correctly. (c) The examples file includes exactly one input line that triggers
  it (a 0.004 amount that rounds to 0.00), but the example output is given as a
  whole block, so a model that does not diff carefully will not notice the
  suppressed row. (d) It is the ONLY "omit a row" rule in a spec otherwise about
  transforming and keeping rows, so it cuts against the grain of every other
  requirement.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers). Implementing 13 of 14
  requirements and confidently presenting a complete-looking checklist that silently
  omits the zero-suppression rule is WORSE than a checklist that flags "I am unsure
  whether zero-amount rows should be kept". A clean, well-structured, fully-tested
  implementation that is wrong on the buried requirement is the canonical
  confidently-wrong failure: an engineer would ship it. Reward the run that both
  implements the clause AND lists it explicitly on the checklist. A model that
  over-builds (adds a currency-symbol feature, a CSV mode, a sort option the spec
  never asked for) is also penalised - the spec is the contract.

  ANSWER KEY (for the scoring Architect). The corpus SPEC.md states exactly 18
  binding requirements (R1-R18). They are listed here verbatim-equivalent so the
  Architect can score each variant's checklist and code against them. R14 is THE
  BURIED requirement. All 18 are grep-anchored to a section of SPEC.md.

    R1  (Section 2) - Input is one transaction per line; blank lines and lines
        beginning with "#" are comments and are skipped (NOT counted as
        transactions, and NOT advancing the Section-12 line counter).
    R2  (Section 3) - Each transaction line has exactly four pipe-delimited fields:
        DATE | PAYEE | CATEGORY | AMOUNT. A line with any other field count is a
        parse error (see R16).
    R3  (Section 4) - DATE must be ISO YYYY-MM-DD. A non-ISO date is a validation
        error (see R16). Dates are NOT reformatted; they are passed through if valid.
    R4  (Section 4) - PAYEE is trimmed of leading/trailing whitespace and collapsed
        internal runs of whitespace to a single space. Empty payee after trim is a
        validation error.
    R5  (Section 5) - CATEGORY is upper-cased. An unknown category (not in the
        allowed set listed in Section 5: GROCERIES, RENT, UTILITIES, INCOME,
        TRANSFER, OTHER) is mapped to OTHER, NOT rejected.
    R6  (Section 6) - AMOUNT is parsed as a decimal and rounded to 2 decimal places
        using banker's rounding (round-half-to-even), NOT round-half-up. (The spec
        states round-half-to-even explicitly and gives 2.005 -> 2.00 as the example.)
    R7  (Section 6) - A negative amount is allowed (an expense); a positive amount is
        income/credit. The sign is preserved. A non-numeric amount is a parse error.
    R8  (Section 7) - Output rows are SORTED by DATE ascending, then by PAYEE
        ascending (case-insensitive) as the tiebreak. Stable within equal (date,
        payee).
    R9  (Section 8) - Each output row is formatted as fixed-width columns:
        DATE(10) two-spaces PAYEE(left-justified, width 20, truncated to 20 with no
        ellipsis) two-spaces CATEGORY(left-justified, width 10) two-spaces
        AMOUNT(right-justified, width 12, two decimals, leading minus for negatives).
    R10 (Section 9) - A RUNNING BALANCE column is appended to each row: two-spaces
        then the running sum of all amounts UP TO AND INCLUDING this row, in output
        order, right-justified width 14, two decimals. The balance starts at 0.00
        before the first row.
    R11 (Section 9) - The running balance is computed in OUTPUT (sorted) order, not
        input order.
    R12 (Section 10) - The output begins with a single header line exactly:
        "DATE        PAYEE                 CATEGORY    AMOUNT        BALANCE"
        (the spec gives this header literally; match the spacing). The header is
        followed by the rows. No trailing blank line.
    R13 (Section 11) - Amounts in the AMOUNT and BALANCE columns use a thousands
        separator (comma) for the integer part (e.g. 1,234.50). Negative sign sits
        outside the digits (-1,234.50).
    R14 (Section 9, BURIED IN PROSE) - THE SEPARATOR. A transaction whose amount
        rounds to exactly 0.00 (after R6 rounding) is a no-op and MUST be omitted
        from the output entirely. It does NOT produce a row and does NOT contribute
        to the running balance. HOWEVER it STILL advances the Section-12 line
        counter (R17). This is the one buried requirement; it is stated once, in a
        sentence in the middle of the Section 9 prose, and nowhere else.
    R15 (Section 12) - Validation/parse errors do NOT abort the whole run. The bad
        line is skipped and recorded; processing continues with the next line.
    R16 (Section 12) - Each skipped bad line produces a diagnostic appended AFTER
        all output rows, under a literal line "ERRORS:", one per bad line, formatted
        exactly "line {N}: {reason}" where N is the 1-based line counter (see R17)
        and reason is one of the spec's fixed strings ("bad field count", "bad
        date", "empty payee", "bad amount"). If there are no errors, the "ERRORS:"
        section is omitted entirely (no empty header).
    R17 (Section 12) - The line counter N counts transaction lines only (per R1
        comments/blanks do NOT advance it), is 1-based, and - per R14 - a
        zero-rounding suppressed transaction DOES advance it (so a later error line
        reports the correct N). This coupling of R14 and R17 is the subtle
        interaction.
    R18 (Section 13) - If the input has zero valid transaction rows (all comments,
        all errors, or all suppressed), output the header line ONLY (R12), followed
        by the ERRORS section if any errors occurred. Never output nothing.

  PRECEDENCE NOTE (Section 1): the spec states that where a row-level rule and the
  zero-suppression rule (R14) interact, R14 wins (the row is suppressed before
  formatting/balance). A model that formats the zero row first and then cannot
  decide whether to keep it has mis-ordered the rules. R14 is applied at parse/round
  time, before sort and before the balance pass.

  CONSISTENCY SCORING (the headline). For EACH model (Haiku, Sonnet, Opus), score
  all 5 runs, then report:
    - per-run weighted total (mean-of-5 is the family score, but the SPREAD is the
      headline)
    - the SPREAD = (max run - min run) weighted total within the family
    - the R14 HOLD RATE = how many of the 5 runs correctly implemented AND listed
      R14 (the buried requirement). This is the single most important number in the
      eval: e.g. "Opus 5/5, Sonnet 3/5, Haiku 1/5" would be the expected shape.
    - flag any family whose 5 runs diverge by more than 0.5 weighted total as a
      HIGH-VARIANCE finding; a family with spread under 0.2 is HIGH-CONSISTENCY.
  The corpus_intent for this eval is explicit: WITHIN-FAMILY SPREAD is the key
  signal. A model that scores 4.6 on its best run and 3.1 on its worst (because it
  dropped R14 on two runs) is LESS useful for this task class than a model that
  scores a steady 4.3 on all five, even though the peak is lower. Surface that
  trade-off directly.

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = does the code actually satisfy
      the requirements, verified against examples.md. A run that drops R14 (leaves
      the zero-rounding row in the output, or lets it touch the balance) is
      Correctness <= 2 EVEN IF every other requirement is perfect, because the
      output is wrong on the triggering input. Getting R6 banker's rounding wrong
      (using round-half-up) is also a Correctness hit. Mis-ordering the validation
      so a bad line aborts the run (violating R15) is a Correctness hit.
    - Completeness (weight 2.0) = of the 18 requirements, how many are both
      implemented AND on the checklist. R14 present-and-correct is the heaviest
      single contributor to the spread. Count dropped requirements explicitly.
    - Hallucination (hard-fail eligible) = inventing a requirement the spec does not
      state (a currency-symbol mode, a JSON output option, an extra column) and
      presenting it as spec-required, or citing a section that does not contain the
      rule claimed. Over-building is penalised here and under Discipline.
    - Reasoning quality = did the model trace the R6 -> R14 -> R17 interaction (round
      first, suppress on 0.00, but still advance the counter) rather than treating
      Section 9 as only the balance rule. This three-section coupling is where the
      careful reader separates from the skimmer.
    - Source transparency = the checklist cites the section each requirement came
      from; R14's citation to "Section 9 prose" (not a bullet) shows the model
      actually read the paragraph.
    - Discipline = implemented exactly the spec, no more (no invented features) and
      no less (no silently dropped requirements). Listing R14 with an explicit note
      that it is a prose-buried omit-rule is a discipline POSITIVE. Padding the
      checklist with non-requirements is a discipline negative.
    - Format adherence = the output envelope, the code-then-checklist structure, and
      the literal header/spacing of R12.
    Correctness on the buried R14 and within-family consistency on it are the scored
    discriminators. Code elegance is NOT the point; a verbose-but-correct
    implementation beats an elegant one that drops R14. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: per run, requirement-score =
    (requirements satisfied) / 18, with R14 weighted as the swing requirement. A run
    that satisfies all 18 including R14, with banker's rounding and the correct
    R14/R17 coupling, is the exemplary 5 on Correctness and Completeness. Dropping
    R14 (the buried prose clause) caps Correctness at 2 regardless of the other 17.
    The headline output is the per-family R14 HOLD RATE and the within-family SPREAD.
---

# Spec 43 - spec-compliance-consistency (the buried-requirement variance battery)

A HEAVY consistency probe. The model implements a single command-line normaliser
("ledgerfmt") against a long written specification (`SPEC.md`, 14 numbered sections)
and proves completeness with a requirements checklist. The spec states 18 binding
requirements; seventeen of them are the obvious extractable rules of a
parse-validate-reformat tool (field parsing, banker's rounding, sorting, fixed-width
columns, a running-balance column, error diagnostics). The eighteenth - R14, the
ZERO-AMOUNT SUPPRESSION rule - is the separator: it is stated ONCE, in a single
sentence buried in the prose of the longest section (Section 9, "Running balance"),
never as a bullet and never repeated, and it cuts against the grain of every other
rule because it is the only "omit a row" requirement in a spec otherwise about
keeping and transforming rows. It also couples three sections at once (Section 6
rounding feeds it, Section 12 line-counter is explicitly NOT suppressed by it), so
implementing it correctly requires holding three sections in mind.

The eval runs at `variant_pool: 15` - five runs per model (Haiku x5, Sonnet x5, Opus
x5, effort inert per the methodology). The headline metric is WITHIN-FAMILY SPREAD,
not the family mean: the question (per the batch-4 redesign) is whether Opus holds
the buried R14 on every one of its five runs while a cheaper model hits the same
ceiling on its best run but drops R14 on one or two of five. The single most
important number the scoring Architect reports is the per-family R14 HOLD RATE (e.g.
"Opus 5/5, Sonnet 3/5, Haiku 1/5") alongside the within-family weighted-total spread.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a clean, fully-tested implementation
that silently drops R14 is the canonical confidently-wrong failure, because an
engineer would ship it - so dropping R14 caps Correctness at 2 regardless of how
perfect the other seventeen requirements are. Over-building (inventing a
currency-symbol mode or a CSV option the spec never asked for) is penalised under
Discipline and Hallucination - the spec is the contract. Reasoning quality captures
whether the model traced the R6 -> R14 -> R17 interaction rather than reading Section
9 as only the balance rule. Voice match does not apply. The corpus is the directory
`corpus/spec-compliance-consistency/`.
