# Prompt Eval Method - Methodology Spec

The load-bearing specification of the framework. Defines the variant pool, the rubric, the bias controls, the four execution phases, and the path for both Claude Code users (full agent infrastructure) and non-Claude-Code users (lite path through a single Claude.ai chat).

---

## Table of contents

1. The 9-variant pool
2. The 9-dimension rubric + binary instruction-following gate
3. Three mandatory bias controls
4. Hard-fail eligibility
5. Within-family tiebreaker (BEFORE cross-family cost-override)
6. Cost-override thresholds (cross-family)
7. N >= 3 protocol for bottom-quartile
8. Variance baseline protocol (once per major task category)
9. Corpus integrity
10. The four phases (Phase 0 through Phase 4)
11. For users WITH Claude Code agents (full path)
12. For users WITHOUT Claude Code agents (lite path)
13. Appendix A - Version history
14. Appendix B - Known limitations
15. Appendix C - Future eval ideas

---

## 1. The 9-variant pool

Default variant pool is model-only: each of the three Anthropic models run x3. Effort is NOT a dispatch dimension (the Agent tool pins `model: haiku|sonnet|opus` only), so it is dropped entirely; the 3 reruns per model are variance runs (mean-of-3).

| Label | Model | Run | Notes |
|-------|-------|-----|-------|
| A | Haiku 4.5 | 1 | |
| B | Haiku 4.5 | 2 | variance run |
| C | Haiku 4.5 | 3 | variance run |
| D | Sonnet 4.6 | 1 | |
| E | Sonnet 4.6 | 2 | variance run |
| F | Sonnet 4.6 | 3 | variance run |
| G | Opus 4.7 | 1 | |
| H | Opus 4.7 | 2 | variance run |
| I | Opus 4.7 | 3 | variance run |

Labels A through I are **randomly assigned per eval** (sealed in `variants/key.md`, NOT opened until Pass 2 of scoring). The per-model score is the mean of its 3 reruns. Effort levels (low/medium/high/xhigh/max) are not used: the Agent tool cannot pin them at dispatch, so same-model/different-effort variants produced functionally identical outputs and added noise without signal.

Reduced N (fewer reruns, or dropping a model) is allowed when targeting a specific question (e.g., "is Sonnet enough or do I need Opus?"). v1.5 default is the 9-variant model-only pool.

---

## 2. The 9-dimension rubric + binary instruction-following gate

9 scored dimensions weighted 1.0 to 3.0 anchored, plus one binary PASS/FAIL gate that eliminates non-compliant variants regardless of other scores.

| # | Dimension | Weight | Hard-fail eligible | Conditional | Notes |
|---|-----------|--------|--------------------|-------------|-------|
| 1 | Correctness | 3.0 | YES (score=1 eliminates) | No | Did it produce a true answer? |
| 2 | Completeness | 2.0 | No | No | Did it cover what was asked? |
| 3 | Format adherence | 1.5 | No | No | Output envelope, frontmatter, structure |
| 4 | Scope discipline | 1.5 | No | No | Did it stay in lane / signal scope-exceeded correctly? |
| 5 | Reasoning quality | 2.5 | No | Skip pure-retrieval | Chain visible? Defensible? |
| 6 | Hallucination | 2.5 | YES (score=1 eliminates) | No | Made-up facts, fabricated citations, ghost paths |
| 7 | Voice match | 2.0 | No | Drafting / voice only | Against voice anchor file |
| 8 | Helpfulness | 1.25 | No | Decision / judgment only | Did it deliver useful output given inputs? |
| 9 | Discipline | 1.25 | No | Decision / judgment only | Did it stay within constraints / refuse appropriately? |
| 10 | Source transparency | 1.0 | No | No - applies to all tasks | Citations, sourcing notes, what-was-used disclosure |

**Weighted total formula:** `sum(score * weight) / sum(weights_scored)`. Conditional dimensions excluded when not applicable.

