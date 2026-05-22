---
task_category: mechanical-apply-exact
prompt_under_test: |
  You are given a single target file at
  corpus/mechanical-apply-exact/target-registry.md - a service registry for a
  fictional platform. It contains a markdown table of services, a fenced INI config
  block of feature flags, and a plain bullet list for an on-call rotation.

  Apply the following change specification to that file EXACTLY. These are precise,
  deterministic edits. There is exactly one correct result. Apply ONLY what is listed.
  Do NOT reformat, reorder, re-align, normalise, or "improve" anything the spec does
  not name. Do NOT touch any other line.

  CHANGE SPECIFICATION (apply all four, in this order):

    C1. In the "Registered services" table, INSERT one new row for a service named
        `harbor`, port `8085`, owner `platform-team`, status `active`. Insert it as
        the LAST row of the table (after the `almanac` row). Use the same column
        layout as the existing rows.

    C2. In the same table, the `beacon` row's `status` cell currently reads `retired`.
        SET it to `active`. Change ONLY that one cell. Leave beacon's port and owner
        unchanged.

    C3. In the `[flags]` config block, the line `enable_courier_v2 = false` must be
        SET to `enable_courier_v2 = true`. Change ONLY the value `false` to `true` on
        that one line. Do NOT change `enable_beacon_metrics` (it stays `false`) and do
        NOT change `max_retries`.

    C4. In the "On-call rotation" bullet list, APPEND one new bullet at the END of the
        list, after the `almanac` line: `- harbor: Yuki Tanaka`. Use the same `- key:
        value` bullet format as the existing entries.

  Output the COMPLETE updated file content, from its first line to its last line, as a
  single fenced code block, with all four changes applied and nothing else altered.
  After the code block, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the code block. No em dashes
  (spaced hyphens). No emojis. Do not add commentary inside the file content.
variant_pool: 9
corpus: corpus/mechanical-apply-exact/
corpus_intent: |
  One target file (corpus/mechanical-apply-exact/target-registry.md): a service
  registry with three distinct edit surfaces - a 5-row markdown table, a 4-line fenced
  INI flags block, and a 4-item bullet list. The eval asks for an exact deterministic
  apply of four precise edits (one table-row insert, one table-cell set, one config
  value flip, one bullet append) with one correct end-state and a hard requirement to
  leave everything else byte-identical.

  THE SETTER TEST (Haiku-lightweight-apply vs Sonnet-Builder). A "Setter" is a cheap
  write/apply agent (Haiku) that, after a Scout retrieves, applies a fully-specified
  change itself. The hypothesis: on a TRIVIAL DETERMINISTIC apply - where the spec
  names the exact insert, the exact cell, the exact value flip, the exact appended
  line, and there is no inference or disambiguation - Haiku should match Sonnet, since
  there is one correct edit and cheap-and-reliable is the whole point. The failure mode
  to detect is the opposite: does Haiku confidently-mangle a fully-specified apply
  (drift the unrelated cells, reformat the table, flip the wrong flag, drop a row,
  re-align columns, "tidy" the file) where Sonnet holds it byte-exact? This eval locates
  whether the Setter niche is safe for fully-deterministic applies.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): an apply that LOOKS done but
  silently mutated an out-of-scope line is WORSE than one that honestly applied three of
  four and flagged the fourth. The four highest-signal traps are all OVER-REACH or
  WRONG-TARGET errors: (a) flipping `enable_beacon_metrics` to true as well (it must
  stay false) - confidently-wrong; (b) re-aligning or reformatting the markdown table
  columns or re-sorting the rows (the spec did not ask) - an out-of-scope mutation; (c)
  changing beacon's port or owner while setting its status (only the status cell
  changes); (d) inserting harbor anywhere but as the last table row, or appending the
  on-call bullet anywhere but last. A model that applies exactly the four named edits
  and leaves every other byte identical is correct; a model that "improves" the file is
  confidently wrong. Over-reach is the heaviest penalty here.

  ANSWER KEY (for the scoring Architect - the exact end-state after applying C1-C4).
  Verify by comparing the model's output line-by-line against the original corpus file.

    The "Registered services" table, AFTER, has SIX rows in this order: gateway 8080
    platform-team active; ledger 8081 finance-team active; courier 8082 logistics-team
    active; beacon 8083 platform-team ACTIVE (status changed from retired - C2); almanac
    8084 data-team active; harbor 8085 platform-team active (NEW last row - C1). beacon's
    port (8083) and owner (platform-team) are UNCHANGED.

    The "[flags]" block, AFTER, reads exactly:
      enable_courier_v2 = true   (changed from false - C3)
      enable_ledger_batch = true (UNCHANGED)
      enable_beacon_metrics = false (UNCHANGED - the trap; must stay false)
      max_retries = 3 (UNCHANGED)

    The "On-call rotation" list, AFTER, has FIVE bullets in this order: gateway: Dana
    Okafor; ledger: Priya Sundaram; courier: Tom Reilly; almanac: Sarah Lin; harbor:
    Yuki Tanaka (NEW last bullet - C4).

    Everything else in the file (headings, the prose intro paragraph, blank lines, the
    code-fence markers, column alignment of pre-existing rows) is BYTE-IDENTICAL to the
    original. No row reordered, no column re-aligned, no extra flag touched, no heading
    changed.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - `harbor` appears exactly twice in the output (one table row, one on-call bullet).
    - `8085` appears exactly once. `8083` still appears exactly once and still on the
      beacon row.
    - `retired` appears ZERO times in the AFTER state (C2 removed the only occurrence).
    - `enable_courier_v2 = true` appears once; `enable_courier_v2 = false` appears zero
      times. `enable_beacon_metrics = false` STILL appears once (unchanged). `= true`
      appears on exactly: enable_courier_v2 and enable_ledger_batch (two lines).
    - The table has exactly 6 data rows (7 lines counting the header, 8 counting the
      separator). The on-call list has exactly 5 bullets.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all four edits applied exactly AND nothing else
      changed. Flipping the wrong flag, changing beacon's port/owner, mis-placing the
      insert, or mutating an out-of-scope line is Correctness=1 (a confidently-wrong
      apply that a downstream commit would trust).
    - Completeness = all four of C1-C4 present.
    - Hallucination (hard-fail eligible) = inventing a fifth edit, a value the spec did
      not give, an extra row/flag/bullet, or claiming "done, nothing else changed" when
      the output in fact reformatted or drifted a line.
    - Format adherence = the complete file as one fenced code block, envelope outside it,
      same code-fence and table syntax as the original.
    - Discipline = applied ONLY the four named edits and left every other byte identical
      (no reformat, no re-sort, no re-align, no extra-flag flip). This is the load-bearing
      Setter discriminator.
    - Reasoning quality = SKIP-eligible (this is a near-pure apply); if reasoning is
      shown, it should not invent scope.
    - Source transparency applies weakly (single target file).
    Voice match does NOT apply. The scored discriminators are exact-application of the
    four edits and ZERO out-of-scope drift.
