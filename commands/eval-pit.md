# /eval-pit - Prompt Engineering Evaluation Run (v1.5)

A slash command for Claude Code (or any compatible agent harness) that pits 9 model variants (default; 3 models x 3 reruns each) against each other on the same prompt with sealed identity scoring + Architect-on-Max tally + cost-adjusted recommendation.

**v1.5 changes:**

- Default variant pool changed from 12 (model x effort) to 9 (model-only). Effort is a no-op at dispatch (Claude Code exposes `model: haiku|sonnet|opus` only), so the effort dimension is dropped entirely. The pool is now Haiku x3, Sonnet x3, Opus x3 - the 3 reruns per model are variance runs (mean-of-3).
- Sealed labels re-lettered A through I (was A through L).
- Dispatch topology is FLAT: variant sub-agents are dispatched FROM THE MAIN SESSION (depth 1), not from inside a runner sub-agent. Sub-agents cannot spawn sub-agents.
- Hard halt guard added at every dispatch site: a sub-agent that finds no spawn tool HALTS rather than self-simulating.
- Reduced N (targeting a specific question, e.g. "just Haiku vs Sonnet") still allowed per eval-specific spec; v1.5 default is the 9-variant model-only pool.

**v1.5 default variant pool (9 - model-only, 3 reruns per model):**

| # | Model | Run | Notes |
|---|-------|-----|-------|
| 1 | Haiku 4.5 | 1 | |
| 2 | Haiku 4.5 | 2 | variance run |
| 3 | Haiku 4.5 | 3 | variance run |
| 4 | Sonnet 4.6 | 1 | |
| 5 | Sonnet 4.6 | 2 | variance run |
| 6 | Sonnet 4.6 | 3 | variance run |
| 7 | Opus 4.7 | 1 | |
| 8 | Opus 4.7 | 2 | variance run |
| 9 | Opus 4.7 | 3 | variance run |

Effort (low/medium/high/xhigh/max) is NOT a dispatch dimension - the Agent tool pins `model:` only. The 3 reruns per model give a mean-of-3 to damp single-run variance. Reduced N (e.g., a 1-rerun head-to-head of two models) still allowed per eval-specific spec. v1.5 default is the 9-variant model-only pool.

**v1.3 changes (rubric):**

- Rubric updated to 9 scored dims + binary Instruction-following gate (was 8 scored dims)
- Source transparency dimension added (weight 1.0, applies all tasks)
- Judgment split into Helpfulness + Discipline (1.25 each, conditional decision tasks)
- Instruction-following converted to binary PASS/FAIL gate (was scored 2.0)
- Phase 0 extended: corpus_intent vs corpus_delivered count check
- Within-family tiebreaker hierarchy added (before cross-family cost-override)
- N >= 3 protocol for bottom-quartile variants added
- Carries forward v1.2 stage-proposals default + file-safety clones

**Consumer:** any session in any project (cross-domain command).
**Blueprint equivalent:** `eval-N-pit` codename in `BLUEPRINTS.md` (same flow, conversational invocation).

---

## When to use

- You want to know which model + effort wins for a recurring task class
- You're considering a tier change (e.g., is Sonnet med enough or do I need Opus?)
- Model release lands and you need to benchmark vs incumbent
- You're rewriting a high-volume prompt and cost matters
- You want to pit specialists (Drafter vs Scribe, Janitor vs Builder) on their cluster's tasks

## Best practice: run in a fresh session

Open a new session in your harness, type `/eval-pit`. The eval runs autonomously across roughly 4-6 turns + outputs a return-prompt for your origin chat. Context isolation = no design-session bias on variant scoring.

---

## Auto-loaded context (read these in parallel Scout calls at start)

1. `{REPO_ROOT}/METHOD.md` - methodology + 9-dim rubric + binary Instruction-following gate + bias controls + cost-override thresholds
2. `{REPO_ROOT}/BLUEPRINTS.md` - context (eval-N-pit is the blueprint form of this command)
3. Your project's agent roster / tier docs - 7-tier roster (Scout / Analyst / Builder / Scribe / Engineer / Researcher / Architect)
4. Most recent eval folder under `{PROJECT_ROOT}/prompt-evals/` - structural reference
5. Variance baseline protocol in `{REPO_ROOT}/METHOD.md` section 8 - noise-floor calibration required when launching evals on a NEW task category

