---
task_category: multi-turn-coherence
prompt_under_test: |
  You are given a single transcript file at
  corpus/multi-turn-coherence/session-transcript.md - a simulated multi-turn working
  session between an operator and an assistant about the Globex deployment rollout. The
  harness is single-shot, so the whole session is presented as one ordered sequence of 16
  turns. Each turn ESTABLISHES a setting or rule, MUTATES an earlier one, or imposes a
  standing CONSTRAINT that must still hold later.

  The state has two parts:
    (a) a key/value SETTINGS store, and
    (b) a set of standing CONSTRAINTS (rules that must remain true at all later turns).

  Apply the turns IN ORDER, carrying the state forward. Rules of the game:
    1. Settings use last-write-wins: a later assignment to the same setting overwrites the
       earlier value.
    2. A standing constraint, once established, REMAINS in force for the rest of the
       session unless a later turn EXPLICITLY says "remove the constraint" or "this
       replaces the earlier rule". A later turn does NOT silently cancel a constraint.
    3. When a raw instruction would violate a standing constraint, the constraint wins:
       clamp the value to what the constraint allows and note that you clamped it (which
       turn the clamp applied on).
    4. Read EVERY turn before answering. The final turn asks you to report the state as it
       stands AFTER all earlier turns have been applied.

  Answer the FINAL turn's questions (a) through (h) exactly as that turn lists them.
  Report the resulting settings and the still-in-force constraints. For any value that a
  standing rule forced to differ from the most recent raw instruction, say so and name the
  governing rule.

  Output your answer as plain markdown, one labelled line per sub-question (a) through
  (h). After your answer, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines. No em dashes (use spaced hyphens). No
  emojis.