**Hard fails:** any output scoring 1 on Correctness OR Hallucination is eliminated from winner regardless of other scores.

**Binary gate - Instruction-following:** NOT a scored dimension. Applied as PASS/FAIL.

- PASS = variant followed envelope (schemaVersion, tier, status, tool_budget_used), constraints (no em dashes, no emojis), sequential processing rule, scope of prompt, output path.
- FAIL = variant ignored envelope OR violated explicit constraint.

FAIL ELIMINATES from winner contention. Equivalent to Correctness=1 hard-fail.

**Mandatory qualitative observation field per variant** (2-4 sentences capturing character numbers miss). This is the load-bearing field for the final call.

**Scoring scale: 1-5 anchored.** Anchors mandatory in every scoring template:

- **1** - fails the dimension (hallucinates, ignores instruction, off-scope)
- **2** - partial, but meaningful gaps
- **3** - acceptable, meets the bar
- **4** - strong, exceeds bar in one or more sub-aspects
- **5** - exemplary, hard to imagine doing better with this prompt

---

## 3. Three mandatory bias controls

Every eval MUST apply all three. Skipping any one invalidates results.

### 3.1 Sealed identity

Score before model labels revealed. Variant files use random labels (A through I). Model identity sealed in `variants/key.md`, NOT opened until Pass 2.

Architect Pass 1 is instructed to not open key.md; sealed identity discipline is procedural (no technical enforcement), so trust the universal envelope discipline plus your own audit.

### 3.2 Dimension-by-dimension scoring

Score Correctness across ALL variants, then Completeness across ALL variants, etc. Never output-by-output (introduces anchoring bias). Treat each dimension as a separate horizontal sweep.

### 3.3 Length disclosure

Note word count BEFORE scoring. Force the question "more complete or more verbose?" into the qualitative observation field. Without this, longer outputs dominate via reading-ease bias.

---

## 4. Hard-fail eligibility

A variant is hard-fail eliminated if any of:

- Correctness score = 1 (produced wrong answer)
- Hallucination score = 1 (fabricated facts, citations, paths)
- Instruction-following binary gate = FAIL (ignored envelope or violated explicit constraint)

Hard-fail eliminated variants do NOT compete for winner regardless of other scores. They are recorded in the tally for transparency but cannot win.

---

## 5. Within-family tiebreaker (BEFORE cross-family cost-override)

The 3 reruns of the SAME model are variance runs. Resolve them by taking the MEAN of the 3 weighted totals as that model's score (mean-of-3). With the pool now model-only, there is no within-model effort axis to tie-break - the mean-of-3 IS the within-family resolution.

If 2+ DIFFERENT models then score within 0.3 weighted total of each other, that is a cross-family tie - resolve it via the cost-override table below (cheaper model wins in the tie zone):

1. **Cheaper model wins** in the tie zone (< 0.3 weighted gap)
2. **If still tied:** shorter output wins (verbosity penalty)
3. **If still tied:** random selection with note in tally

The mean-of-3 collapse happens BEFORE the general cost-override threshold table below. Resolves intra-model variance cleanly before cross-family comparison.

---

## 6. Cost-override thresholds (cross-family)

After within-family tiebreaker, apply:

| Quality gap (weighted) | Cost ratio (winner vs cheaper) | Winner |
|------------------------|--------------------------------|--------|
| < 0.3 (tie zone) | any | Cheaper wins |
| 0.3 - 0.5 | >= 3x | Cheaper wins |
| 0.5 - 1.0 | >= 5x | Cheaper wins |
| >= 1.0 | any | Quality wins |
| Any | Any | Hard-fail loses regardless |

These thresholds are policy not math - heuristics derived from initial calibration. Different task categories may eventually surface different thresholds. Document threshold changes in changelog.

---

## 7. N >= 3 protocol for bottom-quartile

The 9-variant default already runs each model x3, so every model carries N=3 evidence by default (the mean-of-3 in section 5). This protocol is the FALLBACK for a REDUCED-N spec where a model ran fewer than 3 times.

