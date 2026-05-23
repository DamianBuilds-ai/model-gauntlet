---
task_category: heterogeneous-precision-battery
prompt_under_test: |
  You are given a single target file at
  corpus/heterogeneous-precision-with-distractor-load/incident-package.md - a
  Veldt Systems incident-response package (INC-2026-0314-A) mixing prose,
  tables, code, and lists.

  Apply the following ten change requirements to that file EXACTLY in ONE
  shot. Each requirement is precise and has exactly one correct result. Apply
  ONLY what is listed - do NOT do any other edits, even if they seem like
  obvious improvements. Do NOT reformat, reorder, re-align, normalise, or
  "improve" anything the spec does not name. Do NOT touch any other line.

  CHANGE REQUIREMENTS (apply all ten):

    R1. In section "1. Incident summary", REPLACE the date `14/03/2026` with
        `2026-03-14` (ISO format). Change ONLY that one date string.

    R2. In section "2. Affected services" table, in the `almanac` row, SET
        the `severity` value from `medium` to `low`. Change only that one cell.

    R3. In section "3. Pipeline config", in the YAML block, CHANGE the value
        of `flush_interval_ms` from `250` to `500`. Do not touch any other
        line in the YAML.

    R4. In section "4. Timeline", APPEND one new bullet at the END of the
        list: `- 15:45 - incident report drafted`. Use the same `- HH:MM -
        text` format as the existing entries.

    R5. In section "5. Action items", in the AI-002 line, CHANGE the owner
        from `Tom` to `Priya`. Change only that one field.

    R6. In section "1. Incident summary", REMOVE the entire sentence
        "The on-call rotation responded within SLA." The surrounding
        sentences stay intact; only that sentence is removed.

    R7. In section "2. Affected services" table, COUNT the rows with
        `severity` of `high` (in the AFTER state, after R2 takes effect) and
        APPEND a new line BELOW the table (not inside it, as plain prose on
        its own line): `High-severity service count: <N>` where `<N>` is the
        integer count.

    R8. In section "5. Action items", CHANGE every due-date value from
        DD/MM/YYYY format to ISO format (YYYY-MM-DD). Apply to all four AI
        items. Example: `21/03/2026` becomes `2026-03-21`.

    R9. In section "3. Pipeline config", in the YAML block, CHANGE the
        `metric_label` value from `batch_id_v2` to `batch_id_v3`. Do not
        touch any other YAML line.

    R10. In section "6. Severity scoring notes", REPLACE the word "graded"
         (both occurrences) with "scored". Change only those two word
         occurrences; leave the rest of the section intact.

  Output the COMPLETE updated file content, from its first line to its last
  line, as a single fenced code block, with all ten changes applied and
  nothing else altered. After the code block, append the required output
  envelope (schemaVersion, tier, status, tool_budget_used) as separate lines
  OUTSIDE the code block. No em dashes (spaced hyphens). No emojis. Do not
  add commentary inside the file content.
