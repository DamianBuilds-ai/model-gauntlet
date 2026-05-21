#!/usr/bin/env bash
#
# preflight.sh - run by /eval-run before any eval dispatches. Two jobs:
#   1. Validate that every batch spec's corpus path exists on disk.
#   2. Private-content guard: scan outbox/, specs/, corpus/, and any EXAMPLE-*/
#      reference folders for markers that should never appear in this PUBLIC repo
#      (machine paths, internal domain names, infra tokens, table IDs). This is a
#      safety NET that reinforces the no-private-content rule - not the primary
#      sanitization.
#
# Usage:
#   scripts/preflight.sh [corpus-path ...]
#
# The orchestrator passes the corpus path of every eval in the current batch as
# arguments. With no arguments, the corpus-path check is skipped (guard still
# runs) so the script can be used as a standalone private-content lint.
#
# Exit 0 only if all supplied paths exist AND the guard finds nothing.
# Exit 1 on any broken path or any private-content hit, with a plain-English
# message naming the offending path / file+line.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

FAIL=0

# ---------------------------------------------------------------------------
# 1. Corpus path validation
# ---------------------------------------------------------------------------
if [ "$#" -gt 0 ]; then
  echo "preflight: checking ${#} corpus path(s)..."
  for p in "$@"; do
    if [ -e "$p" ]; then
      echo "  OK    $p"
    else
      echo "  BROKEN  $p" >&2
      echo "" >&2
      echo "HALT: corpus path does not exist: '$p'" >&2
      echo "      An eval in this batch points at a corpus file/folder that is" >&2
      echo "      not on disk. Fix the spec's corpus path (or add the missing" >&2
      echo "      corpus file under corpus/) before running." >&2
      FAIL=1
    fi
  done
else
  echo "preflight: no corpus paths supplied - skipping path check (guard still runs)."
fi

# ---------------------------------------------------------------------------
# 2. Private-content guard
# ---------------------------------------------------------------------------
# Known-private markers that must NEVER land in this public repo. If the example
# eval or any seeded corpus accidentally carries Damian's private content, this
# catches it loudly. Word-boundary anchored where it matters to cut false hits.
echo "preflight: scanning outbox/ specs/ corpus/ EXAMPLE-*/ for private-content markers..."

SCAN_DIRS=()
for d in outbox specs corpus; do
  [ -d "$d" ] && SCAN_DIRS+=("$d")
done
# Also scan any EXAMPLE-*/ reference eval folders. These ship completed synthetic
# evals as structural references; they are public-facing so the guard covers them
# too. The literal glob is skipped harmlessly when no such folder exists.
for d in EXAMPLE-*/; do
  [ -d "$d" ] && SCAN_DIRS+=("${d%/}")
done

# Patterns are extended-regex (grep -E). The repo ships NO private literals.
# Real internal names, paths, domains and secrets live in a gitignored
# .preflight-needles file (one regex per line, # for comments) so they never
# enter version control. A fresh clone has no needles and the scan is a harmless
# no-op, which is correct - a fresh clone has no private content to leak.
# See .preflight-needles.example for the format.
PATTERNS=()
if [ -f .preflight-needles ]; then
  while IFS= read -r line; do
    case "$line" in ''|\#*) continue;; esac
    PATTERNS+=("$line")
  done < .preflight-needles
fi

if [ "${#SCAN_DIRS[@]}" -eq 0 ]; then
  echo "  (no outbox/specs/corpus dirs present yet - nothing to scan)"
else
  for pat in "${PATTERNS[@]}"; do
    # --include limits to text-ish files; .gitkeep and binaries are skipped by -I.
    # We grep recursively, print file:line, and treat ANY hit as a failure.
    HITS="$(grep -RInE -- "$pat" "${SCAN_DIRS[@]}" 2>/dev/null || true)"
    if [ -n "$HITS" ]; then
      echo "" >&2
      echo "PRIVATE-CONTENT HIT for pattern: $pat" >&2
      echo "$HITS" | sed 's/^/  /' >&2
      FAIL=1
    fi
  done
  if [ "$FAIL" -eq 0 ]; then
    echo "  clean - no private-content markers found."
  fi
fi

# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------
if [ "$FAIL" -ne 0 ]; then
  echo "" >&2
  echo "PREFLIGHT FAILED. Fix the issues above before running /eval-run." >&2
  echo "If a private-content hit is a false positive, sanitize the wording in" >&2
  echo "the named file - this repo is PUBLIC and the guard is intentionally strict." >&2
  exit 1
fi

echo "preflight: all checks passed."
exit 0