If a model that has NOT yet reached N=3 scores in the BOTTOM QUARTILE (lowest 25%) of the run:

1. Architect tally MUST flag for re-run
2. Dispatch enough MORE runs of that exact model (fresh prompt + corpus context) to reach N=3
3. If all 3 runs show SAME failure pattern -> confirmed model-specific weakness
4. If runs vary widely -> sample variance, not signal; original score upgraded to "noisy"
5. Update tally with N=3 finding

Prevents a single noisy bottom-quartile result from being treated as evidence of model weakness when it might be sample variance.

---

## 8. Variance baseline protocol (once per major task category)

Before drawing confident conclusions about model-tier differences for a NEW task category:

1. Run a baseline: same model + same prompt + N=5 fresh runs (recommend Haiku 4.5 - cheap)
2. Compute variance of weighted total across the 5 identical-config runs
3. Compare against variance observed between different-model variants
4. If between-runs variance >= between-models variance, the model-tier signal is below noise floor for this task class

Document baseline variance in your scoreboard per task category. Run baseline ONCE per major task category, not per eval.

---

## 9. Corpus integrity

Per-eval folder files (README.md, prompt.md, scores.md, tally.md) carry these frontmatter fields:

- **corpus_intent:** integer or description (e.g., "5 entries from period X to Y")
- **corpus_delivered:** TBD until variant agents complete; auto-filled with actual count processed
- **corpus_match:** auto-set to true if delivered == intent, false if mismatch

If `corpus_match: false`, Architect tally MUST set `status: corpus-mismatch` (not just `complete` with caveat). Findings become officially PROVISIONAL until re-run with matching corpus.

This rule exists because the first eval in the founder dataset silently delivered 2 entries instead of declared 5 due to a broken path - no pre-flight check caught it, results were invalidated retroactively.

---

## 10. The four phases

### Phase 0 - Pre-flight validation + file-safety

Before dispatching ANY variant or Architect:

**a) Validate data source paths exist.** Read prompt.md `data_source` field. Confirm every path exists via `ls` or `test -e`. If any path is broken, HALT + fix prompt.md before proceeding.

**b) Clone long-lived reference files to eval folder `.bak-archive/`.** Before any agent dispatch that might touch them. `.bak-archive/` is `.gitignored`.

```bash
mkdir -p {REPO_ROOT}/prompt-evals/{eval-slug}/.bak-archive
timestamp=$(date -u +%Y%m%dT%H%M%S)
cp {REPO_ROOT}/METHOD.md {REPO_ROOT}/prompt-evals/{eval-slug}/.bak-archive/${timestamp}-METHOD.md
# repeat for any other long-lived reference files your project uses
```

**c) Confirm eval-slug folder structure** (if rerun: variants/key.md present + scores.md + tally.md skeletons + .bak-archive/ exists).

**d) Validate corpus_intent vs corpus_delivered count.** Read frontmatter `corpus_intent`. Count actual files matching corpus pattern.

- If actual < intent: HALT + fix prompt.md or corpus before proceeding.
- If actual > intent: OK to proceed but log in scores.md notes.
- If broken path: same as step (a) HALT.

Only after Phase 0 completes successfully, proceed to Phase 1.

### Phase 1 - Stage + dispatch variants

1. Create eval folder `prompt-evals/{YYYY-MM-DD-eval_slug}/` with standard 6 files: `README.md`, `prompt.md`, `rubric.md`, `scores.md`, `tally.md`, `variants/key.md`.

2. Stamp frontmatter on all eval folder files:
   - `corpus_intent: <N or description>` - what eval was designed for
   - `corpus_delivered: TBD` - filled by variant agents
   - `corpus_match: TBD` - auto-flagged in tally

3. Generate randomized variant-to-label mapping (A through I; 9 labels by default - the 3 models x 3 reruns). Seal in `variants/key.md`.

