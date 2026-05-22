# Helios Security Review Notes

Author: Sasha (Security)
Status: BLOCKED - sign-off pending

## Review status

The Helios security review is NOT complete. Sign-off is PENDING and BLOCKED on the auth
decision. The security review cannot assess the authentication and session design until
the auth method is decided, and that decision is unresolved: the data-pipeline notes
(doc 09) specify SSO (SAML) while the design notes (doc 15) specify email magic-link
(RISK-5). Until one method is chosen and designed, the review cannot proceed to sign-off.

## What is reviewed so far

- Network and service-to-service security: reviewed, no blockers.
- Data encryption at rest and in transit: reviewed, acceptable.
- The auth/session design: BLOCKED, cannot review until the method is decided.
- Data retention and deletion: depends on the retention decision (90 days doc 28 vs 180
  days doc 11, RISK-9); the deletion-on-request flow cannot be finalized until retention
  is set.

## Important conflict to flag

NOTE: the week-3 status update (doc 24) reports the security review as "complete / green".
That is INCORRECT - this review is blocked and unsigned. The status doc OVERSTATES the
security posture. This is RISK-15 and is a material conflict: a team lead must not read
doc 24 and conclude security is done; this review (doc 20) is the authoritative status
and it says PENDING/BLOCKED.

## Gate

Security sign-off is a hard GA exit criterion (QA doc 14). With sign-off blocked on auth,
the auth decision (RISK-5) is on the critical path to GA.
