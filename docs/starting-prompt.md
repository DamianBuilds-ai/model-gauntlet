# Starting Prompt - Paste-and-Go

The whole point: clone the repo, open Claude Code in the folder, type one command,
answer one question the very first time, and the framework does the rest. It runs a
batch of evals, sends each result the moment it finishes, and prints a branch name
for you to paste back to Damian.

If you do not have Claude Code, see [METHOD.md section 12](../METHOD.md#12-for-users-without-claude-code-agents-lite-path)
for the lite path.

---

## Prerequisites (3 things)

1. **Claude Code installed** (the agent harness that runs the orchestrator and its
   sub-agents).
2. **git installed** (results are delivered by pushing to a branch).
3. **GitHub access to the repo** - either `gh auth login` done once, or a clone
   token / credential that lets you push to `run/*` branches. You can clone and
   push; you cannot touch `master` (it is protected, by design).

---

## The four actions

### 1. Clone the repo

```bash
gh auth login            # one time - pick GitHub, HTTPS, follow the browser prompt
git clone https://github.com/DamianBuilds-ai/model-gauntlet.git
cd model-gauntlet
```

### 2. Open Claude Code in the folder

```bash
claude
```
(or open the `model-gauntlet` folder in your Claude Code app)

### 3. Type the one command

```
/eval-run
```

**On the very first run only,** it asks one question: a Telegram bot token and chat
id so it can ping you as evals finish. If you do not have those, just press ENTER to
skip - it falls back to git-only mode and never asks again. Either way the run
proceeds.

Then it works on its own. It reads the framework memory, runs the next batch of
evals (at least 5) one at a time, and ships each result the moment that eval
finishes. You do NOT open or close any chats. Leave it running until it prints the
run-complete line.

### 4. Send Damian the branch name

When it finishes it prints something like:

```
Run complete. 5 evals shipped on branch: run/20260521T143000Z
Copy that branch name and send it to Damian. Done.
```

Copy that one line (`run/20260521T143000Z`) and send it to Damian. That is the whole
job.

---

## The literal prompt block

You do not need to paste a long prompt. The single command IS the prompt:

```
/eval-run
```

If for some reason the slash command is not picked up, paste this instead and it
does the same thing:

```
Run the /eval-run orchestrator from this repo (commands/eval-run.md).
Read STAN_STATE.md, do the one-time return-channel setup only if config/return-channel.env
is missing, run scripts/preflight.sh, then run the next batch of at least 5 queued
evals one at a time. After EACH eval finishes, ship it with
scripts/send-eval.sh <NN-slug> <run-branch>, update STAN_STATE.md, wipe that eval's
files from outbox/, and move to the next. Push only to a single run/<timestamp>
branch, never to master. At the end, print the run branch name for me to send to Damian.
Confine all writes to outbox/ and STAN_STATE.md, and reap all child processes at the end.
```

---

## If something interrupts you

- **The run stops partway** (you closed the laptop, network dropped): just type
  `/eval-run` again. It checks the framework memory, skips the evals already done,
  and continues the same batch. Nothing breaks, nothing double-sends.
- **A push fails** (network): it retries safely - the framework re-pushes on the
  next attempt. Re-running `/eval-run` is always safe.
- **It says something about corpus paths**: a corpus file the batch needs is missing.
  Relay the exact message to Damian; he fixes the spec and you re-run.

---

## What you never need to know

You do not need to understand variants, rubrics, sealed keys, cost-overrides, or
any of the method internals. Those are Damian's. Your job is the four actions above:
clone, open Claude Code, type `/eval-run`, send the branch name. The framework
handles everything between.

For the curious: the method itself is documented in [METHOD.md](../METHOD.md), the
evidence base in [EVIDENCE.md](../EVIDENCE.md), and the orchestrator spec in
[commands/eval-run.md](../commands/eval-run.md).