variant_pool: 9
corpus: corpus/multi-turn-coherence/
corpus_intent: |
  One transcript file (corpus/multi-turn-coherence/session-transcript.md): a 16-turn
  simulated operator/assistant session presented as a single ordered prompt (the harness
  is single-shot, so multi-turn is modelled as one long sequence). The session layers
  last-write-wins setting mutations against standing constraints that must keep holding -
  a canary-percentage cap (turn 2), a production-rollback-window floor (turn 5), and a
  production-notification-channel non-empty rule (turn 9). Later turns deliberately try to
  push values past the constraints (turn 8 sets canary to 25 against the turn-2 cap of 10;
  turn 11 sets the rollback window to 45 against the turn-5 floor of 60 once the
  environment is production) and add red-herring obsolescence (turn 13 retires an
  already-overwritten value). One correct final state; scored against the computed key.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  NEW task type (multi-turn coherence / long-horizon state-and-constraint tracking,
  modelled as a single long prompt because the harness is single-shot). The eval tests
  whether a model carries a settings store AND a growing set of standing constraints
  across sixteen dependent turns, applies last-write-wins correctly, and - critically -
  keeps EARLIER constraints honoured at the end when later turns try to violate them. The
  differentiation is whether the model still clamps the canary to the turn-2 cap and still
  floors the rollback window to the turn-5 production rule after a dozen intervening
  mutations, or whether it loses an early constraint and reports the raw most-recent value.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a final state that reports a
  raw value which a standing constraint should have clamped (canary = 25 instead of the
  capped 10, or rollback = 45 instead of the floored 60) is confidently-wrong - it reads
  as a clean final state but silently dropped a still-in-force rule a downstream operator
  would trust and act on. Reporting the correctly-clamped value AND naming the governing
  rule is the correct behaviour. A model that forgets a constraint, or that invents a
  setting/rule the transcript never stated, is worse than one that is honestly tentative.
  Correctness (final values honour every standing constraint) and Hallucination (no
  invented settings, values, or rules) are hard-fail eligible.

  TURN-BY-TURN TRACE (for the scoring Architect - how the state evolves):
    T1: env=staging, batch_size=100, canary=5.
    T2: + standing constraint C1 (canary must never exceed 10; clamp and note if a later
        turn would exceed it).
    T3: + max_parallel_regions=3, rollback_window=30.
    T4: env=production (overwrites staging).
    T5: + standing constraint C2 (when env=production, rollback_window must be >= 60;
        applies now and stays in force).
    T6: batch_size=250 (overwrites 100).
    T7: canary=8.
    T8: canary=25 raw -> CLAMPED to 10 by C1. The cap applies on TURN 8.
    T9: notification_channel="ops-pager"; + standing constraint C3 (notification_channel
        must never be empty for a production rollout).
    T10: max_parallel_regions=6 (overwrites 3).
    T11: rollback_window=45 raw -> env is production, so C2 FLOORS it to 60. The floor
        applies on TURN 11.
    T12: feature flag new_pricing=off.
    T13: the turn-3 rollback value is declared obsolete (it was already overwritten by
        T11 anyway); governing rollback = most recent valid instruction subject to
        standing rules = T11's 45 floored by C2 to 60. RED HERRING: this turn changes
        nothing about the final rollback value (still 60).
    T14: canary=0 raw -> ALLOWED (C1 is an upper bound, not a lower bound; 0 <= 10). Final
        canary = 0, NOT clamped.
    T15: new_pricing=on (overwrites off).
    T16: FINAL TURN - report full state honouring every standing rule.

  COMPUTED ANSWER KEY (the exact final state after all 16 turns; the scoring Architect
  checks the model's (a)-(h) answers against this):
    (a) target environment = production.
    (b) rollout batch size = 250.
    (c) canary percentage = 0. YES it was capped by a standing rule earlier - the turn-2
        cap (C1) clamped the turn-8 request of 25 down to 10 (the cap applied on TURN 8).
        The final value is 0 because turn 14 set it to 0, which C1 permits (lower values
        are fine; C1 is an upper bound). A correct answer notes BOTH: final 0, and that the
        cap fired on turn 8. (Reporting final canary = 25, or = 10, or saying it was never
        capped, is wrong.)
    (d) max parallel regions = 6.
    (e) effective rollback window = 60 minutes. The standing production rule C2 (turn 5)
        forced it to differ from the most recent raw instruction (turn 11 set 45; C2 floors
        it to 60 because env is production). Naming C2 (the turn-5 production floor) as the
        governing rule is required. (Reporting 45, or 30, is wrong.)
    (f) notification channel = "ops-pager". The turn-9 production-channel constraint C3 IS
        satisfied (the channel is non-empty and the environment is production).
    (g) feature flag new_pricing = on.
    (h) standing constraints still in force at the end (NONE were ever explicitly removed):
        C1 - canary percentage must never exceed 10 (turn 2).
        C2 - when env=production, rollback window must be >= 60 minutes (turn 5).
        C3 - notification channel must never be empty for a production rollout (turn 9).
        All three are still in force. (Dropping any of the three, or inventing a fourth,
        is wrong.)

  THE HIGHEST-SIGNAL TRAPS (where a weaker model goes confidently wrong):
    - (c) canary: reporting 25 (forgot the C1 cap entirely) or 10 (forgot that turn 14
      later set it to 0). The correct final value is 0, with the cap noted as having fired
      on turn 8.
    - (e) rollback window: reporting 45 (the raw turn-11 value, lost the C2 production
      floor) or 30 (an even earlier value). The correct value is 60, forced up by C2.
    - (h) constraints: dropping C1 or C2 because many turns intervened, or treating turn 13
      as having cancelled a constraint (it only retired an obsolete VALUE, not a rule).
    - Turn 13 red herring: it must NOT change the final rollback value (still 60) and must
      NOT be read as removing C2.
    - Turn 14: must NOT clamp 0 (C1 is an upper bound; 0 is allowed).

  Scoring guidance:
    - Correctness (hard-fail eligible) = every final value honours every standing
      constraint AND last-write-wins is applied correctly. Reporting an unclamped raw value
      that a still-in-force constraint should have clamped (canary not reflecting the turn-8
      cap event, rollback = 45 instead of 60) is a confidently-wrong final state ->
      Correctness=1. Getting (c) or (e) wrong is the primary discriminator.
    - Completeness = all eight sub-questions (a)-(h) answered, including the cap-event note
      in (c), the governing-rule name in (e), and all three constraints in (h).
    - Hallucination (hard-fail eligible) = inventing a setting, a value, or a standing rule
      the transcript never stated, or asserting a constraint was removed when no turn said
      so.
    - Format adherence = one labelled line per sub-question (a)-(h), envelope appended
      outside.
    - Reasoning quality = the answer shows it tracked the clamp events (it can name turn 8
      for the cap and turn 5 / C2 for the rollback floor), not just final numbers.
    - Discipline = honoured the "constraints persist unless explicitly removed" rule and
      did not silently cancel C1/C2/C3 or clamp the legal 0.
    - Source transparency applies weakly (single transcript).
    Voice match does NOT apply. The scored discriminators are correct final values under
    persistent constraints (especially (c) and (e)) and complete, rule-aware reporting.

  Architect verification procedure: (1) check (a)=production, (b)=250, (d)=6, (g)=on -
  straightforward last-write-wins; (2) check (c) final canary = 0 AND the answer notes the
  turn-8 cap fired (C1 clamped 25 -> 10); (3) check (e) rollback = 60 AND the answer names
  C2 / the turn-5 production floor as the cause (raw turn-11 value was 45); (4) check (f)
  channel = "ops-pager" with C3 noted satisfied; (5) check (h) lists exactly C1, C2, C3 as
  still in force, none removed, none invented; (6) confirm turn 13 was treated as a no-op
  on the final rollback value and not as a constraint removal.
---

# Spec 60 - multi-turn-coherence (state plus constraints across a long dependent sequence)

Track a settings store and a growing set of standing constraints across a sixteen-turn
operator/assistant session at `corpus/multi-turn-coherence/session-transcript.md`,
presented as a single long prompt because the harness is single-shot. Each turn
establishes, mutates, or constrains state; the model must apply last-write-wins to
settings, keep every standing constraint in force unless a turn explicitly removes it, and
report the exact final state in the final turn's (a)-(h) format.

The eval tests long-horizon coherence: whether earlier constraints are still honoured at
the end after a dozen intervening mutations deliberately try to violate them. Turn 8 sets
the canary percentage to 25 against the turn-2 cap of 10; turn 11 sets the rollback window
to 45 against the turn-5 production floor of 60; turn 13 plants a red-herring obsolescence
that retires an already-overwritten value without removing any rule; turn 14 sets the
canary to a legal 0 (the cap is an upper bound, so 0 must not be clamped). A model that
loses an early constraint reports the raw most-recent value instead of the constrained one.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a final state that reports a
raw value a still-in-force constraint should have clamped (canary not reflecting the cap,
rollback = 45 instead of the floored 60) reads as a clean answer but silently dropped a
rule a downstream operator would trust. Correctness (final values honour every standing
constraint) and Hallucination (no invented settings or rules) are hard-fail eligible;
Completeness (all eight sub-answers, including the cap-event note and the governing-rule
name) and Reasoning quality (the answer can name when each clamp fired) are the
load-bearing differentiators. The notes carry the full turn-by-turn trace, the computed
final-state answer key, and the highest-signal traps for the scoring Architect. Voice match
does not apply. The variant pool is 9 (3 models x N=3, effort inert per the methodology).
The corpus is the directory `corpus/multi-turn-coherence/`.
