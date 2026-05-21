# model-gauntlet

A reproducible method for empirically picking the right Claude model + effort level for each agent task class. Pits 12 model + effort variants against the same prompt with sealed identity scoring, produces evidence-backed routing decisions for Scout / Analyst / Builder / Scribe / Engineer / Researcher / Architect agent tiers.

Built in a single-day arc (2026-05-19) by Damian Yazbeck using Claude Code, with 10 completed evals on the board at v1.4 lock. The first day's evidence is included in [EVIDENCE.md](EVIDENCE.md) - not "the method works trust me," but "here is what we found in N=10 evals."

---

## Quickstart for operators (run a batch in 4 actions)

If someone handed you this repo to run evals, this is your whole job. You do not
need to understand the method internals.

1. **Clone the repo.**
   ```bash
   gh auth login            # one time
   git clone https://github.com/DamianBuilds-ai/model-gauntlet.git
   cd model-gauntlet
   ```
2. **Open Claude Code** in the `model-gauntlet` folder (`claude`).
3. **Type one command:**
   ```
   /eval-run
   ```
   On the FIRST run only, it asks once for a Telegram bot token + chat id (press
   ENTER to skip = git-only mode). It never asks again. Then it runs the next batch
   of evals on its own and ships each result as it finishes. Leave it running.
4. **Send the branch name.** When it finishes it prints a line like
   `run/20260521T143000Z`. Copy that one line and send it to whoever curates the
   evals. Done.

If a run is interrupted, just type `/eval-run` again - it resumes safely and never
double-sends. Full operator guide: [docs/starting-prompt.md](docs/starting-prompt.md).

The rest of this README explains what the framework is and how the method works -
useful if you curate the eval queue, not required if you just run batches.

---

## What this is

Three things in one method:

- **A 12-variant pool** (Haiku low/medium/high + Sonnet low/medium/high/max + Opus low/medium/high/xhigh/max) so every model x every effort gets pitted on the same prompt.
- **A 9-dimension scoring rubric** plus a binary instruction-following gate plus three mandatory bias controls (sealed identity, dim-by-dim scoring, length disclosure).
- **A four-phase execution flow** (pre-flight, parallel variant dispatch, Architect Pass 1 sealed scoring, Architect Pass 2/3 reveal + cost-adjust + tally) that produces a paste-ready decision block.

Output of any run is a `tally.md` per eval folder with weighted scores, a Scoreboard row per task category, and a recommendation that either confirms or refutes the model assigned to that task class in your agent system.

---

## Why it exists

Most teams making decisions about which Claude model to use for which task fall into one of two failure modes:

**Failure mode A - "Opus for everything."** Pay 15-20x more than needed for tasks that Haiku low can solve perfectly. Routing-by-vibes biased toward "smart equals expensive."

**Failure mode B - "Haiku for everything."** Save money but ship hallucinations on judgment-heavy work. Routing-by-vibes biased toward "cheap is fine until it isn't."

Both modes share a deeper problem: **opinion as evidence.** "I think Opus is better for this." "I've heard Haiku struggles here." No measurement, no bias controls, no comparable scoring across runs.

This method flips it from opinion to empirical signal. You define a task. You pit every model + effort variant against it. You score sealed (model identity hidden). You compute weighted totals + apply cost-override thresholds. You get a winner per quality and a winner per practical (cost-adjusted) call.

Same posture as A/B testing for product features. The difference: the framework standardizes the structure so results compose across evals and across teams.

---

## The 12-variant pool

| # | Model | Effort | Pool position |
|---|-------|--------|---------------|
| 1 | Haiku 4.5 | low | A |
| 2 | Haiku 4.5 | medium | B |
| 3 | Haiku 4.5 | high | C |
| 4 | Sonnet 4.6 | low | D |
| 5 | Sonnet 4.6 | medium | E |
| 6 | Sonnet 4.6 | high | F |
| 7 | Sonnet 4.6 | max | G |
| 8 | Opus 4.7 | low | H |
| 9 | Opus 4.7 | medium | I |
| 10 | Opus 4.7 | high | J |
| 11 | Opus 4.7 | xhigh | K (unique to Opus 4.7) |
| 12 | Opus 4.7 | max | L |

