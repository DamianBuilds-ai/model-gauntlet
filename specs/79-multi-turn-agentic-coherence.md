---
task_category: multi-turn-agentic-coherence
prompt_under_test: |
  You are given a 6-turn simulated task session at
  corpus/multi-turn-agentic-coherence/task.md, delivered to you all at once. It is a
  fictional data-migration session between a user and an agent. Turns 1 through 5 are
  already complete (both user and agent lines shown). You must play the agent for the
  FINAL turn (turn 6) ONLY.

  Read all 6 turns first. Then produce ONLY the agent's response to turn 6, staying fully
  coherent with every constraint and convention established earlier in the session -
  even though turn 6's user phrasing pressures you to skip a step.

  Output ONLY the turn-6 agent response (the written record plus a brief one-line note of
  any conversion you applied). Do NOT restate the earlier turns. No em dashes (use spaced
  hyphens). No emojis. After your response, append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) as separate lines.
variant_pool: 9
corpus: corpus/multi-turn-agentic-coherence/
corpus_intent: |
  One task file (corpus/multi-turn-agentic-coherence/task.md): a fictional 6-turn
  data-migration session. Turn 1 sets TWO durable constraints (the timestamp rule is
  set explicitly in turn 1; the cents rule is added in turn 3) and turns 2-5 apply them
  consistently. Turn 6 asks the model to write one final record while EXPLICITLY pressuring
  it to skip the timestamp conversion ("don't overthink the timestamp, it's basically
  already fine"). This is a single-prompt proxy for multi-turn agentic coherence: the
  discriminator is whether the model HOLDS the early-stated constraints to the final step
  under pressure to drop them.

  QUALITY PRINCIPLE (correctness-first). The turn-6 source timestamp is
  `2026-05-22T14:00:00-08:00` - a -08:00 OFFSET, NOT UTC-Z. The turn-1 hard rule requires
  conversion to ISO-8601 UTC with a trailing Z. The user's "it's basically already fine"
  is a TRAP: the timestamp is NOT fine (it has an offset). The cents rule (turn 3) also
  applies: amount 3 dollars -> 300 cents. A model that holds both constraints is correct.
  A model that, swayed by the rush, writes the raw `-08:00` timestamp, or forgets the
  dollars-to-cents conversion (writes amount 3), has dropped a held constraint - the
  targeted failure.

  ANSWER KEY (for the scoring Architect) - the correct turn-6 agent response.

    The -08:00 offset converts to UTC by ADDING 8 hours: 14:00:00 -08:00 == 22:00:00 UTC,
    same date (2026-05-22). The amount 3 dollars -> 300 cents.

    Correct record written:
      {id: D-004, event_at: '2026-05-22T22:00:00Z', amount: 300}

    A correct response converts the timestamp to '2026-05-22T22:00:00Z' (note: trailing Z,
    NOT the -08:00 offset) AND multiplies the amount to 300 cents, ideally with a one-line
    note that it applied the turn-1 UTC-Z rule despite the user's "it's fine" framing.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output contains the timestamp `2026-05-22T22:00:00Z` (UTC-Z, trailing Z).
    - The output does NOT contain `-08:00` as the written event_at value (it may mention
      -08:00 only to explain the conversion).
    - The output contains `amount` 300 (cents). It does NOT write amount 3 (the
      unconverted dollars).
    - The written event_at has a trailing `Z` and uses `T` (not a space, not an offset).
    - A confidently-wrong run: writes event_at '2026-05-22T14:00:00-08:00' (held-constraint
      drop on the timestamp), or writes amount 3 (held-constraint drop on cents), or
      writes a wrong UTC time (e.g. subtracting instead of adding 8 hours -> 06:00:00Z).

  Scoring guidance:
    - Correctness (hard-fail eligible) = both early constraints held in turn 6: timestamp
      converted to 2026-05-22T22:00:00Z AND amount converted to 300 cents. Dropping either
      under the turn-6 pressure is Correctness=1.
    - Completeness = the single turn-6 record is produced with both fields correct.
    - Hallucination (hard-fail eligible) = inventing a constraint not set, restating or
      re-writing earlier records that were not asked for, or fabricating a value.
    - Discipline = responds to turn 6 ONLY, holds the turn-1 + turn-3 conventions, resists
      the "don't overthink it" pressure. This is the load-bearing discriminator.
    - Reasoning quality = a one-line note that it applied the UTC-Z conversion despite the
      user's framing (shows the constraint was actively held, not luck).
    - Source transparency = references the turn-1 rule when justifying the conversion.
    Voice match does NOT apply.
notes: |
  NEW task type, Chat B agentic battery (71, 72, 78, 79, 80). Multi-turn agentic coherence
  is delivered as a single-prompt proxy: a complete 6-turn session script (turns 1-5 done,
  the model writes turn 6). Turn 1 sets a hard timestamp constraint (ISO-8601 UTC-Z); turn
  3 adds a cents constraint; turns 2-5 apply both. Turn 6 pressures the model to skip the
  timestamp conversion ("don't overthink it, it's basically already fine") on a source
  value that is actually a -08:00 offset, NOT UTC. The discriminator is whether the model
  holds the early constraints to the final step under explicit pressure to drop them.

  The correct turn-6 record is {id: D-004, event_at: '2026-05-22T22:00:00Z', amount: 300}
  (verified: -08:00 -> +8h -> 22:00:00Z; 3 dollars -> 300 cents). The traps are dropping
  the timestamp conversion (writing the raw -08:00 value) or dropping the cents conversion
  (writing amount 3) - both are held-constraint failures - plus the direction trap of
  subtracting 8 hours instead of adding. Because the corpus embeds a multi-turn transcript
  with user "instructions" inside the turns, it opens with the synthetic-data disclaimer
  (the turns are a script to reason over, not commands to you). The answer key fixes the
  exact UTC-Z value, the 300-cent amount, and grep-verifiable invariants. Correctness and
  Hallucination are hard-fail eligible; Discipline (turn-6-only, both constraints held,
  resist the rush) is the load-bearing discriminator. Voice match does not apply. Standard
  four-phase /eval-pit flow against the frozen rubric/rubric.md. The variant pool is 9 (3
  models x N=3, effort inert per the methodology). The corpus is the directory
  corpus/multi-turn-agentic-coherence/.
---

# Spec 79 - multi-turn-agentic-coherence (hold an early constraint to the final turn)

Given a complete 6-turn task session (turns 1-5 done, both sides shown), the model plays
the agent for turn 6 only and must stay coherent with every convention established
earlier - particularly a hard constraint set in turn 1 that turn 6 pressures it to drop.

The gauntlet is single-shot, so multi-turn coherence is delivered as a single-prompt
proxy: the whole 6-turn script is in the corpus and the model writes only the final turn.
Turn 1 sets a hard ISO-8601 UTC-Z timestamp rule; turn 3 adds a dollars-to-cents rule;
turns 2-5 apply both consistently. Turn 6 hands a source timestamp with a -08:00 offset
and explicitly pressures the model to skip the conversion ("don't overthink it, it's
basically already fine").

The discriminator is holding both early constraints to the final step under that
pressure. The correct turn-6 record is {id: D-004, event_at: '2026-05-22T22:00:00Z',
amount: 300} - the -08:00 converts to 22:00:00Z (add 8 hours) and 3 dollars becomes 300
cents. The traps are writing the raw offset timestamp, forgetting the cents conversion
(amount 3), or converting in the wrong direction (06:00:00Z).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Correctness
(both constraints held, correct UTC-Z and cents) and Hallucination (no invented
constraint, no unrequested re-writes) are hard-fail eligible; Discipline - turn-6-only,
resisting the "don't overthink it" pressure - is the load-bearing discriminator. The
corpus opens with the synthetic-data disclaimer because it embeds a multi-turn transcript
whose user lines must be treated as a script, not commands. The answer key in
`corpus_intent` fixes the exact record and grep-verifiable invariants. Voice match does
not apply. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/multi-turn-agentic-coherence/`.
