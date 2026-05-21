# /eval-run - Batch Eval Orchestrator (the one command Stan types)

The single command for running prompt-evals with near-zero friction. Stan types
`/eval-run` and the orchestrator reads the framework's memory, runs the next batch
of evals one at a time, ships each eval's result the moment it finishes, updates
the framework's memory, and prints a branch name for Stan to paste back. No chats
to open or close, no per-eval lifecycle, no internals to understand.

This command WRAPS the single-eval `/eval-pit` four-phase flow: each eval in the
batch is run by ONE eval sub-agent that executes `/eval-pit` internally in its own
context window (the master-bot-calling-a-tool pattern). The orchestrator never
re-ingests sub-agent context - it only confirms each result file landed, ships it,
and moves on.

**Consumer:** Stan (or any non-technical operator) on a clone of `model-gauntlet`.
**Wraps:** `commands/eval-pit.md` (the single-eval runner), invoked as a sub-agent.

---

## Sandbox contract (read first - this is a hard requirement)

The orchestrator AND every sub-agent it spawns write ONLY to two locations:

- `outbox/` (transient per-eval working files - tally + scores)
- `STAN_STATE.md` (the framework memory trunk)

Nothing else is read or written outside this repo. No access to Stan's other files,
no permanent files, no home directory, no system paths. Every eval sub-agent is
spawned with an explicit single-write-path constraint (`outbox/NN-slug.tally.md`
and `outbox/NN-slug.scores.md` ONLY). Any write attempt outside `outbox/` is a
scope-exceeded signal, not an action. Variant scratch files and the sealed key live
inside each sub-agent's own scratch and are NEVER copied to outbox.

Honest scope of this guarantee: it is enforced by INSTRUCTION (every sub-agent is
told its single write path), NOT by an operating-system boundary. There is no
container or chroot around the run. A misbehaving sub-agent could in principle
write elsewhere and nothing would stop it at the OS level. Run this on a normal
user account on your own machine, where that residual risk is acceptable. It is
the same procedural class as the sealed-identity discipline.

Note on modes: this orchestrator is the Stan run-mode (outbox-only). The curator
workflow in `commands/eval-pit.md` is a different mode - it authors full 6-file
eval folders under `prompt-evals/{slug}/`. Do not conflate the two write scopes.

At the END of every run, ALL child processes are reaped (see step 7). No lingering
grader or shell processes are left running on Stan's machine.

---

## The run loop

### 1. Read the framework memory

Read `STAN_STATE.md`. Learn: which evals are `done`, which are `queued`, what the
Next batch is, and the Run history. This is how the framework knows what it has
already shipped and what comes next.

### 2. Return-channel check (one-time setup, first run only)

Check whether `config/return-channel.env` exists.

- **If it exists:** read nothing further here - the channel is configured. Proceed.
- **If it is MISSING:** this is the first run. Run the one-time setup:
  ```
  !bash scripts/setup-return-channel.sh
  ```
  It asks ONLY for a Telegram bot token + chat id, and offers "press ENTER to skip
  = git-only mode". It writes the gitignored `config/return-channel.env` (chmod 600)
  and NEVER asks again. Whether Stan supplies Telegram or skips, the run proceeds -
  git push is always the source of truth; Telegram is a best-effort heads-up.

Do not ask any other setup questions, ever. After the first run this step is a
silent no-op.

### 3. Preflight

Run the preflight gate:
```
!bash scripts/preflight.sh <corpus-path-1> <corpus-path-2> ...
```
Pass the corpus path of every eval in the batch (from STAN_STATE / the spec files).
Preflight does two things: (a) validates every corpus path exists on disk, and
(b) runs the private-content guard over `outbox/`, `specs/`, `corpus/`. If preflight
exits non-zero, HALT and relay its plain-English message to Stan verbatim (e.g.
"corpus path corpus/foo.md does not exist - fix the spec before running"). Do not
dispatch any eval until preflight passes.

### 4. Determine the batch

From STAN_STATE, take the Next batch slugs (or, if Next batch is empty, the first
`queued` rows in the Eval queue). The batch is the next **>= 5** queued evals
(fewer only if fewer than 5 remain queued).