---

## Args (asks if not provided in invocation)

If user invokes bare `/eval-pit`, prompt for:

- **eval_slug** (required): short kebab-case identifier - e.g., "theme-synthesis", "jd-parse", "hook-draft"
- **task_category** (required): one of the highest-eval-value categories (multi-file synthesis, pattern detection, judgment call, verbatim capture, external research + synthesize)
- **prompt_under_test** (required): the verbatim prompt to send to all variants
- **variants** (optional, defaults to 9-variant model-only pool per v1.5 table above - Haiku x3, Sonnet x3, Opus x3): override with a reduced N (e.g., "Haiku x3 + Sonnet x3" to drop Opus, or "Haiku x1 + Sonnet x1" for a quick head-to-head) when targeting a specific question
- **data_source** (optional): where variants read input from (file paths, date ranges, etc.)
- **rerun_strategy** (optional): if eval slug already exists, do you want to clone old variants to `.bak-archive/` and rerun fresh? Default yes.

---

## Execute in 4 phases

## Phase 0 - Pre-flight validation + file-safety

Before dispatching ANY variant or Architect:

**a) Validate data source paths exist.** Read the prompt.md `data_source` field. Bash `ls` or `test -e` to confirm every path exists. If any path is broken, HALT + tell user to fix prompt.md before proceeding. Do NOT proceed with broken paths.

**b) Clone long-lived ref files to eval folder `.bak-archive/`.** Before any agent dispatch that might touch them:

```bash
mkdir -p {PROJECT_ROOT}/prompt-evals/{eval-slug}/.bak-archive
timestamp=$(date -u +%Y%m%dT%H%M%S)
cp {REPO_ROOT}/METHOD.md {PROJECT_ROOT}/prompt-evals/{eval-slug}/.bak-archive/${timestamp}-METHOD.md
cp {REPO_ROOT}/BLUEPRINTS.md {PROJECT_ROOT}/prompt-evals/{eval-slug}/.bak-archive/${timestamp}-BLUEPRINTS.md
# repeat for any other long-lived reference files your project uses (model-task-fit map, agent-patterns roster, decisions log, etc.)
```

`.bak-archive/` is `.gitignored` at `prompt-evals/*/.bak-archive/` per recommended `.gitignore`.

**c) Confirm eval-slug folder structure** (if rerun: `variants/key.md` present + `scores.md` + `tally.md` skeletons + `.bak-archive/` exists).

**d) Validate corpus_intent vs corpus_delivered count.**

Read prompt.md frontmatter for `corpus_intent` (declared count). Bash count actual files matching the corpus pattern. If count mismatch:

- If actual < intent: HALT + tell user "corpus delivered fewer items than declared (X vs Y). Fix prompt.md or corpus before proceeding."
- If actual > intent: OK to proceed but log mismatch in scores.md notes
- If broken path: same as Phase 0 step (a) HALT

This mitigates a class of bug where a broken corpus path silently delivers fewer items than declared, with no pre-flight check to catch it.

Only after Phase 0 completes successfully, proceed to Phase 1.

### Phase 1 - Stage + dispatch variants

1. Create `{PROJECT_ROOT}/prompt-evals/{YYYY-MM-DD-eval_slug}/` folder with standard 6 files (`README`, `prompt`, `rubric`, `scores`, `tally`, `variants/key.md`). Variants subdir will host A through I (9 files) by default.

**1c) Stamp corpus_intent + corpus_delivered + corpus_match in eval folder files.**

When creating `prompt-evals/{eval-slug}/` files, frontmatter MUST include:

- `corpus_intent: <N or description>` - what the eval was designed for
- `corpus_delivered: TBD` - filled by variant agents when they actually read the corpus (each variant updates if asked to report)
- `corpus_match: TBD` - auto-flagged in tally based on intent vs delivered

If post-eval `corpus_match: false`, the tally automatically gets `status: corpus-mismatch` (not just `status: complete`).

