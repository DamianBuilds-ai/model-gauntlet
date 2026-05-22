# /eval-run - Batch Eval Orchestrator (the one command Stan types)

The single command for running prompt-evals with near-zero friction. Stan types
`/eval-run` and the orchestrator reads the framework's memory, runs the next batch
of evals one at a time, ships each eval's result the moment it finishes, updates
the framework's memory, and prints a branch name for Stan to paste back. No chats
to open or close, no per-eval lifecycle, no internals to understand.

This command WRAPS the single-eval `/eval-pit` four-phase flow: the MAIN
orchestrator session runs each eval's `/eval-pit` flow DIRECTLY in its own context.
The main session is the only place the Agent/Task spawn tool exists, so the main
session itself dispatches the variant sub-agents (depth 1) and, after collecting
their outputs, dispatches ONE consolidator sub-agent (Opus) to score and tally.
There is NO intermediate eval sub-agent. Sub-agents cannot spawn sub-agents, so an
eval sub-agent could never fan out the variants - it would silently self-simulate
them and produce invalid data. The topology is FLAT: main session -> variant
sub-agents (depth 1) -> consolidator sub-agent (depth 1).

Evals in a batch run SEQUENTIALLY in the main session (one eval fully finished -
variants dispatched, consolidated, tally shipped, memory updated - before the next
eval starts, to keep peak context low). The variant fan-out WITHIN a single eval is
parallel at depth 1.

**Consumer:** Stan (or any non-technical operator) on a clone of `model-gauntlet`.
**Wraps:** `commands/eval-pit.md` (the single-eval four-phase flow), executed
directly by the main orchestrator session - NOT delegated to an eval sub-agent.

---

## Sandbox contract (read first - this is a hard requirement)

The orchestrator AND every sub-agent it spawns (variant sub-agents + the
consolidator sub-agent) write ONLY to two locations:

- `outbox/` (transient per-eval working files - tally + scores)
- `STAN_STATE.md` (the framework memory trunk, written by the orchestrator only)

Nothing else is read or written outside this repo. No access to Stan's other files,
no permanent files, no home directory, no system paths. The consolidator sub-agent
is spawned with an explicit single-write-path constraint (`outbox/NN-slug.tally.md`
and `outbox/NN-slug.scores.md` ONLY). Variant sub-agents keep their raw output in
their own scratch only. Any write attempt outside `outbox/` is a scope-exceeded
signal, not an action. Variant scratch files and the sealed key live inside the
sub-agents' own scratch and are NEVER copied to outbox.

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
  = git-push mode". It writes the gitignored `config/return-channel.env` (chmod 600)
  and NEVER asks again.

**The token answer selects the delivery mode** (this is the key fork):

- **Token + chat id supplied -> Telegram-document mode.** Each eval's result files
  are SENT to that Telegram chat as documents (`sendDocument`) the moment the eval
  finishes. There is NO git push and NO git auth needed at all - Telegram IS the
  delivery channel and the source of truth. Stan does not need GitHub access in this
  mode.
- **ENTER to skip (no token) -> git-push mode.** Results push to a `run/<timestamp>`
  branch (the original path). This needs git/GitHub push access.

The token + chat id are RUNTIME-ONLY: they live in the gitignored
`config/return-channel.env` and are NEVER committed. Do not ask any other setup
questions, ever. After the first run this step is a silent no-op, and the saved
config alone decides the mode on every later run.

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

### 5. Create the run branch (ONCE per run, git-push mode only)

**Telegram-document mode:** skip this step - there is no branch. Use the literal
string `run/telegram` as the "run branch" argument when calling `send-eval.sh`
(the script ignores it in Telegram mode). Jump to step 6.