4. Write per-variant prompt template + assign output paths.

5. Dispatch the 9 variant agents (default) in ONE parallel batch (background) FROM THE MAIN SESSION (depth 1). Each variant is pinned with `model: haiku|sonnet|opus` (model is the only dispatch lever; effort is a no-op). Reduced-N override spawns fewer.

   HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.

6. Each agent writes to `variants/{LABEL}.md`, sealed identity, no model self-reference, no cost estimates.

7. File-safety: pre-write clone to `.bak-archive/{label}-{timestamp}.md` if rerunning existing variant.

### Phase 2 - Architect Pass 1 sealed scoring

After all variants land:

- Dispatch ONE Architect FROM THE MAIN SESSION (depth 1), on OPUS (Opus 4.7 - "on max" tier). NOT from inside any runner sub-agent.
- Read variants/{A through I}.md WITHOUT opening key.md
- Score 9 dimensions dimension-by-dimension across ALL variants
- Apply Instruction-following PASS/FAIL gate
- Write to scores.md per template with qualitative observation per variant (mandatory, written LAST)
- Length disclosure: word counts captured BEFORE scoring

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.

### Phase 3 - Architect Pass 2 reveal + Pass 3 cost-adjust + tally

After Pass 1:

- Dispatch SECOND Architect FROM THE MAIN SESSION (depth 1), on OPUS (Opus 4.7). NOT from inside any runner sub-agent.
- Read scores.md + open key.md

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.

- Apply 9-dim rubric + Instruction-following binary gate
  - If any variant fails Instruction-following gate, ELIMINATE
  - If any variant scores 1 on Correctness or Hallucination, ELIMINATE
- Compute weighted totals on remaining variants

**Within-family tiebreaker BEFORE cross-family cost-override:**

If 2+ variants of SAME family score within 0.3 weighted total, apply within-family rules from section 5.

**N >= 3 protocol for bottom-quartile:** Identify bottom 25%. Dispatch 2 more runs each. Update tally with N=3 finding.

**Apply cross-family cost-override thresholds** per section 6 table.

**Write tally.md.** Include:

- Quality winner (highest weighted score)
- Practical winner (cost-adjusted)
- Per-dimension highlights (5-7 bullets)
- Cost-adjusted decision (1-2 sentences)
- Qualitative summary (2-3 sentences)
- Scoreboard row update (which task category, what model+effort, evidence path)
- Open questions surfaced
- Surprises

**STAGE proposals - do NOT auto-write to long-lived reference files.** Output paste-ready markdown for:

- Scoreboard row update
- Methodology Index row update
- Model-task-fit map row update (if applicable)
- Any cross-domain knowledge base entry

Origin chat reviews + approves + dispatches Builders to apply.

**Rationale:** auto-update risk asymmetry. A bad tally that auto-corrupts the routing map silently affects every future tier choice. One paste of approval = one minute. Corruption recovery = hours.

### Phase 4 - Return prompt for origin chat

Output a copy-pastable markdown block:

```
PASTE THIS BACK INTO YOUR ORIGIN CHAT:

============== BEGIN RETURN PROMPT ==============

# Eval {slug} - results back from delegated session

## Headline
- Quality winner: {model+effort} (weighted total {X.X}/5.0)
- Practical winner: {model+effort} ({cost-override rule fired OR "same as quality"})

## Per-dimension highlights
- {5-7 bullets}

## Cost-adjusted decision
{1-2 sentences}

## Qualitative summary
{2-3 sentences}

## Model-task-fit map update
{which row updated, recommended model+effort + evidence path}

## Open questions surfaced
{0-3}

## Surprises
{1-2}

## Full tally
`prompt-evals/{YYYY-MM-DD-slug}/tally.md`

## Staged proposals (awaiting origin-chat approval)

### Proposed Scoreboard row
{paste-ready markdown}

### Proposed methodology Index row
{paste-ready markdown}

### Proposed model-task-fit map update (if applicable)
{specify (domain, task) + model+effort + evidence; OR "Not applicable - eval did not resolve a map row"}

### Approval needed
Origin chat: review tally + above proposals + reply "approve" / "reject" / "modify {field}" per proposal. Builder dispatches the writes after approval.

============== END RETURN PROMPT ==============
```

