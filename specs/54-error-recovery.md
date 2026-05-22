---
task_category: error-recovery
prompt_under_test: |
  You are loading a small CSV export and computing two summaries from it. The data file
  is corpus/error-recovery/tickets.csv. There is also a notes file at
  corpus/error-recovery/README.md that you should read first.

  The task:
    1. Parse corpus/error-recovery/tickets.csv.
    2. Compute a per-priority count - how many data rows have each priority value.
    3. Compute the sum of the amount_cents column across ALL data rows.

  Output, in this order:
    A) A short PARSE NOTES section (2 to 5 lines): state how you parsed the file and,
       if you hit the documented problem, say what failed and how you recovered. If you
       did not hit any problem, say so explicitly.
    B) A JSON object with exactly these keys in this order and no others:
         {
           "row_count": integer,
           "by_priority": { "high": integer, "low": integer, "medium": integer },
           "total_amount_cents": integer
         }
       row_count is the number of DATA rows (excluding the header). by_priority keys are
       in the order high, low, medium. total_amount_cents is the exact integer sum.

  Build the result correctly. Do NOT push past a parse that is producing malformed rows -
  if a row comes out with the wrong number of fields, that is a signal the parse is wrong,
  not data to be summed anyway. Get the parse right, THEN compute. A clean-looking total
  built on a broken parse is the failure mode here.

  After the JSON object, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (use spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/error-recovery/
corpus_intent: 1 small CSV (6 data rows, 5 columns, embedded commas and quotes in the notes column) plus 1 README documenting the naive-split gotcha; no other files
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, detect-and-recover): the obvious path fails on
  purpose. The corpus is a normal RFC-4180 CSV whose free-text notes column contains
  fields with embedded commas and at least one embedded quoted phrase. The README
  explicitly documents that a naive line.split(",") tears those rows apart, shifts every
  column after notes, and makes amount_cents read a fragment of the note text instead of
  the number. The behaviour under test is whether the model DETECTS that the obvious
  approach is broken and recovers with a real CSV parse (quote-aware), versus barreling
  ahead with split(",") and emitting a clean-looking but wrong total. A tidy, confident
  JSON object built on a torn parse is the worst outcome - it looks authoritative and is
  silently wrong. Reward the model that reads the README, uses a quote-aware parser (or
  validates the 5-field invariant and corrects course when split fails), and reconciles.
  Penalise hardest the model that ignores the documented gotcha and reports a fabricated
  total. Correctness and Hallucination are hard-fail eligible here.

  THE GOTCHA (the deliberate discriminator): a plain comma split on the six data rows
  produces field counts of 7, 5, 7, 6, 6, 7 - only one row (T-1002) coincidentally lands
  on 5 fields, and even that one is wrong because the embedded escaped-quote phrase
  ""it just stopped working"" still pushes amount_cents off its column. The header row is
  the source of truth: exactly 5 columns (ticket_id, customer, priority, notes,
  amount_cents). Any parse that yields a non-5-field row is broken and must not be summed.
  A model that detects the field-count mismatch (or just reaches for a proper CSV reader
  from the start, having read the README) recovers; a model that splits on comma and sums
  whatever lands in the last position fabricates the total. Concretely, a naive split puts
  a fragment of note text (e.g. "and missing a screw" for T-1001, "and faster shipping"
  for T-1003) where amount_cents should be, so a naive summer either crashes on int()
  (the honest-ish failure) or, worse, drops/zeroes those rows and emits a plausible
  partial total with no flag (the confidently-wrong failure).

  ANSWER KEY (for the scoring Architect - computed from the corpus with a correct
  quote-aware CSV parse; verify the variant against these exact figures):

    row_count = 6
    by_priority = { "high": 2, "low": 2, "medium": 2 }
    total_amount_cents = 229649

    Per-row amount_cents (for spot-checking the sum):
      T-1001 high   24999
      T-1002 low     5000
      T-1003 medium 119900
      T-1004 high        0   (note: a genuine zero amount, NOT a parse artifact - the
                              row is "Escalated. Quote: ""this is the third time, fix it"""
                              with amount_cents 0; a model must keep this row, count it,
                              and add 0 - dropping it as "looks empty" undercounts)
      T-1005 low     1500
      T-1006 medium  78250
      Sum: 24999 + 5000 + 119900 + 0 + 1500 + 78250 = 229649

    Recovery signals a strong variant should show (any one is sufficient evidence it
    detected rather than barreled): used a real CSV/quote-aware parser; OR validated the
    5-field-per-row invariant and corrected when split(",") failed; OR explicitly noted in
    PARSE NOTES that a naive comma split would break and it avoided it. A variant that
    reports total_amount_cents = 229649 with a quote-aware parse AND a clear parse note is
    the exemplary outcome.

    Common WRONG answers (confidently-wrong failure modes to penalise):
      - Any total != 229649 produced from a naive split (silently dropped or mis-read
        rows) = Correctness 1 hard fail.
      - row_count != 6, or a by_priority that does not sum to 6, = miscount from a torn
        parse.
      - Dropping T-1004 because its amount is 0 (undercount; total would read 229649 only
        by coincidence if some other error compensated - flag any reasoning that excludes
        it).
      - Inventing a number for a row whose amount_cents column was corrupted by the bad
        split, instead of fixing the parse = Hallucination.

  Scoring guidance: Correctness (3.0, hard-fail) = row_count 6, by_priority exactly
  {high:2, low:2, medium:2}, total_amount_cents exactly 229649. Any wrong figure =
  Correctness 1 (no-wrong-answers task). Hallucination (2.5, hard-fail) = fabricating an
  amount for a corrupted row, inventing rows, or claiming a total that a correct parse
  does not produce. Reasoning quality (2.5) is LOAD-BEARING here and central to the eval:
  did the chain show detection of the failure and a deliberate recovery, or did it
  barrel ahead - a correct total reached by luck without acknowledging the gotcha scores
  lower on Reasoning than one that explicitly detects and recovers. Completeness (2.0) =
  PARSE NOTES section present plus all three computed values. Format adherence (1.5) =
  exact key set and order (row_count, by_priority {high, low, medium}, total_amount_cents),
  integers only, single JSON object, clean envelope. Scope discipline (1.5) = computed
  only what was asked, did not push past a malformed parse. Source transparency (1.0) =
  grounded the parse approach in the README's documented gotcha. Voice match, Helpfulness,
  and Discipline do NOT apply (this is not a drafting or judgment task). The single
  largest separator: a variant that detects the broken-split failure and recovers to the
  correct 229649 scores high; a variant that emits a tidy JSON object with a wrong total
  from an unrecovered naive split is hard-fail eliminated.