**git-push mode:** create a single run branch for the whole batch:
```
!git checkout -b "run/$(date -u +%Y%m%dT%H%M%SZ)"
```
Capture the branch name (e.g. `run/20260521T143000Z`). Every eval in this batch
accumulates on this ONE branch. The orchestrator and scripts push ONLY to this
`run/<timestamp>` branch and NEVER to master. (Master is protected; Stan cannot
touch it. This is intentional.)

### 6. For each eval in the batch, SEQUENTIALLY

Process the batch one eval at a time. Do NOT parallelise the evals - sequential
keeps peak context low, makes an interrupted run leave a clean partial state, and
ships each result the instant it is ready. (The variant fan-out WITHIN a single
eval is parallel at depth 1 - see step 6a. Only the eval-to-eval loop is
sequential.) For each eval:

**a. Run the `/eval-pit` flow DIRECTLY in the main session.** Do NOT delegate the
eval to an intermediate sub-agent - the main session is the only context where the
spawn tool exists, and a sub-agent cannot spawn the variant sub-agents. The main
session itself:
  1. Stages the variant pool (9 variants: 3 models x 3 reruns; or the spec's
     reduced-N override) and seals the label->model map in the main session's own
     scratch.
  2. Dispatches the variant pool from the main session (depth 1), each variant
     pinned with `model: haiku|sonnet|opus`, in ONE parallel background batch.
     Process the eval-to-eval loop sequentially, but the variants of THIS eval fan
     out in parallel.
  3. After all variants land, dispatches ONE consolidator sub-agent (Opus) from the
     main session (depth 1) to run Pass 1 sealed scoring against `rubric/rubric.md`,
     Pass 2 reveal + cost-adjust, and write the tally. The consolidator is
     HARD-CONSTRAINED to write ONLY `outbox/NN-slug.tally.md` and
     `outbox/NN-slug.scores.md`. Use the consolidator spawn-prompt template below.

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for
example, you are yourself a sub-agent), STOP immediately and report: HALT - variant
dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER
generate, role-play, or simulate variant outputs yourself. A halted run is correct;
a self-simulated run is invalid data.

**b. Ship that eval immediately.** Once the tally has landed in outbox:
```
!bash scripts/send-eval.sh <NN-slug> <run-branch>
```
`send-eval.sh` auto-selects the delivery mode from `config/return-channel.env`:

- **Telegram-document mode** (token + chat id present): it sends this eval's result
  files to the Telegram chat as documents via `sendDocument`. No git push, no git
  auth. Pass `run/telegram` as `<run-branch>` (it is ignored in this mode).
- **git-push mode** (no token): it commits ONLY that eval's two files to the run
  branch and pushes (retry-safe). The run branch accumulates this eval on top of any
  already shipped in the batch.

Either way the result is delivered the moment the eval finishes.

**c. Update STAN_STATE.md.** Mark the slug `done` in the Eval queue, add a row to
Completed (slug | run branch | date sent | quality winner | practical winner -
pulled from the tally headline). This is the orchestrator's job; do it now, not at
the end. (See "Editing STAN_STATE" below.)

**d. Wipe that eval's transient files from outbox.** Delete `outbox/NN-slug.tally.md`
and `outbox/NN-slug.scores.md` locally:
```
!rm -f outbox/<NN-slug>.tally.md outbox/<NN-slug>.scores.md
```
The delivered copies are safe: in git-push mode they live on the remote run branch
(the local deletion stays unstaged, so the branch keeps them); in Telegram-document
mode they were already sent to the chat as documents. Either way the local outbox
returns toward clean. Variant scratch + sealed key were always in sub-agent scratch
and were never in outbox.

**e. Next eval.** Repeat a through d for the next slug in the batch.

### 7. Run end - reap children, print the result

After the last eval ships:

- Reap ALL child processes spawned during the run (no lingering grader/shell/agent
  processes). The shell scripts each carry their own `trap ... kill $(jobs -p) EXIT`;
  the orchestrator additionally confirms no background jobs remain before declaring
  the run complete.
