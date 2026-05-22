# Evidence - N=10 Cross-Eval Findings

The first day's evidence from the framework's launch (2026-05-19). 10 completed evals across 5+ task classes. This dossier is both **proof-of-method** ("here is what the method produces when applied") AND a **baseline routing reference** for your own decisions until your own evals supersede.

> **Note on framework version:** this dataset was produced under the v1.4 12-variant model+effort pool (Haiku/Sonnet/Opus across low/medium/high/xhigh/max). v1.5 later changed the dispatch default to a 9-variant model-only pool (effort is not a current dispatch dimension - it may be revisited), but the model-level findings recorded here still hold.

> All confidence labels are calibrated against the N=10 dataset. Read these as starting hypotheses, not laws. Run your own evals to confirm or refute.

---

## Pattern 1 - Model tracks task TYPE before DIFFICULTY (HIGH confidence)

**Verdict:** practical winner is the cheapest sufficient model, where "sufficient" varies by task class but Opus is never the floor.

Across 10 evals covering 5+ task classes, the cost-adjusted winner was Haiku 4.5 in 7/10, Sonnet 4.6 in 2/10, and never Opus 4.7. Task TYPE (retrieval / synthesis / code-gen / repair / drafting / diagram) determines the floor more than task DIFFICULTY (corpus size, file count, judgment depth).

**Implication:** route by task type first. Difficulty modulates inside a type, but rarely promotes across model families.

---

## Pattern 2 - Opus xhigh effort saturation - 0-for-10 practical wins (HIGH confidence)

**Verdict:** Opus xhigh as default routing for any bounded task should be retired.

Within-Opus gaps across the first 8 evals where data was clean:

| Eval | Opus medium | Opus xhigh | Direction |
|------|-------------|------------|-----------|
| #1 | 3.50 | 2.91 | medium wins |
| #2 | 4.848 | 4.697 | medium wins |
| #3 | 5.00 | 4.45 | medium wins |
| #4 | 16.375 | 16.45 | within tie zone, cheaper effort wins |
| #5 | 80.5 | 77.5 | medium wins (outside tie zone) |
| #6 | 82.375 | 84.25 | xhigh slightly higher but cost-override fires, medium wins practical |
| #7 | task ceiling hit, all variants tied | | within-family inversion: lower effort wins |
| #8 | 16.375 | 16.375 | tie within Opus, medium wins on cost-override |

xhigh quality lead in eval #6 (narrow, 2.03% normalized) was the FIRST quality crack across 6 evals. Cost-override still pushed practical pick to medium. Across 10 evals total: 0 practical wins for xhigh.

**Mechanism:** effort tax (verbosity, over-elaboration, idiosyncratic structural choices) without quality buy.

---

## Pattern 3 - Within-family inversion: Haiku low > Haiku high (HIGH confidence)

**Verdict:** Haiku low dominates across the board. Haiku high has three distinct failure mode signatures.

Per-family effort scaling across evals 2-6:

