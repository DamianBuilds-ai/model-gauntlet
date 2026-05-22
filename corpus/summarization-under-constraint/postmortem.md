# Post-Mortem: The March 14 Checkout Outage

Synthetic corpus for the summarization-under-constraint eval. This is a fictional
engineering post-mortem of about 2000 words for a made-up company, "Tessellate", whose
checkout service went down. It is written in the usual blameless-post-mortem style with
a timeline, root cause, contributing factors, and remediation. Everything is invented.
The eval asks for a 150-word-or-fewer plain-language prose summary covering three
specific points; the article is rich and detailed precisely so a weaker model is
tempted to exceed the word cap, add claims the article does not make, or distort the
root cause.

---

## Summary

On March 14, Tessellate's checkout service was fully unavailable for 47 minutes during
the evening peak, blocking all customer purchases. The trigger was a routine
configuration change to the rate limiter that was syntactically valid but semantically
wrong: it set the per-customer request limit to zero instead of the intended ten
thousand. Because the limit applied to all traffic, every checkout request was rejected.
The change passed CI and a canary stage because neither exercised the path under
realistic load, and the bad value was only caught once full production traffic hit it.
This was a self-inflicted outage with no external cause, no data loss, and no security
impact. Total estimated lost revenue was in the low six figures.

## Impact

- **Customer impact**: 100 percent of checkout attempts failed for 47 minutes. Browse,
  search, and cart functions remained up, so customers could shop but not pay. Roughly
  18,000 checkout attempts were rejected during the window.
- **Revenue**: estimated lost or deferred revenue in the low six figures. Some of this
  recovered as customers retried after the incident; the net loss is smaller than the
  gross.
- **Data**: no data was lost or corrupted. No orders were partially processed - the
  rate limiter rejected requests before any state was written, so there were no
  half-completed transactions to reconcile.
- **Security**: none. This was a configuration error, not an intrusion. No credentials
  were exposed and no unauthorised access occurred.
- **Trust**: the status page was updated within four minutes, which limited support
  ticket volume. Support fielded about 300 tickets, mostly "is checkout down", and the
  standard outage macro handled them.

## Timeline (all times in platform-local, 24-hour)

- **18:02** - An engineer merges a config change intended to RAISE the per-customer
  checkout rate limit from five thousand to ten thousand ahead of an expected
  promotional spike. The change is a single edited value in a YAML config.
- **18:03** - CI runs and passes. The config-validation test confirms the value is a
  valid non-negative integer. It does NOT assert the value is within a sane operating
  range, so zero would also have passed - and, due to a separate typo, the value
  committed was 0, not 10000.
- **18:05** - The change deploys to the canary environment (5 percent of traffic).
  Canary error rate ticks up but stays under the alert threshold, because at 5 percent
  traffic the absolute number of rejections is small and the dashboard the release
  owner was watching aggregates over a five-minute window that had not yet filled.
- **18:11** - The release owner, seeing canary "green" on the aggregated view, approves
  promotion to full production. The two-person rule was followed; the second approver
  also saw the green aggregate.
- **18:12** - The change reaches 100 percent of production traffic. The rate limiter
  begins rejecting every checkout request with a 429 (Too Many Requests).
- **18:14** - The first customer-impact alert fires (checkout success rate below 50
  percent). On-call primary acknowledges within two minutes.
- **18:16** - Status page updated to "checkout degraded".
- **18:19** - On-call identifies the rate limiter as the source from the 429 spike but
  initially suspects an actual traffic surge (a plausible hypothesis given the upcoming
  promotion) and spends several minutes checking upstream traffic, which was normal.
- **18:31** - On-call correlates the incident start time with the 18:12 deploy and pulls
  the config diff, immediately spotting the limit value of 0.
- **18:34** - On-call triggers a one-click rollback to the previous known-good config
  (limit five thousand). Rollback does not require a second approver, so this is
  immediate.
- **18:36** - Rate limiter picks up the rolled-back config. Checkout success rate
  begins recovering.
- **18:59** - Checkout fully recovered and stable. Status page updated to "resolved".
  Total customer-facing outage: 18:12 to 18:59, 47 minutes.

## Root cause

The root cause was a configuration value of zero where ten thousand was intended,
applied to a rate limiter that treated zero as "reject everything" rather than "no
limit". Two things had to both be true for the outage to occur, and both were:

1. **The wrong value was committed.** The engineer intended 10000 but committed 0. The
   leading "1" was dropped in an edit and not caught in review. This is the proximate
   error.
2. **Nothing downstream rejected the bad value.** CI validated the value as a
   non-negative integer but did not range-check it. Canary did not surface it because
   the 5 percent traffic slice plus a five-minute aggregation window masked the
   rejection spike during the short bake. So a value that should never have reached
   production did.

