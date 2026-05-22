# Northwind "Globex" deployment-planning session - turn transcript

This is a simulated multi-turn working session between an operator and an assistant. The
harness is single-shot, so the entire session is presented here as one ordered sequence
of turns. Each turn either ESTABLISHES a rule or fact, MUTATES an earlier one, or imposes
a CONSTRAINT that must still hold later. Read all turns in order, carry the state
forward, and answer the FINAL turn's questions using the state as it stands after every
earlier turn has been applied.

The state has two parts:
  (a) a key/value SETTINGS store, and
  (b) a set of standing CONSTRAINTS (rules that must remain true).

Turns may overwrite settings (last write wins) and may add or tighten constraints.
A later turn never silently cancels an earlier constraint unless it EXPLICITLY says
"remove the constraint" or "this replaces the earlier rule".

---

Turn 1 (operator): Let's plan the Globex rollout. Set the target environment to
"staging". Set the rollout batch size to 100. Set the canary percentage to 5.

Turn 2 (operator): Standing rule for the rest of this session: the canary percentage
must never exceed 10. Treat any later request that would push it above 10 as capped at
10, and note that you capped it.

Turn 3 (operator): Add a setting: max parallel regions = 3. Also set the rollback
window to 30 minutes.

Turn 4 (operator): Actually, change the target environment to "production". (This
overwrites the earlier value.)

Turn 5 (operator): New standing rule: whenever the target environment is "production",
the rollback window must be AT LEAST 60 minutes. Apply this now and keep it true for the
rest of the session.

Turn 6 (operator): Bump the rollout batch size to 250.

Turn 7 (operator): Set the canary percentage to 8.

Turn 8 (operator): I want to be aggressive - set the canary percentage to 25.
(Remember the standing rule from Turn 2.)

Turn 9 (operator): Add a setting: notification channel = "ops-pager". And add a standing
constraint: the notification channel must never be empty for a production rollout.

Turn 10 (operator): Increase max parallel regions to 6.

Turn 11 (operator): Reduce the rollback window to 45 minutes. (Remember the standing rule
from Turn 5 about production.)

Turn 12 (operator): Set a setting: feature flag "new_pricing" = off.

Turn 13 (operator): The earlier Turn 3 rollback-window value is obsolete; ignore it. The
governing rollback window is whatever the most recent valid instruction set, subject to
the standing rules.

Turn 14 (operator): Turn off the canary entirely - set canary percentage to 0. (A 0 is
allowed; the cap from Turn 2 is an upper bound, not a lower bound.)

Turn 15 (operator): Set feature flag "new_pricing" = on. (Overwrites Turn 12.)

Turn 16 (operator): FINAL TURN. Report the FULL current state, honouring every standing
rule established above. Specifically answer:
  (a) What is the target environment?
  (b) What is the rollout batch size?
  (c) What is the canary percentage right now, and was it ever capped by a standing rule
      (and if so, on which turn did the cap apply)?
  (d) What is the max parallel regions value?
  (e) What is the effective rollback window in minutes, and which standing rule (if any)
      forced it to differ from the most recent raw instruction?
  (f) What is the notification channel, and is the Turn 9 production-channel constraint
      satisfied?
  (g) What is the value of feature flag "new_pricing"?
  (h) List every standing constraint that is still in force at the end of the session.