2. Generate randomized variant-to-label mapping (A through I, 9 labels by default - the 3 models x 3 reruns; fewer if a reduced-N spec), seal in `variants/key.md`
3. Write the per-variant prompt template + assign output paths
4. Dispatch the 9 variants (default) in ONE parallel batch (background) FROM THE MAIN SESSION (depth 1). Each variant is pinned with `model: haiku|sonnet|opus` (model is the only dispatch lever; effort is a no-op). Reduced-N override spawns fewer.

   HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.
5. Each agent writes to `variants/{LABEL}.md`, sealed identity, no model self-reference, no cost estimates
6. File-safety: pre-write clone to `.bak-archive/{label}-{timestamp}.md` if rerunning existing

### Phase 2 - Architect Pass 1 sealed scoring

After all variants land:

- Dispatch ONE Architect FROM THE MAIN SESSION (depth 1), on OPUS (Opus 4.7 - "on max" tier). NOT from inside any runner sub-agent.
- Read `variants/{A through I}.md` WITHOUT opening `key.md` (9 variants default; fewer if a reduced-N spec)
- Score 9 dimensions dimension-by-dimension across ALL variants (then apply Instruction-following PASS/FAIL gate)
- Write to `scores.md` per template with qualitative observation per variant (mandatory, written LAST)
- Length disclosure: word counts captured BEFORE scoring

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.

### Phase 3 - Architect Pass 2 reveal + Pass 3 cost-adjust

After Pass 1:

- Dispatch SECOND Architect FROM THE MAIN SESSION (depth 1), on OPUS (Opus 4.7). NOT from inside any runner sub-agent.
- Read `scores.md` + open `key.md`

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for example, you are yourself a sub-agent), STOP immediately and report: HALT - variant dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER generate, role-play, or simulate variant outputs yourself. A halted run is correct; a self-simulated run is invalid data.
- Apply v1.3 rubric: 9 scored dimensions + Instruction-following binary PASS/FAIL gate
  - If any variant fails Instruction-following gate, ELIMINATE from contention (no weighted score)
  - If any variant scores 1 on Correctness, Hallucination, or marked FAIL on Instruction-following = hard-fail eliminated
- Compute weighted totals on remaining variants: `sum(score * weight) / sum(weights scored)`

**Within-family handling (the 3 reruns) BEFORE cross-family cost-override:**

- The 3 reruns of the same model are variance runs. Take the MEAN of the 3 weighted totals as that model's score (mean-of-3). This is the within-family resolution now that the pool is model-only (no effort dimension to tie-break).
- If 2+ DIFFERENT models score within 0.3 weighted total of each other, that is a cross-family tie - resolve it via the cost-override table below (cheaper model wins in the tie zone). If still tied: shorter output wins (verbosity penalty); if still tied, random with note.

**N >= 3 protocol for bottom-quartile:**

- The 9-variant default already runs each model x3, so the mean-of-3 IS the N=3 evidence for every model. For a REDUCED-N spec (fewer than 3 reruns of a model), if that model lands in the bottom quartile, dispatch 2 MORE runs of it to reach N=3.
- Identify bottom-quartile variants (lowest 25% by weighted total or eliminated by hard-fail)
- Dispatch the additional runs of each bottom-quartile model (same model, fresh corpus context) only if it has not already reached N=3
- If all 3 runs show same failure pattern -> confirmed model-specific weakness
- If runs vary widely -> sample variance, original score upgraded to "noisy" flag
- Update tally with N=3 finding

Then apply cross-family cost-override thresholds per methodology table.

- Write `tally.md` per template (eval-folder file, intended)

**DO NOT auto-write to long-lived reference files.** Instead, STAGE proposals in the return prompt for origin-chat approval:

- **STAGE proposed methodology Scoreboard row content** (full markdown block, paste-ready)
- **STAGE proposed methodology Index row update** (full markdown block, paste-ready)
- **STAGE proposed model-task-fit map update if applicable** (specify (domain, task) target + new model + effort + evidence path)
- **STAGE proposed cross-domain knowledge base row content if eligible per promotion gate** (full JSON or paste-ready markdown payload)