| Family | Pattern at N=6 | Failure modes for Haiku high |
|--------|----------------|--------------------------------|
| Sonnet | Inverted on bounded tasks, normal on multi-file synthesis + voice work | n/a |
| Haiku | Inversion HARDENED at N=6 - low has run the table on evals 4-6 | Phantom precedent fabrication (#6), record dual-listing under scale (#5), over-elaboration on bounded tasks (#3, #4) |

The "high effort = better" intuition is wrong for Haiku 4.5. Haiku high has demonstrated three distinct failure modes across three evals; this is not noise.

---

## Pattern 4 - Cheapest SUFFICIENT model wins, not cheapest always (HIGH confidence)

**Verdict:** there is a floor per task class. Below the floor, cheaper does not win. At or above the floor, cost-override fires consistently.

Practical winners by family across evals 1-6:

- Haiku: 5 of 6 (#1, #2, #4, #5, #6)
- Sonnet: 1 of 6 (#3 - single-file code-gen from spec)
- Opus: 0 of 6

The "sufficient floor" varies by task class:

- **Retrieval / compress / multi-file synthesis / code repair / voice-adjacent ADR:** Haiku is sufficient floor
- **Single-file code generation from spec:** Sonnet is sufficient floor (Haiku finished bottom in #3)
- **Voice-pure work (Voice dim leading):** Opus medium has the niche (#6 voice score 5.0)

---

## Pattern 5 - Sonnet structural dominance (MED-HIGH confidence)

**Verdict:** Sonnet 4.6 dominates structural-reasoning tasks where layout, parallelism, and shape matter.

From eval #12 (ASCII diagram authoring): top 3 spots ALL Sonnet across 3 efforts (J Sonnet high 77.25, E Sonnet max 76.75, H Sonnet medium 76.50; cluster spread 0.75). Sonnet draws decision shapes explicitly, uses parallel layouts confidently, lands in line target window.

Opus introduced idiosyncratic layouts (swimlane, EXCLUDE-loops, buried gates) at higher rates - exploration bias hurts structural-reasoning tasks.

**Meta-finding from #12:** Haiku 4.5 low (75.50) tied Opus 4.7 max (75.50) at 15x cost ratio. Budget tier genuinely competitive at this complexity.

---

## Pattern 6 - Haiku discipline CONFIRMED for retrieval (HIGH confidence - first confirmed hypothesis)

**Verdict:** verbatim retrieval rewards mechanical discipline over reasoning depth.

From eval #11 (verbatim capture precision): five-way tie at 5.000/5.0 between Opus 4.7 low / medium / xhigh, Sonnet 4.6 max, and Haiku 4.5 high. Haiku high won practical via cost-override rule 1 (gap 0 + cost ratio 15x vs Opus, 3x vs Sonnet).

Effort scaling within Opus provided ZERO quality gain (low/medium/xhigh all tied at top). Sonnet 4.6 high Pass-1 outlier resolved by N=3 reruns (~4.6 mean, not 3.77 - sample variance, not weakness).

This was the FIRST CONFIRMED hypothesis across the framework. Strong evidence for routing verbatim / retrieval to Haiku high.

---

## Pattern 7 - Opus medium voice-niche (LOW confidence, N=1)

**Verdict:** Opus medium has at least ONE confirmed niche - voice-pure tasks where canonical-anchor density leads the rubric.

From eval #6 (ambiguous ADR drafting): Opus medium scored 5.0 on Voice (only 5.0 in field). Mechanism: a single canonical sentence landing three core voice anchors in one image.

Sonnet 4.6 high used metaphor density + builder-declarative cadence to score 4.5 on Voice. Different mechanism, valid pattern. Haiku families struggled with Voice across the board.

**Caveat:** single eval observation. Mechanism is specific and reproducible, but generalization needs more voice-active evals.

---

## Model-task-fit map (generic - update with your own evals)

| Task class | Best model + effort (quality) | Best model + effort (practical) | Confidence | Eval(s) |
|------------|--------------------------------|----------------------------------|------------|---------|
| Multi-file synthesis (small N, 4-5 files) | Haiku 4.5 high OR Sonnet 4.6 high (tie) | Haiku 4.5 high | MED-HIGH | #2 |
| Multi-file synthesis (large N, 10 files) | Opus 4.7 medium (by 0.6%) | Haiku 4.5 low | MED | #5 |
| Code generation (simple scope, single-file) | Sonnet 4.6 low | Sonnet 4.6 low | MED | #3 |
| Code repair (precision, single-file, bug-hunt) | Sonnet 4.6 low | Haiku 4.5 low | MED | #4 |
| ADR drafting (judgment + ambiguity + voice) | Sonnet 4.6 high | Haiku 4.5 low | MED | #6 |
| Code-refactor (3-file bounded scope) | tie (task ceiling) | Haiku 4.5 low | MED | #7 |
| Root-cause analysis (well-instrumented traces) | Opus 4.7 max | Haiku 4.5 low | PROVISIONAL | #8 |
| Verbatim capture / retrieval | 5-way tie at 5.0 | Haiku 4.5 high | HIGH (first confirmed) | #11 |
| ASCII diagram authoring | Sonnet 4.6 high | Sonnet 4.6 high | MED-HIGH | #12 |
| Voice-pure drafting (Voice dim leads) | Opus 4.7 medium | Opus 4.7 medium (niche) | LOW (N=1) | #6 |

### Anti-pattern flags

- **Avoid Opus 4.7 xhigh as default for any bounded task** (0/10 practical wins across the dataset)
- **Avoid Haiku 4.5 high outside small-N homogeneous synthesis or verbatim retrieval** (3 distinct failure modes elsewhere)

---

## Tier recommendations from the N=10 dataset

| Agent tier | Evidence-backed pick | Confidence | Source evals |
|------------|----------------------|------------|--------------|
| Scout | Haiku 4.5 low (default) or high (verbatim retrieval) | HIGH | #2, #11 |
| Analyst | Sonnet 4.6 low (bounded), Sonnet 4.6 high (heterogeneous) | MED | #3, #4, #5, #6 |
| Builder | Sonnet 4.6 low (quality default), Haiku 4.5 low (cost-override) | HIGH | #3, #4 |
| Scribe | TBD (voice-critical eval pending) | LOW | - |
| Engineer | Sonnet 4.6 high (default), Opus 4.7 medium (judgment-heavy) | MED | #4, #8 |
| Researcher | Opus 4.7 medium (synthesis) or Sonnet 4.6 high (cost-bridge) | MED | #5 cross-eval |
| Architect | Opus 4.7 medium (default), Sonnet 4.6 high (ambiguous ADRs) | MED | #6 |

**xhigh retired across all tiers** (0-for-10 practical wins).

---

## How to read this dossier

These patterns came out of a single day's evals on one builder's stack. They are **directional**, not absolute. Your task mix may surface different thresholds, different floors, different niches.

The right use of this evidence:

1. **Start here** - use the model-task-fit map as your initial routing default.
2. **Run your own evals** on the task classes that matter most to your team.
3. **Adjust** the map as your evidence accumulates. Cost-override thresholds in particular are policy, not math; tune to your team's economics.
4. **Contribute back** if you find patterns that confirm, refute, or extend what's here.

The framework's job is to give you a structure where evidence can compose - across evals, across teams, across time. This dossier is the seed dataset.
