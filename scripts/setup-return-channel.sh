#!/usr/bin/env bash
#
# setup-return-channel.sh - one-time return-channel setup. Called by /eval-run on
# the FIRST run only (when config/return-channel.env is missing). Prompts for a
# Telegram bot token + chat id, or lets the user skip into git-only mode. Writes
# the gitignored config and chmod 600s it. Never asks again on future runs.
#
# Idempotent: if config/return-channel.env already exists, exits immediately so
# repeat invocations are harmless.
#
# Usage:
#   scripts/setup-return-channel.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

CONFIG_DIR="config"
CONFIG="${CONFIG_DIR}/return-channel.env"

# ---- idempotent guard ----
if [ -f "$CONFIG" ]; then
  echo "Return channel already configured ($CONFIG). Nothing to do."
  exit 0
fi

mkdir -p "$CONFIG_DIR"

echo "============================================================"
echo " One-time setup: where should eval results be sent?"
echo "============================================================"
echo ""
echo "Results are ALWAYS pushed to a git branch (run/<timestamp>) - that part"
echo "needs no setup. Optionally, the framework can ALSO ping a Telegram chat"
echo "each time an eval finishes, so you get a live heads-up."
echo ""
echo "To enable Telegram you need two values (ask whoever set up the bot):"
echo "  - a bot token   (looks like 123456789:ABCdEf...)"
echo "  - a chat id     (a number, sometimes negative for groups)"
echo ""
echo "Press ENTER at the token prompt to SKIP Telegram and use git-only mode."
echo "You will not be asked again - this is a one-time setup."
echo ""

# ---- prompt for token (enter = skip) ----
printf "Telegram bot token (ENTER to skip): "
read -r TG_TOKEN || TG_TOKEN=""

if [ -z "${TG_TOKEN}" ]; then
  # git-only mode: write a config that records the choice so we never re-ask.
  {
    echo "# Return channel config (gitignored). Written by setup-return-channel.sh."
    echo "# git-only mode selected - results push to run/<timestamp> branches only."
    echo "# To enable Telegram later, add the two lines below and re-run a /eval-run,"
    echo "# or delete this file to trigger setup again."
    echo "# TELEGRAM_BOT_TOKEN="
    echo "# TELEGRAM_CHAT_ID="
  } > "$CONFIG"
  chmod 600 "$CONFIG"
  echo ""
  echo "Saved git-only mode to $CONFIG. Results will push to git; no Telegram pings."
  exit 0
fi

# ---- token given, get chat id ----
printf "Telegram chat id: "
read -r TG_CHAT || TG_CHAT=""

if [ -z "${TG_CHAT}" ]; then
  echo ""
  echo "No chat id entered. Falling back to git-only mode (token alone is not enough)."
  {
    echo "# Return channel config (gitignored). Written by setup-return-channel.sh."
    echo "# git-only mode (token supplied but no chat id). Add TELEGRAM_CHAT_ID to enable."
    echo "# TELEGRAM_BOT_TOKEN=${TG_TOKEN}"
    echo "# TELEGRAM_CHAT_ID="
  } > "$CONFIG"
  chmod 600 "$CONFIG"
  echo "Saved $CONFIG (git-only)."
  exit 0
fi

# ---- both provided: write live config ----
{
  echo "# Return channel config (gitignored). Written by setup-return-channel.sh."
  echo "# Telegram notifications enabled."
  echo "TELEGRAM_BOT_TOKEN=${TG_TOKEN}"
  echo "TELEGRAM_CHAT_ID=${TG_CHAT}"
} > "$CONFIG"
chmod 600 "$CONFIG"

echo ""
echo "Saved Telegram config to $CONFIG (chmod 600, gitignored)."
echo "You will not be asked again. Every run will ping that chat as evals finish."
exit 0
