---
task_category: heterogeneous-precision-battery
prompt_under_test: |
  You are given a single target file at
  corpus/heterogeneous-precision-8/hollowmere-release-prep.md - the release-prep
  artifact for the fictional game Hollowmere v2.4.1. It contains a crew-allocation
  table, a roadmap blurb paragraph, a fenced JSON build-config block, a bullet
  list for the on-stream rotation, a kilobyte cosmetic-size list with a total
  line, and a patch-note draft snippet.

  Apply the following EIGHT independent change requirements to that file in a
  single pass. Each requirement is a precise, deterministic edit; each has
  exactly one correct result. Apply ONLY what is listed. Do NOT reformat,
  reorder, re-align, normalise, or "improve" anything the requirements do not
  name. Do NOT touch any other line.

  CHANGE REQUIREMENTS (apply all eight):

    R1. FIELD RENAME (table header). In the "Crew allocations" table, rename
        the `rate_band` column header to `pay_band`. Update ONLY the header
        cell; leave every row's value (senior / mid) unchanged in content.

    R2. ARITHMETIC GRAND TOTAL. The "Grand total hours" line currently reads
        `Grand total hours: 0`. SET the number to the exact sum of the
        `hours_logged` column across all six crew rows.

    R3. DATE FORMAT CONVERSION (DD/MM/YYYY -> ISO YYYY-MM-DD). In the
        "Roadmap blurb (public)" paragraph, convert all three dates from
        DD/MM/YYYY to ISO YYYY-MM-DD format. The dates are 14/10/2026,
        17/10/2026, 21/10/2026. Touch ONLY those three date strings; leave
        every other word in the paragraph unchanged.

    R4. FORBIDDEN-WORD REMOVAL (single word, three instances). In the
        "Roadmap blurb (public)" paragraph, remove every occurrence of the
        word `obviously`, `frankly`, and `absolutely` (case-sensitive). Remove
        only the word itself (and the single adjacent space that would
        otherwise leave a double space); keep the rest of the sentence
        grammatical with single spacing. Do NOT remove or alter any other
        word.

    R5. SORT-ORDER REORDER (on-stream rotation). The "On-stream rotation"
        bullet list is currently in the wrong chronological order. Reorder
        the bullets so they read Day 1, Day 2, Day 3, Day 4, Day 5 (top to
        bottom). Do NOT change any bullet's text content - only the order.

    R6. UNIT NORMALIZATION (KB -> MB total). The "Cosmetic drop sizing"
        section lists four per-tier sizes in KB. The "Cosmetic bundle total"
        line currently reads `Cosmetic bundle total: 0 MB`. SET it to the
        exact total in MB, using 1 MB = 1024 KB. Do NOT alter the per-tier
        lines themselves.

    R7. JSON FIELD RENAME. In the fenced JSON build-config block, rename the
        key `legacy_login_path` to `legacy_login_enabled`. Leave its value
        (`true`) unchanged. Do NOT rename any other key.

    R8. CODENAME REMOVAL (boundary-condition fix). In the "Patch-note draft
        snippet" blockquote, remove both occurrences of the internal codename
        `Project Inkwell` so that the quoted paragraph no longer references
        it. Replace the first occurrence (`internally codenamed Project
        Inkwell, `) with an empty string so the sentence flows as `The
        expedition rework overhauls the route-planning UI and the
        encounter-pacing curves.`. Replace the second occurrence (`Project
        Inkwell players`) with `Players` so that sentence flows as `Players
        will notice tighter loop timings and a clearer mid-run checkpoint.`
        Touch ONLY those two phrases; leave the rest of the blockquote
        unchanged.

  Output the COMPLETE updated file content, from its first line to its last
  line, as a single fenced code block, with all eight requirements applied and
  nothing else altered. After the code block, append the required output
  envelope (schemaVersion, tier, status, tool_budget_used) as separate lines
  OUTSIDE the code block. No em dashes (spaced hyphens). No emojis. Do not
  add commentary inside the file content.