After outputting return prompt: "Eval {slug} complete. Return prompt above. Copy + paste back into your origin chat."

---

## 11. For users WITH Claude Code agents (full path)

If you have Claude Code running with agent infrastructure (Task tool, slash commands, hooks), you can deploy the framework directly and run evals tonight.

### Setup steps

1. **Clone the repo:**

   ```bash
   git clone https://github.com/DamianBuilds-ai/model-gauntlet.git
   cd model-gauntlet
   ```

2. **Copy the slash command to your Claude Code commands folder:**

   ```bash
   cp commands/eval-pit.md ~/.claude/commands/
   ```

3. **Copy the methodology + blueprints to your project root:**

   ```bash
   cp METHOD.md /path/to/your/project/
   cp BLUEPRINTS.md /path/to/your/project/
   ```

4. **Create the `prompt-evals/` folder in your project:**

   ```bash
   mkdir -p /path/to/your/project/prompt-evals
   ```

5. **(Optional) Add `.bak-archive/` to your `.gitignore`:**

   ```
   prompt-evals/*/.bak-archive/
   ```

### Running your first eval

In any Claude Code session, type:

```
/eval-pit
```

Claude Code will prompt you for:

- **eval_slug** (required) - short kebab-case identifier (e.g., "treasury-jd-parse")
- **task_category** (required) - one of the highest-eval-value categories
- **prompt_under_test** (required) - the verbatim prompt to send to all variants
- **variants** (optional, defaults to the 9-variant model-only pool - Haiku x3, Sonnet x3, Opus x3) - override with reduced N for targeted question
- **data_source** (optional) - where variants read input from
- **rerun_strategy** (optional) - clone old variants to `.bak-archive/` and rerun fresh? Default yes.

The eval runs autonomously across roughly 4-6 turns. All dispatches happen at depth 1 from the MAIN orchestrator session (sub-agents cannot spawn sub-agents). Total expected dispatches:

- 3-4 Stage 1 parallel reads (optional but recommended), from the main session
- 9 variant agents (parallel background, depth 1, from the main session)
- 1 Architect Pass 1 (sealed scoring, Opus, from the main session)
- 1 Architect Pass 2/3 (reveal + cost-adjust + tally, Opus, from the main session)
- 1 Builder applying methodology Scoreboard + Index updates after approval
- 1 optional Distiller compressing variant outputs for chat hygiene

= ~11 core dispatches plus ~3-6 stage/builder/distiller dispatches.

### Best practice: run in a fresh session

Open a new session, type `/eval-pit`. The eval runs autonomously and outputs a paste-back return prompt for your origin chat. Context isolation = no design-session bias on variant scoring.

### What the slash command actually does

It executes the four phases in section 10 automatically, ALL dispatched at depth 1 from the main orchestrator session. Phase 0 validates corpus. Phase 1 dispatches the 9 variants in parallel from the main session. Phase 2 fires Architect Pass 1 (sealed, Opus). Phase 3 fires Architect Pass 2/3 (reveal + cost-adjust + tally, Opus). Phase 4 outputs paste-ready return prompt. If a context that should be dispatching finds no spawn tool, it HALTS rather than self-simulating (see the halt guard at each Phase 1/2/3 dispatch site).

### Blueprint form (alternative invocation)

Type `eval-N-pit on {topic}` in any session. Same flow as `/eval-pit`, conversational rather than slash-prefixed. See `BLUEPRINTS.md` for catalog of other named formations (`recon-3`, `spray-5`, `lock`, etc.).

---

## 12. For users WITHOUT Claude Code agents (lite path)