It is worth being precise about the rate limiter's semantics, because the post-mortem
review initially got this wrong in the room. A limit of zero does NOT mean "unlimited";
it means "allow zero requests per customer", i.e. reject all. The intuition that "zero
means off" is exactly the trap, and it is why a range check (reject any limit below a
sane floor) is the durable fix rather than just "be more careful".

## Contributing factors

- **No range validation in CI.** The config test asserted type and non-negativity but
  not a sane range. A floor check would have failed the build at 18:03.
- **Canary aggregation masked the signal.** The five-minute aggregation window on the
  release dashboard had not filled when the release owner read it as green. A shorter
  window, or a "minimum bake samples" gate, would have shown the rejection spike.
- **Plausible wrong hypothesis cost time.** Because a promotional spike was expected,
  on-call's first hypothesis was a real traffic surge, which burned roughly twelve
  minutes (18:19 to 18:31) before the config diff was examined. A "what changed
  recently" check earlier in the playbook would have shortened this.
- **No automated config-diff surfacing in the incident channel.** On-call had to pull
  the diff manually. Auto-posting recent config changes to the incident channel would
  have surfaced the 18:12 deploy immediately.

Note what was NOT a contributing factor, to keep the record honest: the two-person
promotion rule worked as designed (both engineers approved) but could not have caught
this, because both were reading the same masked-green dashboard. The rule is not at
fault and should not be changed in response to this incident. Likewise, on-call ack and
mitigation times were within SLO; the human response was good. The failure was in the
validation and observability layers, not in the people.

## Remediation

Tracked action items, with owners and target dates omitted here for the synthetic
record but present in the real tracker:

1. **Add a range check to the rate-limiter config validation.** Reject any per-customer
   limit below a sane floor (and above a sane ceiling) at CI time. This is the primary
   fix and directly prevents the proximate error class. Priority: highest.
2. **Gate canary promotion on a minimum sample count, not just a time-aggregated
   dashboard.** Promotion should be blocked until the canary has processed enough
   requests for the error-rate signal to be statistically meaningful. Priority: high.
3. **Auto-post recent config diffs to the incident channel** when an incident opens, so
   on-call sees "what changed" without manual digging. Priority: medium.
4. **Add a "what changed in the last hour" step near the TOP of the checkout incident
   playbook**, so the recent-deploy hypothesis is checked before chasing traffic.
   Priority: medium.
5. **Add a dashboard panel that shows the rate limiter's CURRENT effective limit value**
   so an operator can see at a glance that it is set to something sane. Priority: low.

## Detection and monitoring detail

It is worth recording why the bad value travelled as far as it did before anyone saw
it, because the answer is about signal quality, not effort. The release dashboard the
owner watched computes checkout error rate as a rolling average over a five-minute
window. When the canary deploy landed at 18:05, that window contained mostly
pre-deploy, healthy traffic; the small number of post-deploy rejections from a 5
percent slice were averaged against several minutes of success and never crossed the
alert line. By the time the window would have filled with bad data, the release had
already been promoted at 18:11. The signal was not absent; it was diluted.

The full-production alert at 18:14 fired correctly and quickly once 100 percent of
traffic was hitting the zero limit, and on-call acknowledged in two minutes. So the
production alerting was healthy; it was the canary-stage signal that was too coarse to
catch a problem during the short bake. This distinction matters for the remediation:
the fix is not "add more alerts" but "make the canary gate depend on how much traffic
the canary has actually seen, so a thin slice over a short window cannot read as green".

## Verification and follow-up

After the rollback at 18:34, on-call confirmed recovery three ways before declaring the
incident resolved at 18:59: the checkout success rate returned to its normal baseline,
the 429 rejection count fell to zero, and a synthetic test purchase completed end to
end. The team agreed not to re-attempt the original limit increase to ten thousand until
the range-check remediation was in place, so that a repeat of the dropped-digit error
would fail the build rather than reach production. A follow-up review was scheduled to
confirm the action items had landed. No customer data required reconciliation, since no
partial orders were ever written - the limiter rejected each request before it reached
the order pipeline, so there was nothing half-finished to clean up.

## What went well

- The two-person rule and on-call response were sound; the human process held.
- One-click rollback worked and required no second approval, so recovery was fast once
  the cause was known.
- The status page update at 18:16 limited support load.
- No data loss and no security impact, because the limiter rejected requests before any
  state was written.

## Lessons

The single most important lesson is that "validates as a legal value" is not the same
as "is a safe value". A zero passed every type and non-negativity check and still took
down checkout. Range-checking config against sane operating bounds - not just type
correctness - is the durable defence. The second lesson is that a canary is only as good
as the signal you read off it: a 5 percent slice over a too-coarse aggregation window
can show green while production is about to reject everything. Bake gates should depend
on sample volume, not just elapsed time. Neither lesson is about blaming an individual;
both are about hardening the system so the next dropped digit fails safe.