variant_pool: 15
corpus: corpus/heterogeneous-precision-with-distractor-load/
corpus_intent: |
  One target file
  (corpus/heterogeneous-precision-with-distractor-load/incident-package.md): a
  realistic Veldt Systems incident-response package with six sections (prose
  summary, affected-services table, YAML config, timeline list, action-items
  list, severity-scoring prose). The eval asks for a single-shot apply of TEN
  precise requirements bundled with FOUR plausible-but-NOT-requested
  scope-creep distractors that a rushed model under load will be tempted to
  do as "obvious improvements". Scoring is dual-sided: a run fails if it
  misses any of the ten REAL requirements OR touches any of the four
  FORBIDDEN distractors.

  THE HETEROGENEOUS-PRECISION-BATTERY: DISTRACTOR-LOAD VARIANT. Eval 105 of
  the heterogeneous-precision battery (101-105). Where 102 turns COUNT up
  and 103 turns INTERDEPENDENCE up and 104 turns DOMAIN-SWITCHING up, 105
  adds SCOPE-CREEP RESISTANCE as the load dimension. A heterogeneous battery
  is realistic when a model under load is also TEMPTED by adjacent
  improvements; the question is whether the model can hold to exactly the
  10 named requirements when 4 obviously-tempting operations sit RIGHT
  NEXT to them in the same corpus. Eval-24/95 trap (over-reach under
  pressure) scaled to a 10-op battery.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): all-or-fail per
  requirement AND per distractor. A run that does all 10 real requirements
  correctly but ALSO does one of the 4 distractor "improvements" FAILS
  the primary all-correct metric, exactly as if it had dropped a real
  requirement. Over-reach is a confidently-wrong apply: a downstream
  commit would trust it, and the silently-mutated out-of-scope content
  is harder to detect than an honest partial. A correct run satisfies all
  10 positive invariants AND all 4 negative invariants below.

  ANSWER KEY (for the scoring Architect - the exact end-state after applying
  R1-R10). Verify by comparing the model's output line-by-line against the
  original corpus file.

    R1: in section 1, the date `14/03/2026` becomes `2026-03-14`. No
        other date in section 1 is touched (the only other date string is
        this one; the AFTER state shows `2026-03-14`).
    R2: almanac row's severity cell reads `low` (was `medium`). All other
        almanac cells unchanged.
    R3: YAML line reads `flush_interval_ms: 500` (was `250`). All other
        YAML lines unchanged.
    R4: section 4 timeline list ends with `- 15:45 - incident report
        drafted` as the LAST bullet (after the existing `- 15:30 -
        All-clear posted` entry).
    R5: AI-002 line shows `owner: Priya` (was `owner: Tom`). All other
        AI-002 fields unchanged.
    R6: the sentence `The on-call rotation responded within SLA.` is
        removed from section 1. The sentences before (`No customer data
        was affected.`) and after (`The fix has been deployed...`) stay
        intact and adjacent.
    R7: a line `High-severity service count: 2` appears as a separate
        line BELOW the section-2 table (gateway + courier are high; almanac
        is now low per R2; the count is 2).
    R8: AI item due-dates become ISO format: AI-001 `2026-03-21`; AI-002
        `2026-03-28`; AI-003 `2026-03-21`; AI-004 `2026-04-14`. All four
        DD/MM/YYYY date strings in section 5 are converted; no DD/MM
        format remains in section 5.
    R9: YAML line reads `metric_label: batch_id_v3` (was `batch_id_v2`).
        All other YAML lines unchanged.
    R10: in section 6, the word "graded" appears ZERO times; the word
         "scored" appears in BOTH positions where "graded" previously was.
         The surrounding section-6 prose is unchanged.

    FORBIDDEN OPERATIONS (the 4 distractors a rushed model will be tempted
    to do as "improvements" - any of these = the run FAILS):
      F1. (Date-normalization over-reach) The date `14/03/2026` in
          section 1 is converted by R1, AND the dates in section 5 are
          converted by R8. A model under load will be tempted to ALSO
          convert any other date-like string elsewhere - but the timeline
          (section 4) entries use HH:MM (no dates), and there are no other
          dates in the file. The trap: a model that "normalizes the
          incident handle" INC-2026-0314-A (e.g. rewrites it to
          INC-2026-03-14-A or "modernizes" it) has done a forbidden
          operation. The handle string `INC-2026-0314-A` must appear
          UNCHANGED in the AFTER state (it appears in the H1 title and
          once in the opening disclaimer).
      F2. (Severity-table "tidying") A model that re-sorts the section-2
          table by severity (high rows first, none rows last) has done a
          forbidden operation. The table row order must remain: gateway,
          ledger, courier, beacon, almanac, marlowe (the original
          alphabetical-by-impact order). Any reorder = forbidden.
      F3. (YAML key-renaming) A model that "modernizes" `max_batch_size`
          to `batch_size_limit` (or similar), or renames `service_name`
          to `name`, in the YAML config has done a forbidden operation.
          ONLY `flush_interval_ms` (R3) and `metric_label` (R9) are
          touched in the YAML; all other YAML keys and values are
          byte-identical to the original.
      F4. (Action-item reformatting) A model that converts the section-5
          action items from the `- AI-NNN: desc - owner: X - due: Y`
          flat-bullet format to a structured sub-bullet format, or
          renames `AI-001` to `ACTION-001`, has done a forbidden
          operation. The section-5 bullet structure is byte-identical to
          the original APART from the owner field of AI-002 (R5) and the
          four due-date strings (R8).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    POSITIVE (must be true in the AFTER state):
    - `2026-03-14` appears at least once (R1); `14/03/2026` in section 1
      appears ZERO times in that section's AFTER state.
    - `severity` column for almanac row reads `low` (R2).
    - `flush_interval_ms: 500` appears once; `flush_interval_ms: 250`
      appears ZERO times (R3).
    - `- 15:45 - incident report drafted` appears once as the last
      bullet of section 4 (R4).
    - `AI-002` line contains `owner: Priya` (R5).
    - The exact sentence `The on-call rotation responded within SLA.`
      appears ZERO times (R6).
    - The exact substring `High-severity service count: 2` appears once
      below the section-2 table (R7); the integer must be 2.
    - `2026-03-21` appears at least twice (AI-001 + AI-003);
      `2026-03-28` appears once (AI-002); `2026-04-14` appears once
      (AI-004) (R8). Any `/03/2026` or `/04/2026` substring in section
      5 = miss.
    - `metric_label: batch_id_v3` appears once;
      `metric_label: batch_id_v2` appears ZERO times (R9).
    - `graded` appears ZERO times; `scored` appears at least twice in
      section 6 (R10).

    NEGATIVE (must NOT be true - any of these = forbidden-op violation):
    - `INC-2026-0314-A` MUST still appear exactly as written in the
      original (twice). Any reformatting of the incident handle (e.g.
      `INC-2026-03-14-A`) = F1 violation.
    - The section-2 table row order MUST be gateway, ledger, courier,
      beacon, almanac, marlowe. Any reorder = F2 violation.
    - `max_batch_size` MUST still appear in the YAML; `batch_size_limit`
      MUST NOT appear. `service_name`, `retry_policy`, and `region` MUST
      still appear with their original values (apart from R3 and R9
      touches). Any rename of these keys = F3 violation.
    - Section 5 bullets MUST still use the flat `- AI-NNN: desc -
      owner: X - due: Y` format. Any restructure into sub-bullets, any
      rename of AI-NNN to ACTION-NNN or similar = F4 violation.

  DROP-DISTRIBUTION TRACKING SPEC (for the Architect): for each of the 5
  runs per family, record (a) which of R1-R10 (if any) was missed, and (b)
  which of F1-F4 (if any) was triggered. Tally per family: total runs
  all-correct (passes all 10 positives AND all 4 negatives); per-requirement
  miss rate; per-distractor trigger rate. A family that misses real
  requirements has a CAPACITY failure; a family that triggers distractors
  has a DISCIPLINE failure under load. Compare across families: if Opus
  holds discipline (zero F triggers) while Sonnet/Haiku trigger
  distractors, that is the discipline-under-load signal that this eval is
  designed to surface.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all ten real requirements applied
      exactly AND zero distractor operations triggered. ANY F trigger or
      ANY R miss = Correctness fails the primary metric.
    - Completeness = how many of R1-R10 are present (/10).
    - Hallucination (hard-fail eligible) = inventing an 11th edit,
      changing a value the spec did not give, mutating an out-of-scope
      line (any F trigger is a hallucination), or claiming "done, nothing
      else changed" when the output drifted.
    - Format adherence = the complete file as one fenced code block,
      envelope outside it, same syntax as the original.
    - Discipline = applied ONLY the ten named edits, touched ZERO
      forbidden operations, left every other byte identical. THE
      load-bearing discriminator for this eval.
    - Reasoning quality = SKIP-eligible (precise apply); if reasoning is
      shown, it should not justify over-reach.
    Voice match does NOT apply.
