# Starting Prompt - Paste-and-Go

The whole point: clone the repo, open Claude Code in the folder, type one command,
answer one question the very first time, and the framework does the rest. It runs a
batch of evals and sends each result the moment it finishes.

How results come back depends on that one first-run answer:

- **Give a Telegram bot token + chat id -> results arrive in Telegram** as document
  attachments, one per eval. No git push, no GitHub access needed at all. This is the
  easiest path - nothing to copy back.
- **Press ENTER to skip -> results push to a git branch** and you copy the printed
  branch name back to Damian (needs GitHub push access).

If you do not have Claude Code, see [METHOD.md section 12](../METHOD.md#12-for-users-without-claude-code-agents-lite-path)
for the lite path.

---

## Prerequisites

1. **Claude Code installed** (the agent harness that runs the orchestrator and its
   sub-agents).
2. **git installed** (used to clone the repo either way).
3. **GitHub push access - ONLY if you skip Telegram.** If you have a Telegram bot
   token + chat id, you do NOT need any GitHub auth - results are delivered straight
   to Telegram and nothing is pushed. Only the git-push (no-token) mode needs push
   access (via `gh auth login` or a clone token). You can never touch `master`
   either way (it is protected, by design).

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
id. That answer picks how results come back:

- **Enter the token + chat id** and each eval's result files are sent to that
  Telegram chat as documents the moment the eval finishes - no git push, no GitHub
  access needed.
- **Press ENTER to skip** and it falls back to git-push mode (results push to a
  `run/<timestamp>` branch).

It saves the choice and never asks again. Either way the run proceeds.

Then it works on its own. It reads the framework memory, runs the next batch of
evals (at least 5) one at a time, and ships each result the moment that eval
finishes. You do NOT open or close any chats. Leave it running until it prints the
run-complete line.

### 4. Get the results to Damian

When it finishes it prints one of two things, depending on the mode you chose:

- **Telegram mode** - the results are already in the Telegram chat as document
  attachments. Nothing to copy:
  ```
  Run complete. 5 evals delivered to the Telegram chat as documents. Done.
  ```
  Damian already has them.

- **git-push mode** - it prints a branch name:
  ```
  Run complete. 5 evals shipped on branch: run/20260521T143000Z
  Copy that branch name and send it to Damian. Done.
  ```
  Copy that one line (`run/20260521T143000Z`) and send it to Damian.

That is the whole job.

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
Read GAUNTLET_QUEUE.md, do the one-time return-channel setup only if config/return-channel.env
is missing, run scripts/preflight.sh, then run the next batch of at least 5 queued
evals one at a time. After EACH eval finishes, ship it with
scripts/send-eval.sh <NN-slug> <run-branch>, update GAUNTLET_QUEUE.md, wipe that eval's
files from outbox/, and move to the next. send-eval.sh auto-selects the delivery mode:
if a Telegram bot token + chat id are configured in config/return-channel.env it sends
each result file to the Telegram chat as a document (no git push, pass run/telegram as
the branch arg); otherwise it pushes to a single run/<timestamp> branch (never master).
At the end, print the run branch name (git mode) or confirm delivery to Telegram (telegram
mode) so I can pass the result to Damian. Confine all writes to outbox/ and GAUNTLET_QUEUE.md,
never commit the Telegram token, and reap all child processes at the end.
```

---

## If something interrupts you

- **The run stops partway** (you closed the laptop, network dropped): just type
  `/eval-run` again. It checks the framework memory, skips the evals already done,
  and continues the same batch. Nothing breaks, nothing double-sends.
- **A push or Telegram send fails** (network): it retries safely - re-running
  `/eval-run` re-ships any not-yet-done eval (re-pushes the branch in git mode, or
  re-sends the documents in Telegram mode). Re-running `/eval-run` is always safe.
- **It says something about corpus paths**: a corpus file the batch needs is missing.
  Relay the exact message to Damian; he fixes the spec and you re-run.

---

## What you never need to know

You do not need to understand variants, rubrics, sealed keys, cost-overrides, or
any of the method internals. Those are Damian's. Your job is the four actions above:
clone, open Claude Code, type `/eval-run`, then relay the result (a Telegram drop
needs nothing from you; a git run needs the branch name copied back). The framework
handles everything between.

For the curious: the method itself is documented in [METHOD.md](../METHOD.md), the
evidence base in [EVIDENCE.md](../EVIDENCE.md), and the orchestrator spec in
[commands/eval-run.md](../commands/eval-run.md).