> **HARD CAVEAT - this mode is for HUMANS ONLY, never for an agent.** The lite path
> below is a slower fallback for a PERSON deliberately driving Claude.ai by hand,
> one chat at a time, with no agent infrastructure. An AGENT executing the method
> (a `/eval-pit` or `/eval-run` run) must NEVER fall back to this single-context
> mode and must NEVER simulate, role-play, or generate the variant outputs in its
> own context. If an agent finds it cannot dispatch the variant sub-agents (for
> example, it is itself a sub-agent and has no spawn tool), the correct action is
> to HALT and report - not to "do it inline" as a lite-path imitation. A halted run
> is correct; a self-simulated run is invalid data. The single-context path is a
> human convenience, NOT a license for an agent to fake the fan-out.

If you have only Claude.ai (the chat UI), no agent infrastructure, you (a human) can
still apply the framework by hand. You won't get true variant pitting (one chat =
one model at a time), but you can use the method for:

### A. External critique of existing AI outputs

Paste the rubric into Claude. Paste an AI-produced artifact. Ask:

```
Here is an AI-produced artifact. Score it against this rubric, dimension by dimension. Apply the hard-fail criteria. Tell me what model + effort produced it (if you can guess), and what would have been a better routing choice.
```

You get a single-LLM external review. Useful for spot-checking individual outputs against a standard.

### B. Manual variant comparison (slow but works)

Run the same prompt across 2-3 different model + effort variants in separate Claude.ai chats. Capture outputs to files. Open a fresh chat, paste rubric, paste all variants WITHOUT labels, ask Claude to score sealed.

This is the spirit of the method without the parallel infrastructure. Slower but gives you real comparable data.

### C. Single-shot routing decisions

Paste the methodology spec into your context. Describe your task class. Ask Claude:

```
Given the patterns from N=10 evals in EVIDENCE.md, what model + effort do you recommend for this task class? What's your confidence and what would change your mind?
```

You get an informed recommendation grounded in the published evidence, even without running your own eval.

### D. Corpus generation for future evals

Paste the methodology into Claude. Ask:

```
Generate 2-3 corpus files I could use to run an eval on {task category}. Each corpus should test a different difficulty level.
```

You get ready-made corpora to feed back into the framework when you have agent infrastructure.

### E. Methodology critique

Paste the spec. Ask:

```
What gaps do you see in this rubric? Are the bias controls sufficient? Are the hard-fail criteria too loose or too strict? What would you change?
```

You get external critique of the framework itself. The framework is opinionated, not perfect.

---

## Appendix A - Version history

- **v1.0** (2026-05-19 AM): Initial spec, 8-dim rubric, 6-variant pool. 10-agent fleet + Architect-on-Max tally locked the design.
- **v1.1** (2026-05-19 mid): 16 Q-locks, scoreboard added, file-safety (clone-before-write) rules, sub-agents-only protocol for long-lived ref files.
- **v1.1.5** (2026-05-19 PM): Researcher + Scribe tier insertion into the 7-tier ladder. `/eval-pit` slash command shipped. First eval staged.
- **v1.2** (2026-05-19 PM): Phase 0 corpus validation, file-safety clones at Phase 0, stage-proposals default (no auto-write), effort-param limitation documented.
- **v1.3** (2026-05-19 PM): 9-dim rubric + binary Instruction-following gate + Source transparency dim + Judgment split (Helpfulness + Discipline) + within-family tiebreaker + N >= 3 bottom-quartile protocol. Source: eval #1 findings.
- **v1.4** (2026-05-19 PM): Default variant pool expanded from 6 to 12 (every model x every effort level, full spectrum). Sealed labels A through L. ~14 core dispatches per eval. Haiku effort ceiling documented (high; no xhigh/max).
- **v1.5** (2026-05-22): Pool changed from 12 (model x effort) to 9 (model-only: Haiku x3, Sonnet x3, Opus x3) - effort is a no-op at dispatch, so the dimension is dropped and the 3 reruns become variance runs (mean-of-3). Sealed labels re-lettered A through I. Dispatch topology made explicitly FLAT: variants + both Architects dispatched FROM THE MAIN SESSION at depth 1 (no intermediate runner sub-agent; sub-agents cannot spawn sub-agents). Hard halt guard added at every dispatch site. Lite-path (section 12) marked human-only with an explicit no-simulate-must-halt caveat for agents. Architect passes stay on OPUS. ~11 core dispatches per eval.