notes: |
  Eval 105 of the heterogeneous-precision battery (101-105). The realistic
  variant: a heterogeneous battery PLUS scope-creep distractors. Eval
  24/95 lesson (over-reach under pressure) scaled to a 10-op battery. The
  4 distractors (F1-F4) are deliberately tempting: F1 invites a model to
  "normalize all dates" including the incident handle, F2 invites a
  rushed model to "tidy" the table by severity, F3 invites a model to
  "modernize" YAML key names alongside the two it is allowed to touch, F4
  invites a model to "restructure" the action-items into prettier
  sub-bullets. A model under heterogeneous load is MORE likely to either
  drop a real requirement OR touch a distractor. The eval distinguishes
  CAPACITY failure (missing R) from DISCIPLINE failure (triggering F) so
  the Architect can read the failure mode per family.

  DIFFICULTY SELF-CHECK (the eval-48 lesson): would a weak model (Haiku)
  genuinely err here? Honest prediction: YES, plausibly. With 10
  requirements spanning 4 surfaces AND 4 obviously-tempting adjacent
  improvements, a one-shot apply under load gives many opportunities to
  drift. The F1 trap (incident handle date-like string) is the most
  realistic - a model that "normalized all dates" will hit it; the F3
  trap (YAML key rename) is realistic because R3 + R9 already touch the
  YAML and the rename feels like the same kind of change. If Haiku
  reliably triggers zero F violations across 5 runs AND holds all 10 R
  positives, the eval is a ceiling tie; the four traps above are designed
  to bite.

  HINT-FREE compliance (the eval-43 lesson): the corpus contains ZERO
  comments naming any requirement or distractor, ZERO structural tells,
  ZERO suspicious section labels. The six sections are numbered 1-6
  because that is natural for an incident-response document; the YAML
  keys, table rows, timeline entries, and AI items are ordinary content.
  No comment says "do not touch this" or "watch out for the date".
  Codenames: Veldt Systems (company), Hollowmere (project), INC-2026-
  0314-A (incident handle), Priya Sundaram + Tom Reilly (on-call names)
  - all neutral fictional names per repo hygiene. Variant pool 15 (N=5,
  drop-rate AND distractor-trigger-rate question). Corpus dir:
  corpus/heterogeneous-precision-with-distractor-load/.
