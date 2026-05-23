---
task_category: long-task-quality-decay
prompt_under_test: |
  You are given a single source file at
  corpus/long-task-quality-decay/transit-ledger.md - 50 raw vehicle-arrival entries from
  the Hollowmere depot scanner. The file's header describes the normalization rules in
  full (RULE A through RULE E: vehicle code, timestamp, corridor expansion, weight
  conversion, status ENUM). Read the header carefully, then apply the rules to EVERY one
  of the 50 raw entries.

  Output ONE normalized line per raw entry, in the SAME ORDER as the raw log (entries
  01 through 50), each on its own line, in this exact schema:

    [NN] vehicle=<CODE> | iso=<YYYY-MM-DDTHH:MM> | corridor=<EXPANDED> | kg=<INTEGER> | status=<ENUM>

  No headers, no totals, no commentary, no blank lines between entries. Apply the rules
  uniformly - the SAME care for entry 50 as for entry 01. After the 50 lines, append the
  required output envelope (schemaVersion, tier, status, tool_budget_used) as separate
  lines OUTSIDE the entry block. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/long-task-quality-decay/
corpus_intent: |
  One source file (corpus/long-task-quality-decay/transit-ledger.md): 50 sequential raw
  vehicle-arrival entries plus a header that fully specifies five normalization rules
  (vehicle code uppercase prefix; timestamp 12h to 24h ISO with date 2026-05-19;
  corridor abbreviation expansion via a 9-entry table; weight lb-to-kg conversion with
  half-up rounding or kg integer trunc; status free-text-to-ENUM mapping with a
  deterministic tie-break order cleared > flagged > held > rejected). Each individual
  entry is straightforward - one rule per field, mechanical. The eval's whole point is
  WITHIN-TASK POSITIONAL DECAY: does accuracy at entries 40-50 drop versus entries 1-10?
  Does the model start drifting on the corridor table after item 20? Does the lb-to-kg
  rounding start getting sloppy in the second half? Does the status ENUM tie-break get
  forgotten when the same kind of ambiguous note recurs at item 43 that it nailed at
  item 06? This is a single-shot fatigue / positional-drift probe.

  THE POSITIONAL-DECAY HYPOTHESIS. Eval 36 tested 302-item completeness and found NO
  reliable forgetting - models held the list. But that probed PRESENCE/RECALL, not
  per-item ACCURACY under repeated active computation. This eval probes per-item
  computation quality across positions: each item demands five small but real
  computations (uppercase, time conversion, table lookup, unit conversion + rounding,
  ENUM mapping with tie-break). If a model fatigues, the early entries will be near-
  perfect and the late entries will accumulate small mechanical errors (wrong rounded
  kg, missed pm shift, wrong corridor name, wrong tie-break). The scoring Architect
  computes accuracy on items 01-10 vs items 41-50 separately as the headline
  positional-decay metric. If both segments are near-perfect for all three families,
  that mirrors eval 48 - positional decay does NOT reproduce within-task either, and the
  hypothesis is closed.

  QUALITY PRINCIPLE (uniform-attention-across-positions): the scored signal is whether
  per-entry accuracy is FLAT across positions, not just whether the totals look high. A
  model that gets 50/50 right uniformly is correct. A model that gets 10/10 on 01-10 but
  6/10 on 41-50 is exhibiting the failure mode this eval exists to find - and that
  positional gradient is the headline finding even if the total is decent. The scoring
  Architect MUST report per-segment accuracy (01-10, 11-20, 21-30, 31-40, 41-50) so the
  gradient is visible.

  ANSWER KEY (the exact 50 normalized lines, for the scoring Architect to compare
  line-by-line). Each line is independent; score each per-entry as correct or incorrect
  (4 fields per line must all match exactly: iso, corridor, kg, status; the vehicle
  field is uppercase of the raw code and should also match exactly).

    [01] vehicle=TK-204 | iso=2026-05-19T07:42 | corridor=North-Spine | kg=544 | status=flagged
    [02] vehicle=MW-118 | iso=2026-05-19T08:05 | corridor=South-Vault | kg=860 | status=cleared
    [03] vehicle=LP-039 | iso=2026-05-19T08:31 | corridor=East-Arc | kg=1089 | status=held
    [04] vehicle=TK-061 | iso=2026-05-19T09:14 | corridor=Northeast-Cut | kg=540 | status=flagged
    [05] vehicle=MW-227 | iso=2026-05-19T09:48 | corridor=West-Run | kg=816 | status=cleared
    [06] vehicle=LP-152 | iso=2026-05-19T10:02 | corridor=Central-Loop | kg=1100 | status=flagged
    [07] vehicle=TK-088 | iso=2026-05-19T10:39 | corridor=Southwest-Cut | kg=327 | status=rejected
    [08] vehicle=MW-044 | iso=2026-05-19T11:15 | corridor=Northwest-Cut | kg=950 | status=cleared
    [09] vehicle=LP-176 | iso=2026-05-19T11:52 | corridor=Southeast-Cut | kg=658 | status=flagged
    [10] vehicle=TK-130 | iso=2026-05-19T12:08 | corridor=North-Spine | kg=600 | status=held
    [11] vehicle=MW-091 | iso=2026-05-19T12:35 | corridor=South-Vault | kg=735 | status=rejected
    [12] vehicle=LP-005 | iso=2026-05-19T13:14 | corridor=East-Arc | kg=880 | status=cleared
    [13] vehicle=TK-244 | iso=2026-05-19T13:48 | corridor=Northeast-Cut | kg=953 | status=flagged
    [14] vehicle=MW-167 | iso=2026-05-19T14:22 | corridor=West-Run | kg=1340 | status=held
    [15] vehicle=LP-073 | iso=2026-05-19T14:55 | corridor=Central-Loop | kg=345 | status=cleared
    [16] vehicle=TK-022 | iso=2026-05-19T15:30 | corridor=Southwest-Cut | kg=1480 | status=rejected
    [17] vehicle=MW-198 | iso=2026-05-19T16:01 | corridor=Northwest-Cut | kg=449 | status=flagged
    [18] vehicle=LP-115 | iso=2026-05-19T16:38 | corridor=Southeast-Cut | kg=1750 | status=held
    [19] vehicle=TK-159 | iso=2026-05-19T17:12 | corridor=North-Spine | kg=299 | status=cleared
    [20] vehicle=MW-080 | iso=2026-05-19T17:45 | corridor=South-Vault | kg=1290 | status=flagged
    [21] vehicle=LP-203 | iso=2026-05-19T18:18 | corridor=East-Arc | kg=245 | status=rejected
    [22] vehicle=TK-046 | iso=2026-05-19T18:51 | corridor=Northeast-Cut | kg=1860 | status=cleared
    [23] vehicle=MW-134 | iso=2026-05-19T19:24 | corridor=West-Run | kg=503 | status=flagged
    [24] vehicle=LP-067 | iso=2026-05-19T19:58 | corridor=Central-Loop | kg=770 | status=held
    [25] vehicle=TK-181 | iso=2026-05-19T20:32 | corridor=Southwest-Cut | kg=694 | status=cleared
    [26] vehicle=MW-029 | iso=2026-05-19T21:05 | corridor=Northwest-Cut | kg=1240 | status=flagged
    [27] vehicle=LP-142 | iso=2026-05-19T21:39 | corridor=Southeast-Cut | kg=898 | status=rejected
    [28] vehicle=TK-217 | iso=2026-05-19T22:11 | corridor=North-Spine | kg=690 | status=cleared
    [29] vehicle=MW-103 | iso=2026-05-19T22:48 | corridor=South-Vault | kg=640 | status=held
    [30] vehicle=LP-058 | iso=2026-05-19T23:22 | corridor=East-Arc | kg=1080 | status=cleared
    [31] vehicle=TK-095 | iso=2026-05-19T23:55 | corridor=Northeast-Cut | kg=744 | status=flagged
    [32] vehicle=MW-186 | iso=2026-05-19T00:10 | corridor=West-Run | kg=920 | status=cleared
    [33] vehicle=LP-031 | iso=2026-05-19T00:42 | corridor=Central-Loop | kg=826 | status=held
    [34] vehicle=TK-249 | iso=2026-05-19T01:18 | corridor=Southwest-Cut | kg=1370 | status=rejected
    [35] vehicle=MW-076 | iso=2026-05-19T01:50 | corridor=Northwest-Cut | kg=499 | status=flagged
    [36] vehicle=LP-194 | iso=2026-05-19T02:24 | corridor=Southeast-Cut | kg=880 | status=held
    [37] vehicle=TK-138 | iso=2026-05-19T02:58 | corridor=North-Spine | kg=767 | status=cleared
    [38] vehicle=MW-052 | iso=2026-05-19T03:31 | corridor=South-Vault | kg=1240 | status=flagged
    [39] vehicle=LP-211 | iso=2026-05-19T04:04 | corridor=East-Arc | kg=372 | status=held
    [40] vehicle=TK-167 | iso=2026-05-19T04:38 | corridor=Northeast-Cut | kg=1560 | status=rejected
    [41] vehicle=MW-119 | iso=2026-05-19T05:12 | corridor=West-Run | kg=599 | status=cleared
    [42] vehicle=LP-088 | iso=2026-05-19T05:45 | corridor=Central-Loop | kg=950 | status=flagged
    [43] vehicle=TK-033 | iso=2026-05-19T06:19 | corridor=Southwest-Cut | kg=943 | status=cleared
    [44] vehicle=MW-225 | iso=2026-05-19T06:52 | corridor=Northwest-Cut | kg=740 | status=flagged
    [45] vehicle=LP-014 | iso=2026-05-19T07:26 | corridor=Southeast-Cut | kg=531 | status=rejected
    [46] vehicle=TK-201 | iso=2026-05-19T07:59 | corridor=North-Spine | kg=1450 | status=held
    [47] vehicle=MW-068 | iso=2026-05-19T08:33 | corridor=South-Vault | kg=449 | status=cleared
    [48] vehicle=LP-156 | iso=2026-05-19T09:06 | corridor=East-Arc | kg=1280 | status=flagged
    [49] vehicle=TK-110 | iso=2026-05-19T09:40 | corridor=Northeast-Cut | kg=853 | status=held
    [50] vehicle=MW-040 | iso=2026-05-19T10:13 | corridor=Southwest-Cut | kg=860 | status=rejected

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - Output has exactly 50 entry lines, each beginning `[NN] vehicle=` for NN=01..50 in order.
    - Each line matches the schema regex `^\[\d{2}\] vehicle=[A-Z]{2}-\d{3} \| iso=2026-05-19T\d{2}:\d{2} \| corridor=[A-Z][a-z]+(-[A-Z][a-z]+)+ \| kg=\d+ \| status=(cleared|flagged|held|rejected)$`.
    - The 9 corridor strings are spelled exactly as the rule-table specifies (North-Spine,
      South-Vault, East-Arc, West-Run, Northeast-Cut, Northwest-Cut, Southeast-Cut,
      Southwest-Cut, Central-Loop) - any other spelling on any line is a per-entry error.
    - status field is one of the exact lowercase strings {cleared, flagged, held, rejected}.
    - All 30 lb-conversion kg values match the answer key (round-half-up of raw_lb * 0.4536).
    - The 12-hour-to-24-hour conversion handles 12:08 pm -> 12:08 and 12:10 am -> 00:10
      (lines 10 and 32) correctly.
    - Tie-break check on line 06 ("manifest mismatch, weight high"): status=flagged (both
      keywords are in the flagged group, no cross-group ambiguity). Line 15 ("clear, ok"):
      cleared (both in cleared). Line 43 ("ok, cleared"): cleared. No cross-group ties exist
      in the corpus by design - the test is whether the model APPLIES the rule uniformly.

  POSITIONAL-DECAY METRIC (the headline scoring output the Architect MUST report):
    - Accuracy on items 01-10 (segment A).
    - Accuracy on items 11-20 (segment B).
    - Accuracy on items 21-30 (segment C).
    - Accuracy on items 31-40 (segment D).
    - Accuracy on items 41-50 (segment E).
    - Decay delta = (segment A accuracy) - (segment E accuracy). A positive delta is
      positional decay; near-zero means uniform attention; negative means warm-up.
    - Also report per-FIELD error rate (iso, corridor, kg, status) summed across segments
      so the Architect can see WHICH field decays first.

  Scoring guidance:
    - Correctness = per-entry exact match against the answer key, 4 fields per entry.
      Total = N correct / 50. Hard-fail eligible if total < 30/50 (gross failure to follow
      rules rather than positional drift).
    - Completeness = all 50 entries present in order. Missing entries are full failures of
      that position.
    - POSITIONAL DECAY (the load-bearing discriminator, NEW for this eval) = the
      segment-A-minus-segment-E delta. The Architect's headline output is this gradient,
      NOT just the total. A model with total 45/50 distributed 10/9/9/9/8 is uniform
      attention; a model with the same 45/50 distributed 10/10/10/8/7 is showing decay
      even though the total is identical.
    - Hallucination (hard-fail eligible) = inventing fields not in the schema, inventing
      a corridor name not in the table, inventing an ENUM value, fabricating a missing
      raw entry rather than reporting partial.
    - Format adherence = exact schema + correct order + no headers/totals/commentary +
      envelope outside the entry block.
    - Discipline = applied the SAME rules uniformly to all 50, did not start
      paraphrasing/abbreviating in the second half (e.g. "NE-Cut" instead of
      "Northeast-Cut" after item 25 = a discipline drift).
    - Reasoning quality = SKIP-eligible. Voice match does NOT apply.
