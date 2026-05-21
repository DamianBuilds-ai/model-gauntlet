# /eval-pit - Prompt Engineering Evaluation Run (v1.4)

A slash command for Claude Code (or any compatible agent harness) that pits 12 model + effort variants (default; full effort spectrum, no gaps) against each other on the same prompt with sealed identity scoring + Architect-on-Max tally + cost-adjusted recommendation.

**v1.4 changes:**

- Default variant pool expanded from 3-6 to 12 (every model x every effort level, full spectrum, no gaps)
- Phase 1 dispatch: 12 parallel variant agents (was 6)
- Sealed labels extended A through L (was A through F)
- Estimated dispatch count: ~14 per eval (12 variants + 2 Architects), up from 8
- Time-budget note: fewer evals fit per delegated session (likely 2 instead of 3)
- Reduced N (3-6 targeting specific question) still allowed per eval-specific spec; v1.4 default is the FULL spectrum for no-gaps comparison

**v1.4 default variant pool (12 - full effort spectrum):**

| # | Model | Effort | Notes |
|---|-------|--------|-------|
| 1 | Haiku 4.5 | low | |
| 2 | Haiku 4.5 | medium | |
| 3 | Haiku 4.5 | high | No xhigh/max available per Anthropic spec |
| 4 | Sonnet 4.6 | low | |
| 5 | Sonnet 4.6 | medium | |
| 6 | Sonnet 4.6 | high | |
| 7 | Sonnet 4.6 | max | |
| 8 | Opus 4.7 | low | |
| 9 | Opus 4.7 | medium | |
| 10 | Opus 4.7 | high | |
| 11 | Opus 4.7 | xhigh | Unique to Opus 4.7 |
| 12 | Opus 4.7 | max | |

Reduced N (e.g., 3-6 variants targeting specific question) still allowed per eval-specific spec. v1.4 default is the FULL spectrum for no-gaps comparison.

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
- **variants** (optional, defaults to 12-variant full spectrum per v1.4 table above): override with a reduced N (e.g., "Haiku low + Haiku high + Sonnet low + Sonnet high + Opus medium + Opus xhigh") when targeting a specific question
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

1. Create `{PROJECT_ROOT}/prompt-evals/{YYYY-MM-DD-eval_slug}/` folder with standard 6 files (`README`, `prompt`, `rubric`, `scores`, `tally`, `variants/key.md`). Variants subdir will host A through L (12 files) by default.

**1c) Stamp corpus_intent + corpus_delivered + corpus_match in eval folder files.**

When creating `prompt-evals/{eval-slug}/` files, frontmatter MUST include:

- `corpus_intent: <N or description>` - what the eval was designed for
- `corpus_delivered: TBD` - filled by variant agents when they actually read the corpus (each variant updates if asked to report)
- `corpus_match: TBD` - auto-flagged in tally based on intent vs delivered

If post-eval `corpus_match: false`, the tally automatically gets `status: corpus-mismatch` (not just `status: complete`).

2. Generate randomized variant-to-label mapping (A through L, 12 labels by default; A through F if reduced N=6 spec; etc.), seal in `variants/key.md`
3. Write the per-variant prompt template + assign output paths
4. Dispatch all 12 variant agents (default) in ONE parallel batch (background). Reduced-N override spawns fewer.
5. Each agent writes to `variants/{LABEL}.md`, sealed identity, no model self-reference, no cost estimates
6. File-safety: pre-write clone to `.bak-archive/{label}-{timestamp}.md` if rerunning existing

### Phase 2 - Architect Pass 1 sealed scoring

After all variants land:

- Dispatch ONE Architect (Opus 4.7 high effort - "on max" tier)
- Read `variants/{A through L}.md` WITHOUT opening `key.md` (12 variants default; A through F if reduced N=6)
- Score 9 dimensions dimension-by-dimension across ALL variants (then apply Instruction-following PASS/FAIL gate)
- Write to `scores.md` per template with qualitative observation per variant (mandatory, written LAST)
- Length disclosure: word counts captured BEFORE scoring

### Phase 3 - Architect Pass 2 reveal + Pass 3 cost-adjust

After Pass 1:

- Dispatch SECOND Architect (Opus 4.7 high)
- Read `scores.md` + open `key.md`
- Apply v1.3 rubric: 9 scored dimensions + Instruction-following binary PASS/FAIL gate
  - If any variant fails Instruction-following gate, ELIMINATE from contention (no weighted score)
  - If any variant scores 1 on Correctness, Hallucination, or marked FAIL on Instruction-following = hard-fail eliminated
- Compute weighted totals on remaining variants: `sum(score * weight) / sum(weights scored)`

**Within-family tiebreaker BEFORE cross-family cost-override:**

- If 2+ variants of SAME MODEL FAMILY (e.g., Haiku low + Haiku high) score within 0.3 weighted total:
  1. Cheaper effort wins (within same model)
  2. If tied AND same effort: shorter output wins (verbosity penalty)
  3. If still tied: random with note

**N >= 3 protocol for bottom-quartile:**

- Identify bottom-quartile variants (lowest 25% by weighted total or eliminated by hard-fail)
- Dispatch 2 MORE runs of each bottom-quartile variant (same model + effort, fresh corpus context)
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

If you're on metered API access, plan for ~14 core dispatches per eval. Reduced-N (3-6 variants) cuts that to ~5-8. Use reduced-N when targeting a specific question; reserve full-spectrum runs for new task categories or major model releases.

## Total expected agent dispatches per eval

- 3-4 Stage 1 parallel reads (optional but recommended)
- 12 variant agents (parallel background, v1.4 default; reduced N=3-6 still allowed per eval-specific spec)
- 1 Architect Pass 1
- 1 Architect Pass 2/3
- 1 Builder updating methodology Scoreboard + Index
- 1 optional Distiller compressing variant outputs for chat hygiene before Phase 4

= ~14 core dispatches (12 variants + 2 Architects) plus ~3-6 stage / builder / distiller dispatches per eval

**Time-budget note (v1.4):** with 12 variants instead of 6, the dispatch fan-out is wider. Expect fewer evals to fit per delegated session (likely 2 instead of 3). Plan delegated-session scope accordingly.

---

## Known limitations (v1.4)

**1. Effort parameter NOT enforced.** Claude Code's Agent tool exposes `model: haiku|sonnet|opus` only. Effort levels (low/medium/high/xhigh/max) are RECORDED in variant labels for analysis but NOT enforced at dispatch. Variant pairs at same model + different effort labels may produce functionally identical outputs. Document the effort label as an aspiration; treat results as if only model was the differentiator.

**1a. Haiku effort ceiling (v1.4).** Haiku 4.5 tops out at `high` per Anthropic spec - no `xhigh` or `max` available. The 12-variant default pool reflects this (Haiku slots = low/medium/high only). Sonnet 4.6 goes through `max`. Opus 4.7 is the only model with `xhigh` available, plus `max`.

**2. N=1 per variant baseline.** Each eval runs each variant once by default. v1.3 adds N >= 3 protocol for bottom-quartile variants (re-run 2x to confirm failure). Top variants still N=1 unless you manually re-run. Variance baseline protocol (separate from N >= 3) recommended once per major task category to establish noise floor.

**3. Task generalization.** Each eval's findings apply to that task. Multi-file synthesis tells you nothing definitive about pattern detection or judgment call. Cross-task inference requires multiple evals across task categories.

**4. Sealed identity discipline is procedural.** Architect Pass 1 is INSTRUCTED to not open `key.md`. There's no technical enforcement. If Pass 1 disobeys, sealed identity breaks silently. Trust the agent + universal envelope discipline.

**5. Cost-override thresholds are policy not math.** The 0.3/0.5/1.0 quality gap thresholds and 3x/5x cost ratio thresholds are heuristics, not derived. Future evals may surface that different thresholds fit different task categories.

**6. Auto-approve is NOT available.** Long-lived ref file updates require origin-chat approval. By design, no shortcut yet.

**7. Filesystem sandbox is procedural, not OS-enforced.** The Stan orchestrator's "write only to outbox/ + STAN_STATE.md" contract (see `commands/eval-run.md`) is an instruction given to every sub-agent, not an operating-system boundary - there is no container or chroot around the run. A misbehaving sub-agent could write outside its lane and nothing would stop it at the OS level. Run on a normal user account where that is acceptable. Same procedural class as limitation 4.

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