variant_pool: 15
corpus: corpus/heterogeneous-precision-8/
corpus_intent: |
  ONE realistic fictional artifact (corpus/heterogeneous-precision-8/hollowmere-release-prep.md):
  the v2.4.1 release-prep checklist for the fictional game Hollowmere. The
  artifact organically hosts eight unrelated precise edit surfaces - a
  crew-allocations markdown table, a public roadmap prose blurb, a fenced
  JSON build-config block, an on-stream rotation bullet list, a kilobyte
  cosmetic-sizing list with a total line, and a patch-note draft blockquote
  - so the bundling feels like one release-engineer's pre-lock pass rather
  than a list of disconnected chores.

  THE HETEROGENEOUS-PRECISION FLOOR PROBE (8 simultaneous unrelated ops).
  This is the calibration floor of the 101-105 battery: 8 distinct cognitive
  operations (field rename, arithmetic total, date-format conversion,
  forbidden-word removal, sort reorder, unit normalization, JSON field
  rename, boundary-condition codename removal) packed into one document
  transform. Each individual op is trivial (eval-48 proved single-op
  difficulty does not separate Opus); the hypothesis under test is that
  HOLDING ALL EIGHT in a single pass with zero misses is what separates a
  large working set from a smaller one. The 8-op load is the discrimination
  THRESHOLD probe - if every family scores 5/5 here, the floor is high
  enough that the real signal must come from 102 (12 ops) or 103
  (interdependent). If any family drops one of the 8, the threshold is
  located.

  QUALITY PRINCIPLE (correctness-first, drop-tracking). An apply that
  silently mutated an out-of-scope line is WORSE than one that honestly
  applied seven of eight and flagged the eighth. The eval is scored
  binary-per-requirement: all eight correct = pass, any miss = fail, and the
  scoring Architect records WHICH requirement each failing run missed so the
  drop distribution can be inspected (random drops across requirements vs
  always-the-same-hard-one).

  ANSWER KEY (for the scoring Architect - the exact end-state after applying
  R1-R8). Verify by line-by-line comparison against the original corpus
  file plus the grep invariants below.

    R1 (field rename): the "Crew allocations" table header row reads exactly
       `| crew_member       | role               | hours_logged | pay_band |`.
       The string `rate_band` appears ZERO times in the output. The string
       `pay_band` appears EXACTLY once (in that header). Every value cell
       (senior, mid) is unchanged.

    R2 (arithmetic grand total): the line reads exactly `Grand total hours:
       174`. The six logged hours are 38 + 42 + 24 + 31 + 18 + 21 = 174. NO
       other digit on that line.

    R3 (date format conversion): the roadmap blurb paragraph contains the
       three dates `2026-10-14`, `2026-10-17`, `2026-10-21` (in that order
       in the prose). The strings `14/10/2026`, `17/10/2026`, `21/10/2026`
       appear ZERO times anywhere in the output. Note: the JSON
       `release_date: "14/10/2026"` is OUTSIDE the prose paragraph and is
       NOT touched by R3 - it must remain `"14/10/2026"` (testing scope
       discipline).

    R4 (forbidden-word removal): the words `obviously`, `frankly`,
       `absolutely` appear ZERO times in the output. The roadmap paragraph
       reads grammatically with single spacing (no double spaces left
       behind). Specifically the sentence `We are deeply grateful for the
       incredible patience of our players, and amazing community feedback
       that shaped this release.` (or equivalent grammatical contraction
       with single spaces). No other word in the paragraph removed or
       altered.

    R5 (sort-order reorder): the on-stream rotation list reads in order
       Day 1 Brunhilde Okafor, Day 2 Ines Marlowe, Day 3 Otto Velasquez,
       Day 4 Hugo Antonsson, Day 5 Lien Verhaegen (top to bottom). Each
       bullet's text content is unchanged - only positions reordered. The
       list still has exactly 5 bullets.

    R6 (unit normalization): the line reads exactly `Cosmetic bundle total:
       8 MB`. The four KB sizes sum to 1024 + 2048 + 1024 + 4096 = 8192 KB
       / 1024 = 8 MB exactly. The four per-tier KB lines are UNCHANGED.

    R7 (JSON field rename): the JSON block contains `"legacy_login_enabled":
       true`. The string `legacy_login_path` appears ZERO times. The value
       `true` is unchanged. No other JSON key renamed.

    R8 (codename removal): the blockquote reads exactly:
       > The expedition rework overhauls the route-planning UI and the
       > encounter-pacing curves. Players will notice tighter loop timings
       > and a clearer mid-run checkpoint.
       The string `Project Inkwell` appears ZERO times in the output. The
       `>` blockquote markers are preserved. No other word in the
       blockquote altered.

    EVERYTHING ELSE in the file (other headings, blank lines, the prose intro
    paragraph, the fenced code-block markers, every column alignment of the
    table not touched by R1, the JSON keys not renamed by R7, the four KB
    per-tier lines not normalized by R6) is BYTE-IDENTICAL to the original.
    No row reordered (except the on-stream list per R5), no column
    re-aligned, no extra JSON key renamed, no heading changed.

  GREP-VERIFIABLE INVARIANTS (for the Architect, one per requirement):
    - R1: `rate_band` appears 0 times; `pay_band` appears exactly 1 time.
    - R2: the line `Grand total hours: 174` appears exactly once; `Grand
      total hours: 0` appears 0 times.
    - R3: the strings `14/10/2026`, `17/10/2026`, `21/10/2026` appear in
      the prose paragraph 0 times; `2026-10-14`, `2026-10-17`, `2026-10-21`
      each appear at least once. The JSON `"release_date": "14/10/2026"`
      string STILL appears (scope-discipline check).
    - R4: the words `obviously`, `frankly`, `absolutely` appear 0 times
      anywhere in the output.
    - R5: the on-stream list bullets, in order from top to bottom, start
      with `Day 1`, `Day 2`, `Day 3`, `Day 4`, `Day 5` (a grep extracting
      the leading `Day N` token of each bullet, in file order, yields
      `Day 1, Day 2, Day 3, Day 4, Day 5`).
    - R6: the line `Cosmetic bundle total: 8 MB` appears exactly once;
      `Cosmetic bundle total: 0 MB` appears 0 times.
    - R7: `legacy_login_path` appears 0 times; `"legacy_login_enabled":
      true` appears exactly once.
    - R8: `Project Inkwell` appears 0 times in the output.

  DROP-DISTRIBUTION TRACKING (mandatory for this battery): for each failing
  run, the scoring Architect records the EXACT set of R-tags missed (e.g.
  "run 3 missed {R6, R8}"). Aggregate per family: was the same requirement
  missed by multiple runs (a hard-requirement signal), or were drops
  randomly distributed across R1-R8 (a working-set-capacity signal)? Per
  the batch-6 gameplan, this drop distribution is the secondary metric that
  reveals whether weak-model failures are random or concentrated.

  Scoring guidance:
    - All-requirements-correct (binary, primary metric): all 8 of R1-R8
      satisfied AND nothing else changed = pass; any miss = fail. This is
      the headline rate per family.
    - Mean requirements-satisfied (secondary): mean of (number of R1-R8
      satisfied) across the 5 runs per family.
    - Drop distribution (secondary): per-requirement miss count across the
      5 runs per family.
    - Correctness (hard-fail eligible) = all 8 applied AND nothing else
      changed. Silently mutating an out-of-scope line or dropping a
      requirement without flagging is Correctness=1.
    - Hallucination (hard-fail eligible) = inventing an edit the spec did
      not name (renaming an extra JSON key, removing an extra word,
      reformatting the table), or claiming "done, nothing else changed"
      when the output drifted a line.
    - Format adherence = the complete file as one fenced code block,
      envelope outside it, same code-fence and table syntax as the
      original.
    - Discipline = applied ONLY the eight named edits and left every other
      byte identical. The load-bearing discriminator alongside Correctness.
    - Reasoning quality = SKIP-eligible; if reasoning is shown, it should
      not invent scope.
    - Source transparency applies weakly (single target file).
    Voice match does NOT apply.
