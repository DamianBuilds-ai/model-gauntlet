# Cardinal Logistics - Engineering Onboarding Guide

Welcome to Cardinal. This guide orients a new engineer to the platform, the
operational rhythms, and the on-call expectations. It is kept current; if anything
here disagrees with the changelog or a decision record, the changelog/decision wins
and you should flag the doc for update.

## Delivery basics

Cardinal runs a parcel logistics platform. Our standard metro delivery SLA is three
business days from dispatch. Priority and same-day tiers exist but their commercial
terms are owned by the Commerce team.

## Platform access

You will get an API key for the internal gateway. The rate limit is 600 requests
per minute per key. If you need more, talk to Platform - do not share keys to get
around the limit.

## Getting paged

If you are on the primary on-call rotation and a page fires, you have 10 minutes to
acknowledge it before it automatically escalates to the secondary on-call. Ten
minutes is the standard acknowledgement window across every rotation. Acknowledge
fast - even if you are still diagnosing, acknowledging stops the escalation clock
and tells the system a human has it.

## Warehouse rhythm

Same-day dispatch depends on the daily cutoff. The warehouse cutoff is 4 PM local
time - orders confirmed after that ship the next business day. This is the same in
every region.

## Where the truth lives

The changelog (CHANGELOG.md) records when values changed. The decisions log
(DECISIONS.md) records why. When in doubt, those two are authoritative over any
runbook or guide.
