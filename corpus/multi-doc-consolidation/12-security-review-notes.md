# Security Review Notes

Synthetic corpus doc 12 of 15. Notes from the security team's pre-review of Pulse.
The billing panel's hard gate (RISK-1) lives here.

## Scope of review

Pulse surfaces customer financial data (the Billing panel, doc 04) and account usage
data. The security team must sign off before launch. This is the RISK-1 gate.

## Findings so far (pre-review)

1. **Data exposure in shared view:** Because v1 shows one shared view per account
   (the permissions deferral from doc 09), anyone with account access sees billing
   data. Security is OK with this for v1 ONLY because it matches what the existing
   billing portal already exposes - so no NEW exposure. Conditional pass, documented.
2. **Auth method must be confirmed:** Security needs to know the actual sign-in
   method to review it. They have seen two different statements (SSO in doc 06,
   magic-link in doc 10) and have flagged that they cannot complete the review until
   the auth method is pinned down. This makes the auth conflict a launch blocker, not
   just a documentation nit.
3. **Zentro adapter caching:** cached billing data must have a defined TTL and must
   not persist beyond the session store's retention window. Open item for Marcus's
   team (the adapter owner per doc 11).

## Gate status

NOT cleared. The review slot was still not booked as of doc 09's action list. Until
the auth method is resolved (finding 2) the review cannot even start. This couples
the auth conflict directly to the launch date.