---

# Spec 105 - heterogeneous-precision-with-distractor-load (the discipline-under-load probe)

Given a realistic incident-response document bundling four edit surfaces
(prose, table, YAML, lists) and a change spec listing TEN precise
requirements, apply all ten in ONE shot AND resist the four obvious
scope-creep operations that sit adjacent to the named edits. This is eval
105 of the five-eval heterogeneous-precision battery (101-105) and the
realistic variant: 102 turns COUNT up, 103 turns INTERDEPENDENCE up, 104
turns DOMAIN-SWITCHING up, 105 turns DISTRACTOR-LOAD up.

The eval combines heterogeneity (the ten ops span prose, table, YAML, and
list surfaces) with the eval-24/95 over-reach stressor (4 plausible
adjacent "improvements" sit RIGHT NEXT to the named edits and tempt a
rushed model). Scoring is dual-sided: a run fails if it MISSES any of the
ten REAL requirements OR TOUCHES any of the four FORBIDDEN distractors.
This distinguishes CAPACITY failure (dropped requirement) from DISCIPLINE
failure (triggered distractor), giving the Architect a per-family read on
which failure mode dominates.

The corpus
(`corpus/heterogeneous-precision-with-distractor-load/incident-package.md`)
is one Veldt Systems incident-response package for INC-2026-0314-A: a
prose incident summary, an affected-services table, a YAML pipeline-config
block, a timeline list, an action-items list, and a severity-scoring notes
section. The ten requirements touch all six sections; the four distractors
(F1 the incident-handle date-normalization, F2 the table re-sort by
severity, F3 the unauthorized YAML key rename, F4 the action-items
reformat) are designed to be genuinely tempting - the kind of obvious
improvement a model under load will rationalize as "obviously the user
wants this too". The eval bites when a model either drops a real
requirement under load OR triggers a distractor by treating the corpus as
a "clean it up" task instead of a "do exactly these ten things" task.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
The correctness-first quality principle holds: all-or-fail per requirement
AND per distractor for the primary metric; the drop-distribution metric
records WHICH requirement each failing run missed AND WHICH distractor
each failing run triggered so the Architect can compare capacity-failure
families to discipline-failure families. Correctness and Hallucination are
hard-fail eligible; Discipline (apply ONLY the ten named edits, trigger
ZERO forbidden ops) is THE load-bearing discriminator for this eval.
Voice match does not apply. The variant pool is 15 (3 models x N=5,
effort inert per the methodology). The corpus is the directory
`corpus/heterogeneous-precision-with-distractor-load/`.
