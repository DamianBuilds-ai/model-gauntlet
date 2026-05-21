#!/usr/bin/env bash
#
# send-eval.sh - per-eval incremental send (the orchestrator calls this after
# each eval lands). Commits THIS eval's specific files to the run branch, pushes
# (retry-safe), and Telegram-notifies if configured.
#
# This is the primary delivery path. The orchestrator (/eval-run) calls it once
# per eval inside the run loop, so each eval ships the moment it finishes -
# incremental, interruption-safe delivery. The run branch accumulates every eval
# in the batch because we stage ONLY the new eval's files (git add specific
# paths, never `git add outbox/`); the prior evals' files were already committed
# to the branch on earlier passes, and the local wipe of those files stays
# unstaged, so they survive on the remote branch.
#
# Usage:
#   scripts/send-eval.sh <NN-slug> <run-branch>
# Example:
#   scripts/send-eval.sh 01-verbatim-capture run/20260521T143000Z
#
# Idempotent: re-running after an interrupted push retries the push and no-ops if
# the commit already exists. Never pushes to master.

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

# ---- safety: never operate on master ----
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

# ---- Telegram notify (best-effort; push already succeeded above) ----
CONFIG="config/return-channel.env"
if [ -f "$CONFIG" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
fi

if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  # Pull the two winner lines out of the tally headline for the notification.
  QWIN="$(grep -i -m1 'Quality winner' "$TALLY" 2>/dev/null | sed 's/^[#>* -]*//' || true)"
  PWIN="$(grep -i -m1 'Practical winner' "$TALLY" 2>/dev/null | sed 's/^[#>* -]*//' || true)"
  [ -z "$QWIN" ] && QWIN="Quality winner: (see tally)"
  [ -z "$PWIN" ] && PWIN="Practical winner: (see tally)"
  MSG="eval ${SLUG} sent on ${RUN_BRANCH}
${QWIN}
${PWIN}"
  if curl -sS --max-time 20 \
      "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
      --data-urlencode "text=${MSG}" >/dev/null 2>&1; then
    echo "send-eval: ${SLUG} pushed to ${RUN_BRANCH}; Telegram notified."
  else
    echo "send-eval: ${SLUG} pushed to ${RUN_BRANCH}; Telegram send failed (best-effort, push is the source of truth)."
  fi
else
  echo "send-eval: ${SLUG} pushed to ${RUN_BRANCH}; git-only mode (no Telegram configured)."
fi

exit 0