notes: |
  NEW task type and the first of the three Setter-vs-Builder probes (49-51). A "Setter"
  is a lightweight write/apply agent (Haiku) that applies a fully-specified change after
  a Scout retrieves; the Builder (Sonnet) is execution-plus-verification. This eval tests
  the trivial-deterministic-apply niche: four precise edits (table-row insert, one
  table-cell set, one INI value flip, one bullet append) against a single small file,
  each with exactly one correct result and a hard requirement to leave everything else
  byte-identical. The question is whether Haiku matches Sonnet on a fully-deterministic
  apply, or confidently-mangles it (drifts an out-of-scope line, flips the wrong flag,
  reformats the table, mis-places an insert) where Sonnet holds it byte-exact.

  The corpus (corpus/mechanical-apply-exact/) is one target file with three edit
  surfaces (a markdown table, a fenced INI block, a bullet list) so the apply spans more
  than one syntax. The traps are all over-reach / wrong-target: a second flag flipped,
  the table re-aligned or re-sorted, beacon's port/owner changed alongside its status, or
  the insert/append placed in the wrong position. The correctness-first principle holds:
  a confidently-wrong apply (a silently mutated out-of-scope line, a clean-looking but
  reformatted file) is worse than an honest partial. Correctness and Hallucination are
  hard-fail eligible; Discipline (apply ONLY the four edits, change nothing else) is the
  load-bearing discriminator. The answer key gives the exact end-state plus
  grep-verifiable invariants. Voice match does not apply. Standard four-phase /eval-pit
  flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
  inert per the methodology). The corpus is the directory corpus/mechanical-apply-exact/.
---

# Spec 49 - mechanical-apply-exact (the Setter test)

Given a precise, fully-specified change spec and a single target file, apply the
change EXACTLY - insert a named table row, set one named cell, flip one named config
value, append one named bullet - and leave every other byte of the file identical.
This is the first of three Setter-vs-Builder probes (49 exact-single-file, 50
exact-multifile, 51 patch-application).

A "Setter" is Damian's term for a lightweight write/apply agent (Haiku) that, after a
Scout or Explorer retrieves, applies a fully-specified change itself - as opposed to
the Builder (Sonnet, execution plus verification). The expected line is that a Setter
excels on TRIVIAL DETERMINISTIC applies, where there is one correct edit and no
inference, because Haiku is cheap and should be reliable there. This eval tests that
claim directly: does Haiku match Sonnet on a fully-deterministic four-edit apply, or
does Haiku confidently-mangle it - drifting an unrelated cell, flipping the wrong flag,
reformatting the table, or mis-placing an insert - where Sonnet holds it byte-exact.

The corpus (`corpus/mechanical-apply-exact/target-registry.md`) is one small service
registry with three distinct edit surfaces: a five-row markdown table, a four-line
fenced INI flags block, and a four-item bullet list. The four edits (C1 insert harbor
as the last table row, C2 set beacon's status from retired to active, C3 flip
`enable_courier_v2` from false to true, C4 append a harbor on-call bullet) each have
exactly one correct result. The traps are all over-reach or wrong-target: flipping
`enable_beacon_metrics` as well (it must stay false), re-aligning or re-sorting the
table, changing beacon's port or owner alongside its status, or placing the insert /
append anywhere but last.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a confidently-wrong
apply (a silently mutated out-of-scope line, a clean-looking but reformatted file) is
worse than an honest partial that applies three of four and flags the fourth.
Correctness and Hallucination are hard-fail eligible; Discipline - applying ONLY the
four named edits and leaving every other byte identical - is the load-bearing
discriminator, and the answer key provides the exact end-state plus grep-verifiable
invariants for the scoring Architect. Voice match does not apply. The variant pool is 9
(3 models x N=3, effort inert per the methodology). The corpus is the directory
`corpus/mechanical-apply-exact/`.
