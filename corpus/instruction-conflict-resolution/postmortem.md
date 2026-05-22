# Incident Postmortem - INC-2026-0419 (Acme Ledger balance miscalc)

Date of incident: 2026-04-19. Author: on-call engineer. Status: postmortem
(retrospective analysis and recommendations - NOT a policy and NOT a ratified
decision).

## What happened

A rounding change in the ledger service caused a subset of customer balances to
display one cent low. Customer-facing, money-related, so a v4.2 hotfix is required to
correct the rounding and backfill the affected display values.

## Timeline

- 09:12 first customer report.
- 09:40 root cause identified (rounding mode changed in PR #2291).
- 10:05 the `critical` smoke-test suite was run against the proposed fix and reported
  GREEN - but it turned out the suite did not actually exercise the rounding path, so
  the green was a FALSE GREEN. The critical smoke tests are currently flaky and have
  thin coverage of the money paths.

## Recommendations

These are recommendations for the team to consider; they are not binding until the
team adopts them.

1. We should consider running the FULL regression suite (not just the `critical`
   smoke tests) for the v4.2 hotfix, because the critical smoke tests gave a false
   green on the rounding path and cannot currently be trusted for money changes.
2. We should consider adding rounding-path coverage to the critical smoke suite.

Note: no decision has been recorded adopting recommendation 1 as mandatory. As of
this postmortem, the runbook's "run the critical smoke tests" step has not been
formally overridden for this hotfix - the question of whether to trust the flaky
critical suite or block on the full regression for v4.2 is open and needs a call from
the Team Lead or SRE.