Labels A through L are **randomly assigned per eval** (sealed in `variants/key.md`, NOT opened until Pass 2 of scoring). Reduced N (3-6 variants) is allowed when targeting a specific question (e.g., "is Sonnet high enough or do I need Opus?"). v1.4 default is the full spectrum for no-gaps comparison.

---

## The four phases

| Phase | What happens |
|-------|--------------|
| **Phase 0** | Pre-flight validation. Confirm data-source paths exist. Clone long-lived reference files to `.bak-archive/`. Validate `corpus_intent` vs `corpus_delivered`. |
| **Phase 1** | Stage eval folder + dispatch all 12 variant agents in parallel (background). Each writes to `variants/{LABEL}.md` with sealed identity. |
| **Phase 2** | Architect Pass 1 - sealed scoring across 9 dimensions, dimension-by-dimension, plus binary instruction-following gate. Length disclosure mandatory. |
| **Phase 3** | Architect Pass 2/3 - open `key.md`, compute weighted totals, apply within-family tiebreaker, apply N >= 3 protocol for bottom-quartile, apply cost-override thresholds, write tally. |
| **Phase 4** | Output paste-ready return prompt for origin chat with Headline + per-dimension highlights + cost-adjusted decision + staged proposals for long-lived reference file updates. |

Full method spec: [METHOD.md](METHOD.md). Cross-eval findings from the first 10 evals: [EVIDENCE.md](EVIDENCE.md). Named formations (codenames Damian or any user can invoke conversationally): [BLUEPRINTS.md](BLUEPRINTS.md). Slash command spec for Claude Code: [commands/eval-pit.md](commands/eval-pit.md). Paste-and-go bootstrap prompt for newcomers: [docs/starting-prompt.md](docs/starting-prompt.md).

---

## Quick start

If you have Claude Code with agent infrastructure (Task tool, slash commands), you can deploy and run evals tonight.

```bash
# 1. Clone the repo
git clone https://github.com/DamianBuilds-ai/model-gauntlet.git
cd model-gauntlet

# 2. Copy the slash command to your Claude Code commands folder
cp commands/eval-pit.md ~/.claude/commands/

# 3. Copy the methodology + blueprints to your project root
cp METHOD.md /path/to/your/project/
cp BLUEPRINTS.md /path/to/your/project/

# 4. Create the prompt-evals/ folder
mkdir -p /path/to/your/project/prompt-evals

# 5. Add .bak-archive/ to your .gitignore
echo "prompt-evals/*/.bak-archive/" >> /path/to/your/project/.gitignore
```

In any Claude Code session, type:

```
/eval-pit
```

The eval runs autonomously across roughly 4-6 turns. You'll get a paste-ready return prompt to drop back into your origin chat with the headline winner, per-dimension highlights, cost-adjusted decision, and staged proposals for updating your routing map.

If you don't have Claude Code, see the **lite path** in [METHOD.md section 7](METHOD.md) - external critique, manual variant comparison, single-shot routing decisions, corpus generation, and methodology critique are all possible from a single Claude.ai chat.

---

## Headline findings from N=10 evals

Confirmed at high confidence across the first day's dataset:

- **Practical winner is Haiku 4.5 in 7/10 evals, Sonnet 4.6 in 2/10, Opus 4.7 in 0/10.** Task type tracks the routing floor before task difficulty does.
- **Opus 4.7 xhigh effort: 0-for-10 practical wins.** Effort tax (verbosity, over-elaboration) without quality buy. Retire from default routing.
- **Within-family inversion for Haiku 4.5: low > high on bounded tasks.** Three distinct failure modes for Haiku high.
- **Sonnet 4.6 structural dominance.** Wins layout / parallelism / shape tasks (eval #12 ASCII diagram authoring: top 3 spots all Sonnet).
- **Haiku discipline for verbatim retrieval CONFIRMED.** Eval #11 five-way tie at 5.0/5.0 between Haiku high, Sonnet max, Opus low/medium/xhigh; Haiku high wins practical via 15x cost-override.

Full evidence dossier: [EVIDENCE.md](EVIDENCE.md).

---

## Repository structure

```
model-gauntlet/
|-- README.md                    # This file
|-- STAN_STATE.md                # Framework memory trunk - read at every run start
|-- METHOD.md                    # Methodology spec (the load-bearing doc)
|-- EVIDENCE.md                  # N=10 cross-eval findings
|-- BLUEPRINTS.md                # Codename catalog (eval-N-pit is the conversational form)
|-- LICENSE                      # MIT
|-- .gitignore
|-- commands/
|   |-- eval-run.md              # Batch orchestrator - the ONE command operators type
|   `-- eval-pit.md              # Single-eval four-phase runner (wrapped as a sub-agent)
|-- specs/                       # One file per eval to run (curated; operators do not edit)
|   `-- .gitkeep                 # real specs seeded by the queue dispatch
|-- corpus/                      # Sanitized public inputs the specs point at
|   `-- .gitkeep
|-- rubric/
|   `-- rubric.md                # Frozen scoring contract (9 dims + binary gate + cost-override)
|-- outbox/                      # Transient per-eval working dir (wiped between evals)
|   `-- .gitkeep                 # only .gitkeep is tracked; outbox/* is gitignored
|-- config/                      # Gitignored return-channel.env lives here (Telegram token)
|   `-- .gitkeep
|-- scripts/
|   |-- send-eval.sh             # Per-eval incremental send (commit specific files + push + notify)
|   |-- preflight.sh             # Corpus-path check + private-content guard
|   |-- setup-return-channel.sh  # One-time Telegram setup (or skip to git-only)
|   `-- send-and-clean.sh        # Recovery flush (fallback only)
`-- docs/
    `-- starting-prompt.md       # Paste-and-go operator guide
```

---

## License + attribution

MIT License. See [LICENSE](LICENSE).

**Origin:** Framework developed 2026-05-19 in a single-day arc by Damian Yazbeck via Claude Code (Anthropic). v1.0 through v1.4 all locked the same day across multiple Damian Q&A loops with the Architect tier. N=10 evals completed same day, evidence dataset published with method.

**Models referenced:** Anthropic Claude Haiku 4.5, Sonnet 4.6, Opus 4.7. Method generalizes to any provider but evidence is Anthropic-specific.

**No warranty.** The cost-override thresholds (3x at 0.3-0.5 gap, 5x at 0.5-1.0 gap) are policy heuristics from initial calibration. Adjust for your team's economics. The 9-dimension rubric weights are also initial calibration; iterate.

---

## How to contribute

Open issues for:

- Bias control gaps (something the method misses)
- Rubric dimension overlap (two dims that measure the same thing)
- Threshold suggestions (you've run enough evals to suggest different cost-override numbers)
- Task category additions (a new task class not yet covered)
- Methodology bugs

PRs welcome for:

- New example evals as `EXAMPLE-{slug}/` at the repo root (full 6-file structure, sealed-identity-discipline followed; see the shipped `EXAMPLE-multi-file-synthesis/`)
- Cross-LLM extensions (running the method against GPT-5, Gemini 4, Llama, etc.)
- Tooling that automates Phase 0 corpus validation
- Tooling that compares evals across teams (a meta-Scoreboard)

If you adapt the method to non-Anthropic LLMs and run a corpus through, contribute the results. We'll add a "Cross-LLM evidence" section once 3+ providers are represented.

If you read the N=10 evidence dataset and come to different conclusions than the published patterns, open a discussion. The framework is opinionated; opinions should be defensible.
