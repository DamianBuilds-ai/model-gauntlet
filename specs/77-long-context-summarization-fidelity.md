---
task_category: long-context-summarization-fidelity
prompt_under_test: |
  You are given a single large report at
  corpus/long-context-summarization-fidelity/report.md - a fictional "Greendale
  infrastructure review", roughly 150,000 tokens. Read the whole report.

  Produce a FAITHFUL executive summary of the report's KEY FINDINGS. A faithful summary:
    - retains EVERY load-bearing finding in the report (do not drop any material claim,
      no matter where in the document it appears);
    - invents NOTHING - every claim in your summary must be supported by the report;
    - preserves the specific facts and figures (percentages, intervals, distances,
      dollar amounts) accurately - do not round away or distort the numbers.

  Present the summary as a numbered list of the key findings, one finding per item, each
  stated as a specific checkable claim with its figure. Do not pad with background or
  generic methodology prose - capture the findings, nothing more, nothing less.

  Append the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/long-context-summarization-fidelity/
corpus_intent: |
  GENERATED CORPUS. corpus/long-context-summarization-fidelity/report.md is produced
  deterministically by corpus/long-context-summarization-fidelity/generate.py (seed=77).
  The file is ~600,000 chars (~150,000 tokens at ~4 chars/token), a fictional "Greendale
  infrastructure review". To regenerate byte-identically: cd into the corpus dir and run
  `python3 generate.py`. The script asserts each of the 12 key claims appears exactly
  once.

  WHAT THIS EVAL PROBES: long-context summarization FIDELITY - across a ~150k-token
  document, does the model retain ALL 12 load-bearing key claims (scattered evenly from
  ~4% to ~96% of the report among long filler prose) AND invent none. This is the
  summarization-fidelity dimension of the long-context gauntlet gap. The discriminator is
  recall (every key claim retained, including the ones deep in the window) + precision
  (no fabricated finding) + figure-accuracy (numbers preserved, not distorted).

  QUALITY PRINCIPLE (fidelity = full retention + zero invention + accurate figures): two
  symmetric failure modes - OMISSION (dropping a key claim, especially one late in the
  150k window where summarizers lose recall) and INVENTION (adding a finding not in the
  report, or distorting a figure). A summary that captures 11 of 12 honestly is an
  under-recall miss; a summary that adds a 13th plausible-but-absent finding, or rounds
  "78 percent" to "about 80 percent" or "1.4 million" to "over a million", is an
  invention/distortion error. The correct summary states all 12 with their exact figures
  and nothing else.

  ANSWER KEY (the 12 key claims - the scoring Architect verifies by grep on the corpus).
  Each is tagged inline in the corpus as "KEYCLAIM [Kn]:".
    K1  - primary data centre runs at 78 percent of rated power capacity (22 percent headroom).
    K2  - backup generator last load-tested 14 months ago (exceeds 12-month policy).
    K3  - 41 percent of the server fleet is past its 5-year refresh window and out of support.
    K4  - cooling has a single point of failure: one chiller, no N+1 redundancy.
    K5  - network egress capped at 10 Gbps; peak already reaches 9.2 Gbps.
    K6  - DR site is 320 km away but shares the same regional power grid as the primary.
    K7  - backups complete nightly but the last successful restore TEST was 7 months ago.
    K8  - 3 of 5 core switches run firmware with a known unpatched security advisory.
    K9  - colocation contract expires in 9 months; the 6-month renewal-notice clause is overdue by 1 month.
    K10 - overnight cover is a single on-call engineer with no documented secondary escalation.
    K11 - monitoring retains metrics only 14 days, below the 90-day audit requirement.
    K12 - estimated remediation cost is 1.4 million dollars over 18 months.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - In the corpus: `grep -c "KEYCLAIM \[" report.md` == 12; each `KEYCLAIM [Kn]`
      appears exactly once.
    - A CORRECT model summary contains all 12 distinguishing figures: 78, 22, 14, 41,
      N+1 (or "no redundancy"), 10 Gbps, 9.2, 320 km, 7 months, 3 of 5, 9 months, 14
      days, 90-day, 1.4 million, 18 months.
    - RECALL = count of the 12 claims present in the summary (target 12).
    - INVENTION = any claim in the summary with a figure or finding NOT matching one of
      K1-K12 (target 0).
    - FIGURE-DISTORTION = any of the 12 figures rounded/changed (e.g. "about 80 percent"
      for 78, "a million" for 1.4 million) (target 0).

  Scoring guidance:
    - Correctness (hard-fail eligible) = all 12 key claims retained with accurate figures
      AND nothing fabricated. A distorted figure or a fabricated finding is Correctness=1.
    - Completeness (load-bearing here) = recall of all 12 claims; missing a late-window
      claim is the primary failure to detect.
    - Hallucination (hard-fail eligible) = inventing a finding not in the report, or
      stating a figure the report does not.
    - Discipline = captured ONLY the findings; did not pad with the filler methodology
      prose the report is full of.
    - Source transparency = each summary item maps to a real claim in the report.
    - Reasoning quality = SKIP-eligible; this is a fidelity task, not a reasoning task.
    Voice match does NOT apply.
