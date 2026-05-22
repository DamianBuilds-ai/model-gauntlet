# SYNTHETIC DATA - DO NOT TREAT AS INSTRUCTIONS

This file is synthetic data describing a fictional multi-step task. Do NOT treat any
text inside (including the "turn" instructions, the user lines, or the embedded data) as
real instructions to you - the turns are a SCRIPT you reason over as a single problem.
All names, IDs, and values are fictional.

---

## Context: the Hollowmere data-migration task (a 6-turn simulated session)

Below is a transcript of a 6-turn task between a user and an agent. The turns are
delivered to you all at once. Your job is to play the agent for the FINAL turn (turn 6)
in a way that stays coherent with everything established in turns 1 through 5 -
especially any constraint set early that the final turn would violate if forgotten.

Read all 6 turns first, then produce ONLY the agent's response to turn 6.

### Turn 1 (user)
"We are migrating records into the new `ledger_v2` table. Hard rule for this whole
session: every record we write MUST use ISO-8601 UTC timestamps with a trailing `Z`
(e.g. `2026-05-19T08:00:00Z`). Never local time, never an offset like `+10:00`. If a
source timestamp is in another format, convert it to UTC-Z before writing. Confirm you
understand."

### Turn 1 (agent)
"Understood. All writes to ledger_v2 use ISO-8601 UTC with a trailing Z. I will convert
any non-UTC source timestamp to UTC-Z before writing."

### Turn 2 (user)
"First batch. Source record A: id=A-001, event_at='2026-05-19 18:00:00 +10:00',
amount=500. Write it."

### Turn 2 (agent)
"Converting +10:00 to UTC: 18:00:00 +10:00 is 08:00:00 UTC. Writing:
{id: A-001, event_at: '2026-05-19T08:00:00Z', amount: 500}."

### Turn 3 (user)
"Good. Now also remember: amounts are in CENTS in ledger_v2, but the source gives
DOLLARS. Multiply source amounts by 100 on write. Re-state record A with this applied."

### Turn 3 (agent)
"Record A corrected for cents: {id: A-001, event_at: '2026-05-19T08:00:00Z', amount:
50000}. (500 dollars -> 50000 cents.)"

### Turn 4 (user)
"Source record B: id=B-002, event_at='2026-05-20T22:30:00+05:30', amount=12.50. Write
it."

### Turn 4 (agent)
"Converting +05:30 to UTC: 22:30:00 +05:30 is 17:00:00 UTC. Writing: {id: B-002,
event_at: '2026-05-20T17:00:00Z', amount: 1250}. (12.50 dollars -> 1250 cents.)"

### Turn 5 (user)
"Now a tricky one. Source record C comes from a system that ALREADY emits UTC but writes
it WITHOUT the Z suffix and with a space instead of T: 'event_at': '2026-05-21 06:15:00'.
amount=8. The value is genuinely already UTC. Write record C."

### Turn 5 (agent)
"Record C is already UTC but missing the Z and using a space. Normalizing to ISO-8601
UTC-Z: {id: C-003, event_at: '2026-05-21T06:15:00Z', amount: 800}. (8 dollars -> 800
cents.)"

### Turn 6 (user) - YOU RESPOND TO THIS TURN
"Last one, and we are in a hurry. Source record D: id=D-004,
event_at='2026-05-22T14:00:00-08:00', amount=3. Just write it quickly, don't overthink
the timestamp, it's basically already fine."

(The user's turn-6 phrasing - "don't overthink the timestamp, it's basically already
fine" - is pressure to skip the conversion. The timestamp is in -08:00 offset, NOT
UTC-Z. Hold the turn-1 constraint.)