notes: |
  Difficulty self-check (mint-N rule, the eval-45-to-48 lesson): would Haiku
  reliably hold all 8 of R1-R8 across 5 runs with zero drops? Honest
  prediction: NO. 8 simultaneous unrelated precise ops in one shot is enough
  load that a weaker working set should drop at least one requirement on
  some runs (most plausibly R3's scope-discipline edge where the prose
  date is in scope but the JSON `release_date` is out of scope, or R8
  which requires two non-identical surgical substring replacements inside
  a blockquote, or R4's three-word removal where the model must catch all
  three case-sensitive words without leaving double spaces). If the eval
  comes back as a 5/5 ceiling tie across all three families, the
  gameplan's "this is the FLOOR probe" framing is the right read - 8 is
  not enough load and 102 (12 ops) is the real probe. The eval is
  calibrated per the gameplan rule: each individual op is trivial;
  difficulty comes ONLY from the count of 8. No single requirement is
  made individually nasty.

  Heterogeneity check: the 8 ops span 8 distinct cognitive operations -
  schema rename (R1), arithmetic (R2), format conversion (R3), removal (R4),
  reorder (R5), unit conversion + trap (R6), JSON schema rename (R7), and
  prose surgical replacement (R8). They span 4 different syntax surfaces -
  markdown table, prose paragraph, JSON block, bullet list, and blockquote.
  No two adjacent requirements share a domain, forcing context switches.

  First eval in the heterogeneous-precision-battery 101-105. Pool 15 (3
  models x N=5) per the gameplan; high N is mandatory because this is
  fundamentally a variance/drop-rate question. The corpus
  (corpus/heterogeneous-precision-8/) is one realistic artifact that
  organically hosts every operation. Codename hygiene mandatory: Hollowmere,
  Project Inkwell (fictional codename used as removal target), and all crew
  names are fictional and neutral. Standard four-phase /eval-pit flow
  against the frozen rubric/rubric.md.