notes: |
  NEW task type, the within-task positional-decay probe. Eval 36 tested 302-item
  completeness and found NO reliable forgetting (presence/recall held). This eval tests
  the orthogonal question: does per-item COMPUTATION quality decay across positions
  within a single shot? Each of 50 entries requires five small computations (uppercase,
  12h-to-24h time, corridor expansion, lb-to-kg with half-up rounding, free-text-to-ENUM
  with a tie-break). Individually trivial. The hypothesis is that a fatiguing model gets
  10/10 early and drifts to 6-8/10 late on the same rules. The scoring contract is
  designed to make the gradient visible: per-segment accuracy (01-10, 11-20, 21-30,
  31-40, 41-50), plus a decay delta and a per-field error breakdown.

  DIFFICULTY SELF-CHECK (the eval-45-to-48 rule): would a weak model (Haiku) plausibly
  drop something? Yes - the lb-to-kg conversion with half-up rounding is a per-item
  arithmetic operation that compounds attention demand across 30 instances; the 12h-to-
  24h conversion has the 12:00-noon/midnight edge case TWICE (items 10 and 32) that a
  pattern-matching model often gets wrong on one of the two; the ENUM tie-break rule
  with explicit ordering is the kind of fine-grained instruction that drifts as fatigue
  sets in. The corpus also forces a corridor-table lookup on every line with 9 possible
  expansions (not 4) so spelling drift is plausible (e.g. "Northeast" vs "North-East" vs
  "NorthEast Cut"). If Haiku and Sonnet both still score 50/50 uniformly, that mirrors
  eval 36 and the positional-decay hypothesis closes for this corpus class - which IS a
  finding. The risk is a ceiling tie; the design tries to break the ceiling by stacking
  five per-item ops with one numeric, one table-lookup, one edge-case time, and one
  rule-tie-break across 50 positions.

  Pool 9 (3 models x N=3) per the gameplan - the decay gradient is a within-run
  positional metric, not primarily a variance/drop-rate question, so the higher-N pool
  is not needed. Standard four-phase /eval-pit flow against the frozen rubric/rubric.md.
  The corpus is the single file corpus/long-task-quality-decay/transit-ledger.md (whose
  header contains the full rule spec - the prompt only references the path).

  Codename hygiene: Hollowmere depot, vehicle prefixes TK/MW/LP, corridor names
  North-Spine/South-Vault/etc - all neutral fictional. No real platform, company, port,
  or service is referenced.