Origin chat reviews + approves + dispatches Builders to apply. No long-lived file edits without explicit user approval.

**Rationale:** auto-update risk asymmetry. A bad tally that auto-corrupts your routing map silently affects every future tier choice that reads from there. One paste of approval = one minute. Corruption recovery = hours.

**Future versions may add `--auto-approve` opt-in flag** once pattern is proven over multiple eval runs. Until then, NO auto-approve.

### Phase 4 - Return prompt for origin chat

Output a copy-pastable markdown block formatted as:

```
PASTE THIS BACK INTO YOUR ORIGIN CHAT:

============== BEGIN RETURN PROMPT ==============

# Eval {slug} - results back from delegated session

## Headline
- Quality winner: {model} (weighted total {X.X}/5.0)
- Practical winner: {model} ({cost-override rule fired OR "same as quality"})

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
`{PROJECT_ROOT}/prompt-evals/{YYYY-MM-DD-slug}/tally.md`

## What's next
{updates landed, suggested next eval}

## Staged proposals (awaiting origin-chat approval)

### Proposed Scoreboard row
{paste-ready markdown}

### Proposed methodology Index row
{paste-ready markdown}

### Proposed model-task-fit map update (if applicable)
{specify (domain, task) + model+effort + evidence; OR "Not applicable - eval did not resolve a map row"}

### Proposed knowledge base row (if eligible)
{full payload OR "Not eligible per promotion gate"}

### Approval needed
Origin chat: review tally + above proposals + reply "approve" / "reject" / "modify {field}" per proposal. Builder dispatches the writes after approval.

============== END RETURN PROMPT ==============
```

After outputting return prompt: "Eval {slug} complete. Return prompt above. Copy + paste back into your origin chat."

---

## Constraints

- Sub-agents-only writes for long-lived reference files (methodology Scoreboard + Index, BLUEPRINTS.md, model-task-fit map, agent-patterns roster, decisions log)
- Per-eval folder files may be main-session-written for one-shot work
- NO em dashes anywhere (use spaced hyphens or en-dashes)
- NO emojis
- All variant + Architect agents use universal output envelope (`schemaVersion: 1` + `tier` + `status` + `tool_budget_used`)
- File-safety: pre-write clone to `.bak-archive/` before overwriting existing variant files
- Sealed identity is non-negotiable - Pass 1 NEVER opens `key.md`
- Pit specialists (Drafter, Scribe, etc.) on their cluster's tasks when relevant - not just canonical tiers

## Cost note

If you're on a flat-rate Claude Code subscription (e.g., Max tier), per-call cost is irrelevant during eval design. Quality + signal matters. Full variant slate + Architect passes is the budget; no shrinkage.

If you're on metered API access, plan for ~11 core dispatches per eval. Reduced-N (e.g., 2 models x 1 rerun) cuts that to ~4-6. Use reduced-N when targeting a specific question; reserve the full 9-variant pool for new task categories or major model releases.

## Total expected agent dispatches per eval

- 3-4 Stage 1 parallel reads (optional but recommended), from the main session
- 9 variant agents (parallel background, depth 1, dispatched from the MAIN SESSION; v1.5 default = 3 models x 3 reruns; reduced N still allowed per eval-specific spec)
- 1 Architect Pass 1 (Opus), dispatched from the main session
- 1 Architect Pass 2/3 (Opus), dispatched from the main session
- 1 Builder updating methodology Scoreboard + Index
- 1 optional Distiller compressing variant outputs for chat hygiene before Phase 4

= ~11 core dispatches (9 variants + 2 Architects) plus ~3-6 stage / builder / distiller dispatches per eval

**Topology note (v1.5):** every dispatch above happens at depth 1 from the main orchestrator session. Sub-agents cannot spawn sub-agents, so NO dispatch is nested inside a runner sub-agent. If a context that should be dispatching finds no spawn tool, it HALTS (see the halt guard at each Phase 1/2/3 dispatch site) - it never self-simulates the variants.

---

## Known limitations (v1.5)