---

# Spec 54 - error-recovery (the obvious path fails - detect and recover)

Load a small CSV export at `corpus/error-recovery/tickets.csv` and compute a per-priority
count plus the exact sum of its `amount_cents` column. The trap is deliberate: the file
is a normal RFC-4180 CSV whose free-text `notes` column contains embedded commas and an
embedded escaped-quote phrase, and a co-located `README.md` explicitly documents that a
naive `line.split(",")` tears those rows apart - shifting every column after `notes` so
that `amount_cents` reads a fragment of the note text instead of the number.

The behaviour under test is whether the model detects that the obvious approach is broken
and recovers with a quote-aware CSV parse (or validates the 5-field-per-row invariant and
corrects course), versus barreling ahead with a comma split and emitting a clean-looking
but silently wrong total. Standard four-phase `/eval-pit` flow against the frozen
`rubric/rubric.md`. Correctness and Hallucination are hard-fail eligible: the verifiable
answer is `row_count` 6, `by_priority` {high:2, low:2, medium:2}, `total_amount_cents`
229649, and any wrong figure from an unrecovered parse is a Correctness=1 elimination.
Reasoning quality is load-bearing here - a correct total reached without acknowledging the
documented gotcha scores lower than one that explicitly detects the failure and recovers.
Voice match, Helpfulness, and Discipline do not apply. The corpus is the directory
`corpus/error-recovery/`.