- Append a line to STAN_STATE Run history (`run/<timestamp>` or `telegram` + eval
  count + date).
- Print the result plainly for Stan:
  - **git-push mode:** the run branch name, e.g.
    ```
    Run complete. 5 evals shipped on branch: run/20260521T143000Z
    Copy that branch name and send it to Damian. Done.
    ```
  - **Telegram-document mode:** there is no branch - the result files already
    arrived in the Telegram chat, e.g.
    ```
    Run complete. 5 evals delivered to the Telegram chat as documents. Done.
    Nothing to copy - Damian has the results in Telegram.
    ```

### 8. Resumability

If a run was interrupted (laptop closed, network drop), Stan just types `/eval-run`
again. The orchestrator reads STAN_STATE, sees which slugs are already `done`, and
SKIPS them - no duplicate work, no double-shipping. It resumes the same batch from
the first not-yet-done slug. Because each eval is shipped + recorded the moment it
finishes (steps 6b and 6c), at most one eval's work is ever in flight when an
interruption hits.

---

## Variant sub-agent spawn-prompt template

The MAIN session dispatches each of the 9 variants (3 models x 3 reruns) at depth 1
with a prompt of this shape (fill the bracketed fields from the spec). Each variant
is pinned with `model: haiku|sonnet|opus` - the model is the differentiator (effort
is a no-op at dispatch). Variants run sealed: no model self-reference, no cost
estimates. The main session holds the label->model map in its own scratch.

```
You are a sealed variant in a model-gauntlet eval. You produce ONE answer to the
prompt below, with NO awareness of which model you are and NO self-reference.

Eval: NN-slug = [e.g. 01-verbatim-capture]
Sealed label: [e.g. A]   (your output is identified only by this label)
Prompt under test (verbatim - this is the ENTIRE task):
[paste prompt_under_test from specs/[slug].md]
Corpus / data source: [corpus path from the spec]

Rules:
- Answer the prompt as written. Do NOT mention your model, effort, or cost.
- Write your answer to YOUR OWN scratch only (the main session collects it). Do NOT
  write to outbox/, STAN_STATE.md, or any repo file.
- Universal output envelope (schemaVersion: 1, tier, status, tool_budget_used).
- NO em dashes (spaced hyphens), NO emojis. Sequential processing if multi-item.
```

The main session repeats this dispatch once per sealed label (A through I for the
9-variant default), pinning the correct `model:` per the sealed map, in ONE parallel
background batch.

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for
example, you are yourself a sub-agent), STOP immediately and report: HALT - variant
dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER
generate, role-play, or simulate variant outputs yourself. A halted run is correct;
a self-simulated run is invalid data.

---

## Consolidator sub-agent spawn-prompt template

After all variants land, the MAIN session dispatches ONE consolidator sub-agent
(Opus) at depth 1 to score and tally. State the write constraint explicitly - it is
the core sandbox guarantee:

```
You are the consolidator for ONE model-gauntlet eval. You score the variant outputs
and write the tally. You run in your own context window.

Eval: NN-slug = [e.g. 01-verbatim-capture]
Variant outputs: [the main session provides the sealed variant answers, labelled
                  A through I, AND the sealed label->model key]
Rubric: rubric/rubric.md   (the FROZEN scoring contract - score against this)

Run two sealed passes:
- Pass 1: sealed scoring - score the 9 dimensions dimension-by-dimension across ALL
  variants + the binary instruction-following gate, WITHOUT looking at the
  label->model key. Length disclosure (word counts) BEFORE scoring.
- Pass 2/3: reveal the key, compute weighted totals, apply the within-family
  tiebreaker then the cross-family cost-override table from rubric/rubric.md, write
  the tally.

HARD WRITE CONSTRAINT (sandbox - non-negotiable):
- You may write ONLY these two files:
    outbox/NN-slug.tally.md     (the headline result + the two winners)
    outbox/NN-slug.scores.md    (the sealed-scoring audit trail)
- Any attempt to write ANY other path (home dir, system paths, other repo files,
  STAN_STATE.md) = STOP and return scope-exceeded. The orchestrator owns STAN_STATE,
  not you.

The tally headline MUST contain two clearly labelled lines the send script can grep:
  Quality winner: <model> (weighted total X.X/5.0)
  Practical winner: <model> (<cost-override rule fired OR "same as quality">)

Constraints: NO em dashes (spaced hyphens), NO emojis, universal output envelope
(schemaVersion: 1, tier, status, tool_budget_used), sequential processing, sealed
identity discipline (do not open the key until Pass 2).
```

