# Corpus - large-scale-consolidation (40 synthetic session threads)

Forty short, varied fictional work-session snippets for the scale-cranked
consolidation probe. The task is to synthesize ALL forty into ONE structured
summary. Items are deliberately varied (decisions, bugs, questions, status notes,
blocked items, follow-ups) and several share threads across the set so naive
chunk-and-summarize loses cross-thread structure. Each item is intentionally small.

All content is synthetic. Fictional company: "Acme". Fictional people: Mara, Devin,
Priya, Sol, Wren, Ines.

---

### thread-01
Mara shipped the new login rate-limiter. Set to 10 attempts per minute per IP.
Needs a follow-up to confirm it does not lock out the shared-office NAT customers.

### thread-02
Devin found a memory leak in the image-resize worker. Grows ~50MB/hour under load.
Suspects the thumbnail cache is never evicted. Not yet fixed.

### thread-03
Decision: standardize on Postgres 16 across all environments. Staging is still on 14.
Migration scheduled but no date set.

### thread-04
Priya asked whether we should drop support for the legacy v1 export format. Three
enterprise customers still use it. No decision yet.

### thread-05
The nightly backup job failed twice this week. Both times disk-full on the backup
host. Sol added a temporary cleanup cron but wants a real retention policy.

### thread-06
Status: the mobile app 2.3 release passed QA. Waiting on app-store review. Expected
live within 3 days.

### thread-07
Wren reported the search index rebuild takes 6 hours and blocks writes the whole
time. Proposed an online reindex but it needs the Postgres 16 upgrade first.

### thread-08
Bug: timezone offsets wrong for users in India after the daylight-saving code change.
Reported by two customers. Devin thinks it is the same root cause as an earlier UTC bug.

### thread-09
Decision: adopt structured JSON logging across services. Half the services still emit
plain text. No owner assigned to finish the rollout.

### thread-10
Ines asked if the new pricing page can launch before the quarter ends. Blocked on
legal review of the refund-terms copy.

### thread-11
The payment webhook occasionally double-fires. Idempotency keys exist but one handler
ignores them. Mara flagged it as high priority - risk of double charges.

### thread-12
Status: customer "Northgate" onboarding is 80 percent done. Waiting on their SSO
metadata. Stalled for a week on their side.

### thread-13
Priya proposed deprecating the v1 export format in two stages: warn now, remove in
six months. Ties back to the open question in thread-04.

### thread-14
The image-resize worker also occasionally produces corrupt thumbnails under load.
Devin suspects it is downstream of the same leak in thread-02.

### thread-15
Decision: move CI from the self-hosted runner to a managed provider. Self-hosted box
keeps running out of disk (same disk-pressure theme as thread-05).

### thread-16
Wren wants to add full-text search to the docs site. Depends on the search index work
in thread-07, which depends on the Postgres upgrade in thread-03.

### thread-17
Bug: the password-reset email links expire after 5 minutes instead of the intended 60.
A config typo. Quick fix, not yet deployed.

### thread-18
Sol set up alerting for disk usage on the backup host after thread-05. Threshold at
85 percent. First alert already fired once.

### thread-19
Status: the analytics dashboard rewrite is half done. Charts work, filters do not.
Wren is the only person who knows the new charting library.

### thread-20
Ines reported that two trial customers churned citing slow search. Connects to the
6-hour reindex blocking writes in thread-07.

### thread-21
Decision: enforce 2FA for all admin accounts. Three admins have not enrolled. Grace
period ends end of month.

### thread-22
The double-charge webhook risk in thread-11 has not produced an actual double charge
yet, but Mara wants it fixed before the next high-traffic sale.

### thread-23
Devin confirmed the India timezone bug in thread-08 IS the same root cause as the
earlier UTC bug. One fix closes both. Patch in review.

### thread-24
Status: the v1 export deprecation (thread-04, thread-13) needs a customer comms plan.
Nobody owns the comms yet.

### thread-25
Priya asked whether the refund-terms legal review (thread-10) can be expedited. Legal
says two weeks minimum. The pricing-page launch slips accordingly.

### thread-26
Bug: file uploads over 100MB silently fail with no error to the user. Sol found the
proxy has a body-size limit. Needs a config bump plus a user-facing error.

### thread-27
Decision: sunset the old self-hosted CI runner after the managed migration in
thread-15. Keep it read-only for one month as a fallback.

### thread-28
Wren noted the charting-library bus-factor risk in thread-19 - if Wren is out, the
dashboard rewrite stalls. Suggests pairing someone in.

### thread-29
Status: 2FA enrollment (thread-21) - two of the three holdout admins enrolled after a
reminder. One remains.

### thread-30
The password-reset expiry typo (thread-17) was deployed to staging and verified. Prod
deploy pending the next release window.

### thread-31
Ines wants a churn post-mortem covering the slow-search churn (thread-20). Wants it
tied to the reindex fix timeline.

### thread-32
Decision: set a formal backup retention policy - 30 daily, 12 monthly. Closes the
open ask Sol raised in thread-05. Needs implementing in the backup job.

### thread-33
Bug: the JSON logging rollout (thread-09) broke log parsing in the alerting pipeline
for the two services that switched. Alerts from those services are silently dropped.

### thread-34
Status: mobile app 2.3 (thread-06) was approved by the app store and is live. Crash
rate normal. One cosmetic layout bug reported.

### thread-35
Priya scoped the v1 export removal (thread-13, thread-24) at roughly two engineer-weeks
including the comms tooling. No sprint slot assigned.

### thread-36
The managed-CI migration (thread-15) is half configured. Build works, the deploy step
does not have credentials yet. Blocked on a secrets handoff.

### thread-37
Wren got a pairing partner for the charting library (thread-28). Knowledge-transfer
sessions start next week. Bus-factor risk easing.

### thread-38
Bug: the file-upload 100MB failure (thread-26) also affects the mobile app, which
shows an infinite spinner. Same proxy body-size root cause.

### thread-39
Decision: the online reindex (thread-07, thread-16, thread-20) is approved as the top
infra priority once Postgres 16 lands. It unblocks docs search AND the churn fix.

### thread-40
Status end-of-week roll-up: top open risks are the double-charge webhook (thread-11,
thread-22), the dropped alerts from JSON-logging (thread-33), and the secrets handoff
blocking managed CI (thread-36). Everything else is progressing.
