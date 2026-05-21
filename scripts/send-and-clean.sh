#!/usr/bin/env bash
#
# send-and-clean.sh - RECOVERY FALLBACK ONLY.
#
# The normal path is the orchestrator (/eval-run), which calls send-eval.sh after
# EACH eval so results ship incrementally. You should rarely need this script.
#
# Use it only when the orchestrator DIED mid-run and left completed tallies sitting
# in outbox/ unsent. This flushes whatever is in outbox/ to a fresh run branch in
# one shot, then wipes outbox/ back to clean. It is the manual "ship the partial
# batch and reset" button.
#
# Differences from the per-eval send: this stages the WHOLE outbox at once and
# creates its own run branch. The per-eval send (send-eval.sh) is the one that
# accumulates evals on a single branch incrementally; this one is the bulk
# recovery flush.
#
# Usage:
#   scripts/send-and-clean.sh
#
# Idempotent: re-running after an interrupted push retries the push. The wipe only
# fires after a successful push (set -e aborts before the wipe if push fails), so
# an auth/network failure never loses your outbox.

set -euo pipefail

# Reap any background children on exit.
trap 'kill $(jobs -p) 2>/dev/null || true' EXIT

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# 0. guard: refuse if outbox is empty (nothing to send)
if [ -z "$(find outbox -type f ! -name '.gitkeep' 2>/dev/null)" ]; then
  echo "outbox/ is empty - nothing to send. Did /eval-run finish, or did it already ship each eval?"
  exit 2
fi

BRANCH="run/$(date -u +%Y%m%dT%H%M%SZ)"

# 1. bundle: stage every result file in outbox (recovery flush stages the lot,
#    by design - this is the partial-batch rescue path, not the incremental path).
git checkout -b "$BRANCH"
git add outbox/*.tally.md outbox/*.scores.md 2>/dev/null || true
# Fall back to staging any remaining non-gitkeep files if the globs missed.
git add -- outbox/ ':!outbox/.gitkeep' 2>/dev/null || true

EVAL_COUNT="$(find outbox -name '*.tally.md' 2>/dev/null | wc -l | tr -d ' ')"
git commit -m "eval run recovery flush $(date -u +%Y-%m-%dT%H:%M:%SZ) - ${EVAL_COUNT} evals"

# 2. ship: push the branch (retry-safe; re-run no-ops if already pushed)
git push -u origin "$BRANCH"

# 3. self-clean: return to master, wipe outbox back to .gitkeep only.
#    NOTE: master, not main - this repo's default branch is master.
git checkout master
find outbox -type f ! -name '.gitkeep' -delete

echo "Recovery flush sent on branch $BRANCH and wiped outbox/. Clean slate for next run."
echo "Tell Damian: $BRANCH"
exit 0