---

## Appendix B - Known limitations

**1. Effort is NOT a dispatch dimension.** Claude Code's Agent tool exposes `model: haiku|sonnet|opus` only - effort (low/medium/high/xhigh/max) cannot be pinned at dispatch. v1.5 therefore drops the effort dimension entirely: the pool is model-only (Haiku x3, Sonnet x3, Opus x3). Earlier versions carried effort labels as an aspiration, but same-model/different-effort variants produced functionally identical outputs, so the label added noise without signal. Model is the differentiator. (A HUMAN running the lite path in section 12 can still pick effort by hand in the Claude.ai UI - that is a separate, human-only path.)

**2. N=3 per model by default.** The 9-variant default runs each model x3 (the 3 reruns are variance runs; the per-model score is the mean-of-3). This damps single-run variance for every model, not just bottom-quartile ones. A reduced-N spec (fewer reruns) reverts toward N=1 and re-enables the bottom-quartile re-run protocol. Variance baseline protocol (separate from the reruns) still recommended once per major task category.

**3. Task generalization.** Each eval's findings apply to that task. Multi-file synthesis tells you nothing definitive about pattern detection or judgment call. Cross-task inference requires multiple evals across task categories.

**4. Sealed identity discipline is procedural.** Architect Pass 1 is INSTRUCTED to not open key.md. There's no technical enforcement. If Pass 1 disobeys, sealed identity breaks silently. Trust the agent + universal envelope discipline + your own audit.

**5. Cost-override thresholds are policy not math.** The 0.3 / 0.5 / 1.0 quality gap thresholds and 3x / 5x cost ratio thresholds are heuristics, not derived. Future evals may surface that different thresholds fit different task categories. Document threshold changes in your changelog.

**6. Auto-approve is NOT available.** Long-lived reference file updates require origin-chat approval. By design, no shortcut yet. The asymmetry: a bad tally that auto-corrupts your routing map silently affects every future tier choice that reads from there. One paste of approval = one minute. Corruption recovery = hours.

---

## Appendix C - Future eval ideas

Task classes still UNTESTED as of N=10 dataset publication:

- **Voice-CRITICAL drafting** (content where voice IS the deliverable, not just adjacent). Tests whether Opus medium's eval #6 voice-niche generalizes from voice-adjacent (ADR) to voice-critical (content).
- **Multi-file code-gen with cross-file consistency** (Pydantic schema + SQLAlchemy model + FastAPI route + tests, all four must match). Tests whether eval #3 single-file Sonnet win holds at multi-file scope.
- **Scout-tier confirmation eval** (same retrieval-and-compress task at minimal context budget, all 3 families x 2 effort levels). Confirms whether Haiku low's 5/6 practical-winner streak is genuinely the right Scout default OR whether Scout-tier-specific constraints change the picture.
- **Schema / architecture design** (drafting schemas / DB models / API contracts where forward-compat reasoning matters more than execution).
- **Root-cause analysis with bare traceback** (no pre-disclosure - eval #8b scheduled).
- **Cross-domain judgment with conflicting signals.**
- **Open-ended novel synthesis** (no prior art, ambiguous spec - the original "Opus's sweet spot" hypothesis target).
- **Conversation-shaped tasks** (transcripts where empathy + reasoning + voice all matter).
- **Heterogeneous-source synthesis** (mixed input types - queue files + database rows + code diffs + voice notes).

If you run any of these and want to contribute results, see [README.md](README.md) - How to contribute.
