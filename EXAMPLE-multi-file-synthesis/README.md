# EXAMPLE eval - multi-file-synthesis

A fully-synthetic, completed eval folder. Its only job is to show the exact shape an
eval takes from end to end, so a curator or contributor can see every artifact a real
run produces without having to run one. All content here is invented (a fictional
"Acme Logistics" API). There is zero private content.

## What this eval demonstrates

The task category is **multi-file-synthesis**: the prompt under test hands the model
three overlapping source files and asks for ONE structured status brief that connects
threads ACROSS the files (not three separate summaries). This is a good reference task
because the quality signal is legible - you can see which variants found the cross-file
connections, which stayed disciplined, which fabricated, and which ignored the output
contract.

## The decision it reached

- **Quality winner:** Sonnet 4.6 medium (5.0/5.0) - flawless cross-file synthesis with
  an explicit combined-urgency ranking.
- **Practical winner:** Haiku 4.5 low (4.62/5.0) - the cross-family cost-override fired
  (0.38 quality gap at a 7x cost ratio, so the cheaper variant wins per the frozen
  rubric). For bounded synthesis where the inputs are present, Haiku low is the route.
- Two variants were eliminated for opposite reasons: one fabricated facts not in the
  corpus (Hallucination hard-fail), one ignored the required output envelope (binary
  instruction-following gate FAIL). Together they show why sealed scoring plus the gate
  catch both the fluent-but-wrong and the correct-but-non-compliant failure classes.

Full reasoning is in `tally.md`.

## File manifest

| File | What it is |
|------|------------|
| `README.md` | This file - summary + the decision reached. |
| `prompt.md` | The synthetic prompt under test, with frontmatter (`task_category`, `corpus_intent`, `corpus_delivered`, `corpus_match`, `data_source`). |
| `rubric.md` | A pointer to the frozen `rubric/rubric.md` plus task-specific scoring notes (the rubric is never forked per-eval). |
| `corpus/api-changelog.md` | Synthetic source file 1 of 3. |
| `corpus/support-tickets.md` | Synthetic source file 2 of 3. |
| `corpus/roadmap-notes.md` | Synthetic source file 3 of 3. |
| `variants/A.md` ... `variants/F.md` | The six variant outputs (reduced-N example pool). |
| `variants/key.md` | The sealed identity reveal (label -> model + effort). Sealed until Pass 2 in a real run; shown here for teaching. |
| `scores.md` | Pass 1 sealed scoring: per-variant 9-dimension scores, the binary gate result, and a qualitative note each. |
| `tally.md` | Pass 2/3 synthesis: reveal, cost-override trace, per-dimension highlights, scoreboard row, surprises, and a paste-back return block. |

## Reduced-N note

This pool is **6 variants (A-F)**, a reduced-N example chosen for legibility. The
production default is the **9-variant model-only pool** (Haiku x3, Sonnet x3, Opus x3).
Reduced-N is a legitimate mode when targeting a specific question; here it keeps the
reference readable. The cost multipliers in `variants/key.md` are illustrative
placeholders, not live pricing.

## This is a reference, NOT a live run target

This folder is a static teaching artifact. It is NOT consumed by Stan's `/eval-run`
orchestrator. Live runs are driven by lightweight `specs/NN-slug.md` definition files
that point at `corpus/` inputs; each run writes transient results to `outbox/` and ships
them via `scripts/send-eval.sh` to a `run/<timestamp>` branch. To author a runnable eval,
add a spec under `specs/` and a corpus under `corpus/`, not a folder like this one. See
`commands/eval-run.md` and `GAUNTLET_QUEUE.md`.