---

# Spec 110 - long-task-quality-decay

Run a single long structured task - normalize 50 sequential raw vehicle-arrival entries
using five mechanical rules (uppercase, 12h-to-24h ISO conversion, corridor-table
expansion, lb-to-kg conversion with half-up rounding, free-text-to-ENUM mapping with a
deterministic tie-break) - and measure whether per-item accuracy at the END of the run
(items 41-50) drops versus the BEGINNING (items 01-10). This is the within-task
positional-decay probe: the orthogonal question to eval 36, which tested 302-item
PRESENCE/RECALL and found no reliable forgetting. Here the probe is per-item
COMPUTATION quality across positions.

The corpus (`corpus/long-task-quality-decay/transit-ledger.md`) is one file: a header
that fully specifies the five rules, then 50 raw entries with mixed-format timestamps,
9-way corridor abbreviations, mixed kg/lb units, and free-text status notes. Each
individual entry is straightforward; the question is whether a model holds the rules
uniformly across all 50 positions or starts drifting late. The scoring contract is
purpose-built for this signal: the Architect reports accuracy per 10-entry segment
(A=01-10, B=11-20, C=21-30, D=31-40, E=41-50) plus a decay delta (A-E) plus a per-field
error breakdown (iso vs corridor vs kg vs status).

The hypothesis: a fatiguing model produces a positive decay delta (10/10 early,
6-8/10 late on the same rules), and the per-field breakdown reveals which dimension
fatigues first (numeric rounding? table lookup? edge-case time? ENUM tie-break?). The
risk is a ceiling tie that mirrors eval 36 - everyone holds all 50 - in which case the
positional-decay hypothesis closes within-task too, which is itself a useful finding.
The design stacks five per-item ops including one numeric, one 9-way table lookup, two
edge-case 12h-noon/midnight times (items 10 and 32), and one rule-tie-break across 50
positions to make drift plausible. Correctness, Completeness, Discipline (uniform
application), and the new POSITIONAL DECAY metric are scored; Hallucination is
hard-fail eligible; Reasoning quality is skip-eligible; Voice match does not apply. The
variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
single file `corpus/long-task-quality-decay/transit-ledger.md`.