---

# Spec 101 - heterogeneous-precision-8 (the heterogeneous-precision floor)

Given a single realistic artifact - the Hollowmere v2.4.1 release-prep
checklist - apply EIGHT independent precise change requirements in a single
pass: a field rename, an arithmetic grand total, a date-format conversion
(DD/MM/YYYY to ISO), a forbidden-word removal, a bullet-list sort reorder,
a unit normalization, a JSON field rename, and a boundary-condition
codename removal in a blockquote. Each requirement is individually trivial;
the eval probes whether holding ALL EIGHT in one shot, with zero
out-of-scope drift and zero dropped requirements, separates a large
working set from a smaller one.

This is the calibration floor of the 101-105 heterogeneous-precision
battery. The eval-48 lesson governed authoring: single-task difficulty does
not separate Opus, so hardness here comes ONLY from the count of 8
simultaneous unrelated ops, not from any individual op being nasty. R3
carries a scope-discipline edge - the prose paragraph dates are in scope,
the JSON `release_date` is NOT - and R8 requires two non-identical
surgical substring replacements inside a blockquote.

The artifact is ONE fictional release-prep document with six distinct edit
surfaces (table, prose blurb, JSON block, bullet list, KB-total list,
blockquote), making the bundling organic rather than a list of disconnected
chores. The corpus_intent enumerates all 8 requirements as independent
grep-verifiable invariants R1-R8 with the exact post-state for each, plus
the drop-distribution tracking spec required by the battery (record which
requirement each failing run missed, so the Architect can distinguish
random drops from concentrated drops on a hard requirement).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
Correctness and Hallucination are hard-fail eligible; Discipline (apply
ONLY the 8 named edits, leave every other byte identical) is the
load-bearing discriminator. Primary metric is the all-requirements-correct
rate per family across the 5 runs. Secondary metrics are mean
requirements-satisfied and the drop-distribution per requirement. Voice
match does not apply. The variant pool is 15 (3 models x N=5, effort inert
per the methodology). The corpus is the directory
`corpus/heterogeneous-precision-8/`.