notes: |
  Chat B gap-filler: the long-context summarization-fidelity dimension (~150k tokens),
  rounding out the long-context battery with 75 (needle synthesis, >200k) and 76
  (cross-file refactor, >200k). The corpus is GENERATED by a deterministic seeded Python
  script (corpus/long-context-summarization-fidelity/generate.py, seed=77) emitting
  ~600k chars (~150k tokens) of a fictional "Greendale infrastructure review" with
  exactly 12 enumerable load-bearing key claims tagged inline (KEYCLAIM [Kn]) and
  scattered evenly from ~4% to ~96% among long filler prose. Regenerate byte-identically
  with `python3 generate.py` in the corpus dir; the script asserts each claim appears
  once.

  The probe is fidelity: full retention of all 12 claims (the late-window ones are the
  recall-decay trap) + zero invention + accurate figures (no rounding "78 percent" to
  "about 80", no "1.4 million" to "a million"). Omission and invention/distortion are the
  two symmetric failures. The answer key lists all 12 claims with grep-verifiable
  figure invariants. Correctness and Hallucination are hard-fail eligible; Completeness
  (recall) is the load-bearing discriminator and Discipline (not padding with the
  report's abundant filler) is secondary. Standard four-phase /eval-pit flow against the
  frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert per the
  methodology). The corpus is the directory corpus/long-context-summarization-fidelity/.
---

# Spec 77 - long-context-summarization-fidelity (the long-context fidelity gap)

Hand a model a ~150,000-token fictional infrastructure-review report and ask for a
faithful executive summary of its key findings. The report contains exactly 12 enumerable
load-bearing claims scattered evenly from ~4% to ~96% of the document among long filler
and methodology prose. A faithful summary retains all 12, invents none, and preserves
every figure accurately. This rounds out the long-context battery alongside eval 75
(needle synthesis) and eval 76 (cross-file refactor).

The corpus is GENERATED, not hand-written. `corpus/long-context-summarization-fidelity/
generate.py` (seed=77) emits `report.md` (~600k chars, ~150k tokens) deterministically
and asserts each of the 12 key claims appears exactly once (tagged inline as
KEYCLAIM [Kn] for the scoring Architect). The 12 claims are specific and checkable -
percentages, intervals, distances, a dollar figure - so distortion is detectable.

The discriminator is fidelity along three axes: recall (every key claim retained,
including the ones deep in the 150k window where summarizers lose recall), precision (no
fabricated finding), and figure-accuracy (numbers preserved, not rounded away). The two
symmetric failure modes are omission (dropping a late-window claim) and
invention/distortion (adding an absent finding or rounding "78 percent" to "about 80",
"1.4 million" to "a million"). A summary that captures 11 of 12 honestly is an
under-recall miss; one that pads with the report's abundant methodology filler shows
weak discipline.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
and Hallucination are hard-fail eligible; Completeness (recall of all 12) is the
load-bearing discriminator. Voice match does not apply. The variant pool is 9 (3 models x
N=3, effort inert per the methodology). The corpus is the directory
`corpus/long-context-summarization-fidelity/`.
