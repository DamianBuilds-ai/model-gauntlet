# Rubric for this eval

This eval scores against the FROZEN repo rubric. Do not copy or fork it here -
read the single source of truth:

-> `rubric/rubric.md` (repo root)

That file defines the 9 scored dimensions, the binary instruction-following gate,
the two hard-fail-eligible dimensions (Correctness, Hallucination), the
within-family tiebreaker, and the cross-family cost-override table. The
`scores.md` and `tally.md` in this folder reference those exact dimensions and
thresholds.

Task-specific scoring notes for multi-file-synthesis:
- Correctness here means: claims in the brief are traceable to the corpus files.
- Reasoning quality is heavily weighted by whether the brief CONNECTS threads
  across files (the explicit ask) versus summarizing files in isolation.
- Voice match does NOT apply (this is a synthesis task, not a drafting/voice task)
  and is excluded from the weighted denominator.
- Helpfulness and Discipline DO apply (this is a judgment task - prioritizing
  issues by combined urgency is a judgment call).
- Source transparency applies: does the brief say which file each claim came from?