HALT GUARD: if the Agent/Task spawn tool is not available in your context (for
example, you are yourself a sub-agent), STOP immediately and report: HALT - variant
dispatch requires the main session; sub-agents cannot spawn sub-agents. NEVER
generate, role-play, or simulate variant outputs yourself. A halted run is correct;
a self-simulated run is invalid data.

---

## Editing STAN_STATE during a run

The orchestrator (this command, in the main run context) is the ONLY writer of
STAN_STATE.md during a run. Variant and consolidator sub-agents never touch it.
After each eval ships,
update three things: flip the slug to `done` in the Eval queue, add the Completed
row, and (at run end) append the Run history line. Never hand-edit STAN_STATE while
a run is in progress from outside the orchestrator - that races the run.

---

## What Stan types, total

```
/eval-run
```
On the first run only, Stan answers one question (Telegram token + chat id, or
ENTER to skip). That one answer picks the delivery mode for good:
- **Token given:** results arrive in the Telegram chat as documents. Nothing to copy
  back - Damian already has them. No GitHub access needed.
- **Skipped:** results push to a `run/<timestamp>` branch; Stan copies that printed
  branch name and sends that one line to Damian.

Every run after is zero-question.

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

Note: `send-and-clean.sh` is a git-push-mode flush. In Telegram-document mode there
is no branch to flush to - just re-run `/eval-run`, which re-sends any not-yet-`done`
evals as Telegram documents.

---

## Constraints

- NO em dashes anywhere (use spaced hyphens or en-dashes).
- NO emojis.
- Two delivery modes, picked by `config/return-channel.env`: Telegram-document
  (token present, zero git) or git-push (no token).
- In git-push mode: NEVER push to master - run branches (`run/<timestamp>`) only.
  `git add` SPECIFIC files in the per-eval send (handled by send-eval.sh), never
  `git add outbox/` wholesale - that mechanic is what lets the run branch accumulate
  all evals while the local outbox returns to clean between evals.
- NEVER hardcode or commit the Telegram bot token or chat id. They are runtime-only,
  loaded from the gitignored `config/return-channel.env`.
- Sequential batch processing. One eval fully done (run, ship, record, wipe) before
  the next.
- All sub-agents use the universal output envelope.
- Sandbox: writes confined to `outbox/` + `STAN_STATE.md`; child processes reaped at
  run end.

---

## Related

- `commands/eval-pit.md` - the single-eval four-phase flow this orchestrator runs directly in the main session.
- `STAN_STATE.md` - the framework memory trunk read at run start, updated after each eval.
- `rubric/rubric.md` - the frozen scoring contract.
- `scripts/send-eval.sh` - per-eval incremental send; auto-selects Telegram-document
  or git-push mode from `config/return-channel.env`.
- `scripts/send-telegram-doc.sh` - Telegram-document delivery (sends each result file
  to the chat as a document via `sendDocument`; zero git, zero auth).
- `scripts/preflight.sh` - corpus + private-content gate.
- `scripts/setup-return-channel.sh` - one-time return-channel setup.
- `scripts/send-and-clean.sh` - git-push-mode recovery flush (fallback only).
- `docs/starting-prompt.md` - the paste-and-go bootstrap for Stan.
