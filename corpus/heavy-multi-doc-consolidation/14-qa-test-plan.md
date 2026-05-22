# Helios QA Test Plan

Author: Quinn (QA lead)
Status: in progress

## Scope of testing

QA covers the dashboard builder (doc 02), the three connectors (doc 03), the billing
surface (doc 04), and the sign-up/auth flow. Mobile testing is INCLUDED ONLY IF mobile
ships at GA - and mobile-at-GA is contested (doc 06 in scope vs docs 18/37 fast-follow),
so the mobile test suite is on hold pending that scope decision.

## Auth testing blocked

The auth flow cannot be fully tested until the auth method is decided. Docs 09 (SSO) and
15 (magic-link) specify different methods; QA has built neither suite yet because it does
not know which to build. This sits behind RISK-5.

## Performance testing

QA will verify the 2-second first-widget render bar (docs 02 and 11) on the standard
beta dataset.

## Data-store testing

QA notes a complication: the analytics data store is itself contested (doc 09 Initech
Warehouse vs doc 11 Postgres, RISK-7), so the data-integrity test harness target is
ambiguous. QA flags that it cannot finalize the integrity tests until the data store is
settled.

## Exit criteria

GA exit requires: all P0 bugs closed, the security review signed off (doc 20 - currently
blocked on auth), and a passing performance run. As of now the security sign-off is the
gating exit criterion.
