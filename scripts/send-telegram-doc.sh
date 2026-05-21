#!/usr/bin/env bash
#
# send-telegram-doc.sh - Telegram document-delivery mode.
#
# Sends ONE eval's result files (the tally, and the scores if present) to a
# Telegram chat as DOCUMENTS via the Bot API sendDocument endpoint. This is the
# zero-git delivery path: a runner with a Telegram bot token + chat id can ship
# eval results with NO GitHub push and NO git auth at all. Each result file
# arrives in the chat as a downloadable .md attachment the moment its eval lands.
#
# The token + chat id are RUNTIME-ONLY. They come from the gitignored
# config/return-channel.env (or are already exported in the environment by the
# orchestrator). They are NEVER hardcoded here and NEVER committed.
#
# Usage:
#   scripts/send-telegram-doc.sh <NN-slug>
# Example:
#   scripts/send-telegram-doc.sh 01-verbatim-capture
#
# Idempotent-ish: re-running re-sends the documents (Telegram has no dedupe), so
# the orchestrator calls this exactly once per eval. A send failure exits non-zero
# so the caller knows the result did NOT arrive (unlike the git path, there is no
# branch to fall back on - Telegram IS the source of truth in this mode).

set -euo pipefail

# Reap any background children on exit (no lingering shell processes).
trap 'kill $(jobs -p) 2>/dev/null || true' EXIT

# ---- args ----
if [ "$#" -ne 1 ]; then
  echo "ERROR: usage: scripts/send-telegram-doc.sh <NN-slug>" >&2
  echo "  e.g. scripts/send-telegram-doc.sh 01-verbatim-capture" >&2
  exit 2
fi
SLUG="$1"

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

# ---- load the runtime return-channel config (gitignored) if present ----
CONFIG="config/return-channel.env"
if [ -f "$CONFIG" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
fi

# ---- require both values; this script is ONLY for Telegram-document mode ----
if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
  echo "ERROR: Telegram-document mode needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID." >&2
  echo "  Set them in $CONFIG (gitignored) or export them before calling. Never commit them." >&2
  exit 2
fi

# ---- helper: send one file as a Telegram document, with an optional caption ----
send_doc() {
  local file="$1"
  local caption="$2"
  # Multipart upload: chat_id + document=@file. --max-time guards against a hung
  # connection. We check the API's "ok":true field, not just curl's exit code,
  # because Telegram returns HTTP 200 with ok:false on logical errors.
  local resp
  resp="$(curl -sS --max-time 60 \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
    -F "chat_id=${TELEGRAM_CHAT_ID}" \
    -F "document=@${file}" \
    -F "caption=${caption}" 2>/dev/null || true)"
  case "$resp" in
    *'"ok":true'*) return 0 ;;
    *) echo "  Telegram API response: ${resp:-<empty - network/timeout>}" >&2; return 1 ;;
  esac
}

# ---- send the tally (headline), then the scores audit trail if present ----
# Pull the two winner lines for the tally caption so the chat shows them inline.
QWIN="$(grep -i -m1 'Quality winner' "$TALLY" 2>/dev/null | sed 's/^[#>* -]*//' || true)"
PWIN="$(grep -i -m1 'Practical winner' "$TALLY" 2>/dev/null | sed 's/^[#>* -]*//' || true)"
[ -z "$QWIN" ] && QWIN="Quality winner: (see tally)"
[ -z "$PWIN" ] && PWIN="Practical winner: (see tally)"
TALLY_CAPTION="eval ${SLUG} - tally
${QWIN}
${PWIN}"

if ! send_doc "$TALLY" "$TALLY_CAPTION"; then
  echo "send-telegram-doc: FAILED to send tally for ${SLUG}. Result did NOT arrive in Telegram." >&2
  exit 1
fi

if [ -f "$SCORES" ]; then
  if ! send_doc "$SCORES" "eval ${SLUG} - scores audit trail"; then
    # Scores is best-effort; the headline tally already landed. Warn but do not fail.
    echo "send-telegram-doc: ${SLUG} tally delivered; scores send failed (best-effort)." >&2
    exit 0
  fi
fi

echo "send-telegram-doc: ${SLUG} delivered to Telegram chat as document(s). No git push needed."
exit 0