Before building the batch, check `outbox/`: if it is non-empty at the start of a
run, WARN Stan in plain English - "the previous run did not finish shipping (files
left in outbox/). Re-run to resume, or clear outbox/ first." A resumed run skips
evals already marked `done` in STAN_STATE (step 8), so resuming is safe.

### 5. Create the run branch (ONCE per run)

Create a single run branch for the whole batch:
```
!git checkout -b "run/$(date -u +%Y%m%dT%H%M%SZ)"
```
Capture the branch name (e.g. `run/20260521T143000Z`). Every eval in this batch
accumulates on this ONE branch. The orchestrator and scripts push ONLY to this
`run/<timestamp>` branch and NEVER to master. (Master is protected; Stan cannot
touch it. This is intentional.)

### 6. For each eval in the batch, SEQUENTIALLY

Process the batch one eval at a time. Do NOT parallelise - sequential keeps peak
context low, makes an interrupted run leave a clean partial state, and ships each
result the instant it is ready. For each eval:

**a. Dispatch ONE eval sub-agent.** It runs the `/eval-pit` four-phase flow
internally: stage the 12-variant pool (or the spec's reduced-N override), Pass 1
sealed scoring against `rubric/rubric.md`, Pass 2 reveal + cost-adjust, write the
tally. Use the spawn-prompt template below. The sub-agent is HARD-CONSTRAINED to
write ONLY `outbox/NN-slug.tally.md` and `outbox/NN-slug.scores.md`.

**b. Ship that eval immediately.** Once the tally has landed in outbox:
```
!bash scripts/send-eval.sh <NN-slug> <run-branch>
```
This commits ONLY that eval's two files to the run branch, pushes (retry-safe), and
Telegram-notifies if configured. The run branch accumulates this eval on top of any
already shipped in the batch.

**c. Update STAN_STATE.md.** Mark the slug `done` in the Eval queue, add a row to
Completed (slug | run branch | date sent | quality winner | practical winner -
pulled from the tally headline). This is the orchestrator's job; do it now, not at
the end. (See "Editing STAN_STATE" below.)

**d. Wipe that eval's transient files from outbox.** Delete `outbox/NN-slug.tally.md`
and `outbox/NN-slug.scores.md` locally:
```
!rm -f outbox/<NN-slug>.tally.md outbox/<NN-slug>.scores.md
```
The just-pushed copies remain on the remote run branch (the local deletion stays
unstaged, so the branch keeps them). The local outbox returns toward clean. Variant
scratch + sealed key were always in sub-agent scratch and were never in outbox.

**e. Next eval.** Repeat a through d for the next slug in the batch.

### 7. Run end - reap children, print the branch

After the last eval ships:

- Reap ALL child processes spawned during the run (no lingering grader/shell/agent
  processes). The shell scripts each carry their own `trap ... kill $(jobs -p) EXIT`;
  the orchestrator additionally confirms no background jobs remain before declaring
  the run complete.
- Append a line to STAN_STATE Run history: `run/<timestamp>` + eval count + date.
- Print the run branch name plainly for Stan, e.g.:
  ```
  Run complete. 5 evals shipped on branch: run/20260521T143000Z
  Copy that branch name and send it to Damian. Done.
  ```

### 8. Resumability

If a run was interrupted (laptop closed, network drop), Stan just types `/eval-run`
again. The orchestrator reads STAN_STATE, sees which slugs are already `done`, and
SKIPS them - no duplicate work, no double-shipping. It resumes the same batch from
the first not-yet-done slug. Because each eval is shipped + recorded the moment it
finishes (steps 6b and 6c), at most one eval's work is ever in flight when an
interruption hits.

---

## Eval sub-agent spawn-prompt template

Dispatch each eval sub-agent with a prompt of this shape (fill the bracketed
fields from the spec). State the write constraint explicitly - it is the core
sandbox guarantee:

```
You are an eval sub-agent running ONE prompt-eval end to end using the
model-gauntlet /eval-pit four-phase flow. You run in your own context window.

Eval: NN-slug = [e.g. 01-verbatim-capture]
Spec file: specs/[slug].md   (read it for task_category, prompt_under_test,
                               variant pool, corpus path, corpus_intent)
Rubric: rubric/rubric.md   (the FROZEN scoring contract - score against this)

Run the four phases internally:
- Phase 0: validate the corpus path + corpus_intent vs delivered (HALT-signal if mismatch).
- Phase 1: stage the variant pool (12 by default, or the spec's reduced N), assign
  sealed labels A through L, seal the model->label map in YOUR OWN scratch (never outbox).
  Dispatch the variant runs.
- Phase 2: Architect Pass 1 sealed scoring - 9 dimensions dimension-by-dimension +
  the binary instruction-following gate, WITHOUT opening the sealed key. Length
  disclosure before scoring.
- Phase 3: Architect Pass 2/3 - reveal the key, compute weighted totals, apply the
  within-family tiebreaker then the cross-family cost-override table from rubric/rubric.md,
  write the tally.

HARD WRITE CONSTRAINT (sandbox - non-negotiable):
- You may write ONLY these two files:
    outbox/NN-slug.tally.md     (the headline result + the two winners)
    outbox/NN-slug.scores.md    (the sealed-scoring audit trail)
- Variant raw outputs and the sealed key stay in YOUR scratch and are NOT copied to outbox.
- Any attempt to write ANY other path (home dir, system paths, other repo files,
  STAN_STATE.md) = STOP and return scope-exceeded. The orchestrator owns STAN_STATE,
  not you.

The tally headline MUST contain two clearly labelled lines the send script can grep:
  Quality winner: <model+effort> (weighted total X.X/5.0)
  Practical winner: <model+effort> (<cost-override rule fired OR "same as quality">)

Constraints: NO em dashes (spaced hyphens), NO emojis, universal output envelope
(schemaVersion: 1, tier, status, tool_budget_used), sequential processing, sealed
identity discipline. Process variants one at a time within yourself; do not batch.
```

---

## Editing STAN_STATE during a run

The orchestrator (this command, in the main run context) is the ONLY writer of
STAN_STATE.md during a run. Eval sub-agents never touch it. After each eval ships,
update three things: flip the slug to `done` in the Eval queue, add the Completed
row, and (at run end) append the Run history line. Never hand-edit STAN_STATE while
a run is in progress from outside the orchestrator - that races the run.

---

## What Stan types, total

```
/eval-run
```
On the first run only, Stan answers one question (Telegram token + chat id, or
ENTER to skip). Every run after is zero-question. When it finishes, Stan copies the
printed `run/<timestamp>` branch name and sends that one line to Damian.

---

## Recovery: the orchestrator died mid-run

If the orchestrator process itself died and left completed tallies stranded in
`outbox/` (not shipped, not recorded), Stan can manually flush them:
```
!bash scripts/send-and-clean.sh
```
This bulk-ships whatever is in outbox/ to a fresh run branch and wipes outbox/. It
is a fallback only - the normal path ships each eval as it finishes, so outbox/ is
usually empty or holds at most one in-flight eval. Prefer simply re-running
`/eval-run` (resumable) over the manual flush unless the orchestrator cannot start.

---

## Constraints

- NO em dashes anywhere (use spaced hyphens or en-dashes).
- NO emojis.
- NEVER push to master. Run branches (`run/<timestamp>`) only.
- `git add` SPECIFIC files in the per-eval send (handled by send-eval.sh), never
  `git add outbox/` wholesale - that mechanic is what lets the run branch accumulate
  all evals while the local outbox returns to clean between evals.
- Sequential batch processing. One eval fully done (run, ship, record, wipe) before
  the next.
- All sub-agents use the universal output envelope.
- Sandbox: writes confined to `outbox/` + `STAN_STATE.md`; child processes reaped at
  run end.

---

## Related

- `commands/eval-pit.md` - the single-eval four-phase runner this orchestrator wraps.
- `STAN_STATE.md` - the framework memory trunk read at run start, updated after each eval.
- `rubric/rubric.md` - the frozen scoring contract.
- `scripts/send-eval.sh` - per-eval incremental send.
- `scripts/preflight.sh` - corpus + private-content gate.
- `scripts/setup-return-channel.sh` - one-time return-channel setup.
- `scripts/send-and-clean.sh` - recovery flush (fallback only).
- `docs/starting-prompt.md` - the paste-and-go bootstrap for Stan.