**1. Effort is NOT a dispatch dimension.** Claude Code's Agent tool exposes `model: haiku|sonnet|opus` only - effort (low/medium/high/xhigh/max) cannot be pinned at dispatch. v1.5 therefore drops the effort dimension entirely: the pool is model-only (Haiku x3, Sonnet x3, Opus x3). Earlier versions carried effort labels as an aspiration, but same-model/different-effort variants produced functionally identical outputs, so the label added noise without signal. Model is the differentiator.

**2. N=3 per model by default.** The 9-variant default runs each model x3 (the 3 reruns are variance runs; the per-model score is the mean-of-3). This damps single-run variance for every model, not just bottom-quartile ones. A reduced-N spec (fewer reruns) reverts toward N=1 and re-enables the bottom-quartile re-run protocol. Variance baseline protocol (separate from the reruns) still recommended once per major task category to establish the noise floor.

**3. Task generalization.** Each eval's findings apply to that task. Multi-file synthesis tells you nothing definitive about pattern detection or judgment call. Cross-task inference requires multiple evals across task categories.

**4. Sealed identity discipline is procedural.** Architect Pass 1 is INSTRUCTED to not open `key.md`. There's no technical enforcement. If Pass 1 disobeys, sealed identity breaks silently. Trust the agent + universal envelope discipline.

**5. Cost-override thresholds are policy not math.** The 0.3/0.5/1.0 quality gap thresholds and 3x/5x cost ratio thresholds are heuristics, not derived. Future evals may surface that different thresholds fit different task categories.

**6. Auto-approve is NOT available.** Long-lived ref file updates require origin-chat approval. By design, no shortcut yet.

**7. Filesystem sandbox is procedural, not OS-enforced.** The Stan orchestrator's "write only to outbox/ + GAUNTLET_QUEUE.md" contract (see `commands/eval-run.md`) is an instruction given to every sub-agent, not an operating-system boundary - there is no container or chroot around the run. A misbehaving sub-agent could write outside its lane and nothing would stop it at the OS level. Run on a normal user account where that is acceptable. Same procedural class as limitation 4.

---

## Related

- `METHOD.md` - methodology spec
- `BLUEPRINTS.md` - blueprint catalog (`eval-N-pit` is the conversational form)
- `EVIDENCE.md` - N=10 cross-eval findings

---

## Version history

- **v1.0** (2026-05-19 AM): framework spec locked
- **v1.1** (2026-05-19 mid): Q-locks, scoreboard, file-safety, sub-agents-only
- **v1.1.5** (2026-05-19 PM): Researcher + Scribe tier insertion, `/eval-pit` slash command, first eval staged
- **v1.2** (2026-05-19 PM): Stage proposals default + file-safety clones at Phase 0 + effort-param limitation documented + data-source validation + NO auto-approve
- **v1.3** (2026-05-19 PM): 9-dim rubric + binary Instruction-following gate + Source transparency + Judgment split (Helpfulness / Discipline) + corpus integrity (Phase 0 step d + frontmatter) + within-family tiebreaker + N >= 3 bottom-quartile protocol. Source: eval #1 findings.
- **v1.4** (2026-05-19 PM): Default variant pool expanded from 3-6 to 12 (every model x every effort level, full spectrum, no gaps). Sealed labels A through L. Estimated 14 core dispatches per eval (12 variants + 2 Architects). Haiku effort ceiling documented (high; no xhigh/max). Time-budget note: ~2 evals per delegated session (down from ~3).
- **v1.5** (2026-05-22): Pool changed from 12 (model x effort) to 9 (model-only: Haiku x3, Sonnet x3, Opus x3) - effort is a no-op at dispatch, so the dimension is dropped and the 3 reruns become variance runs (mean-of-3). Sealed labels re-lettered A through I. Dispatch topology made explicitly FLAT: variants + both Architects dispatched FROM THE MAIN SESSION at depth 1 (no intermediate runner sub-agent). Hard halt guard added at every dispatch site (variants + both Architects) - a sub-agent that finds no spawn tool HALTS rather than self-simulating. Consolidator/Architect passes stay on OPUS. ~11 core dispatches per eval (9 variants + 2 Architects).
