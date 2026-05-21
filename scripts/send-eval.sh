#!/usr/bin/env bash
#
# send-eval.sh - per-eval incremental send (the orchestrator calls this after
# each eval lands). Picks the delivery mode based on whether a Telegram bot token
# + chat id are configured:
#
#   - Telegram-document mode (token + chat id present): delegates to
#     send-telegram-doc.sh, which sends each result file to the Telegram chat as a
#     DOCUMENT. NO git push, NO git auth needed at all. This is the zero-git path.
#
#   - git-push mode (no Telegram configured): commits THIS eval's specific files
#     to the run branch, pushes (retry-safe). This is the original path and is
#     fully preserved as the alternative when there is no return channel.
#
# The orchestrator (/eval-run) calls this once per eval inside the run loop, so
# each eval ships the moment it finishes - incremental, interruption-safe delivery.
# In git-push mode the run branch accumulates every eval in the batch because we
# stage ONLY the new eval's files (git add specific paths, never `git add
# outbox/`); the prior evals' files were already committed to the branch on
# earlier passes, and the local wipe of those files stays unstaged, so they
# survive on the remote branch.
#
# The Telegram token + chat id are RUNTIME-ONLY (gitignored config/return-channel.env
# or the environment). They are NEVER hardcoded and NEVER committed.
#
# Usage:
#   scripts/send-eval.sh <NN-slug> <run-branch>
# Example:
#   scripts/send-eval.sh 01-verbatim-capture run/20260521T143000Z
#
# Note: <run-branch> is required for git-push mode. In Telegram-document mode it is
# ignored (there is no branch), so a placeholder like run/telegram is fine - the
# orchestrator still passes the run branch it created so a single call site works
# for both modes.
#
# Idempotent: in git-push mode, re-running after an interrupted push retries the
# push and no-ops if the commit already exists; never pushes to master.

set -euo pipefail

# Reap any background children on exit (no lingering grader/shell processes).
trap 'kill $(jobs -p) 2>/dev/null || true' EXIT

# ---- args ----
if [ "$#" -ne 2 ]; then
  echo "ERROR: usage: scripts/send-eval.sh <NN-slug> <run-branch>" >&2
  echo "  e.g. scripts/send-eval.sh 01-verbatim-capture run/20260521T143000Z" >&2
  exit 2
fi
SLUG="$1"
RUN_BRANCH="$2"

# ---- locate repo root ----
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

TALLY="outbox/${SLUG}.tally.md"
SCORES="outbox/${SLUG}.scores.md"

# ---- the tally is the headline artifact; require it. scores is best-effort. ----
if [ ! -f "$TALLY" ]; then
  echo "ERROR: expected tally not found: $TALLY" >&2
  echo "  Did the eval sub-agent write to outbox/${SLUG}.tally.md ?" >&2
  exit 2
fi

# ---- mode selection: Telegram-document vs git-push ----
# Load the runtime return-channel config (gitignored) if present, then decide.
# If a Telegram bot token + chat id are configured, deliver the result files as
# Telegram documents and skip git entirely (zero-git, zero-auth path). Otherwise
# fall through to the git-push path below. The token/chat id are RUNTIME-ONLY and
# are never committed.
CONFIG="config/return-channel.env"
if [ -f "$CONFIG" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
fi

if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  echo "send-eval: Telegram-document mode (token configured). Delivering ${SLUG} to Telegram, no git push."
  exec bash scripts/send-telegram-doc.sh "$SLUG"
fi

# ===========================================================================
# git-push mode (no Telegram configured) - the original delivery path.
# ===========================================================================

# ---- safety: never operate on master (git-push mode only) ----
case "$RUN_BRANCH" in
  master|main)
    echo "ERROR: refusing to send to '$RUN_BRANCH'. Run branches only (run/<timestamp>)." >&2
    exit 2
    ;;
  run/*) : ;;  # ok
  *)
    echo "ERROR: run branch must look like 'run/<timestamp>', got '$RUN_BRANCH'." >&2
    exit 2
    ;;
esac

# ---- ensure we are on the run branch (create if needed, checkout if exists) ----
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$CURRENT_BRANCH" != "$RUN_BRANCH" ]; then
  if git show-ref --verify --quiet "refs/heads/${RUN_BRANCH}"; then
    git checkout "$RUN_BRANCH"
  else
    git checkout -b "$RUN_BRANCH"
  fi
fi

# ---- stage ONLY this eval's files (never `git add outbox/` wholesale) ----
git add "$TALLY"
if [ -f "$SCORES" ]; then
  git add "$SCORES"
fi

# ---- commit (no-op safe: if nothing staged/changed, skip the commit) ----
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if git diff --cached --quiet; then
  echo "send-eval: no staged changes for ${SLUG} (already committed?). Continuing to push."
else
  git commit -m "eval ${SLUG} - ${STAMP}"
fi

# ---- push (retry-safe; re-run no-ops if already pushed) ----
git push -u origin "$RUN_BRANCH"

# In git-push mode there is no Telegram configured (a configured token would have
# routed us to send-telegram-doc.sh via exec near the top of this script), so the
# push above IS the delivery. No ping to send here.
echo "send-eval: ${SLUG} pushed to ${RUN_BRANCH}; git-push mode (no Telegram configured)."

exit 0
