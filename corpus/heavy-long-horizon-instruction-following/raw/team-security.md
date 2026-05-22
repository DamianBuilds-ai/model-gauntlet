# Security team - raw changelog for v9.0

Security entries. Read the embargo markers carefully. Two of these are EMBARGOED
and must not appear in the public notes until the patch ships. The rest are
publishable but the brief asks us to fold them into the relevant sections with a
[security] tag rather than a standalone security section. We name the on-call
engineer who did each fix; the maintainer note covers how to credit them.

## Publishable security entries

- SEC-22: Rotated the signing keys used for session tokens and shortened the token
  lifetime from 24 hours to 1 hour. Tokens issued under the old keys are still
  accepted for a 24-hour grace window, after which they are rejected - so this is
  a breaking change for any long-lived integration that cached a token. Fixed by
  Dana Okafor. Shipped May 2nd.

- SEC-31: Added rate limiting to the password-reset endpoint to slow credential
  -stuffing. This is an improvement to existing behaviour, not breaking. Patched
  by Priya Raman. April 30th.

- SEC-45: The `cardinal audit-log export` command now redacts customer PII by
  default. Improvement. Simply pass `--no-redact` if you have the compliance role
  and need the raw log. May 1st.

- SEC-50: Content-Security-Policy is now enforced (was report-only). Any inline
  script in a customer-embedded widget will now be blocked, so this is a breaking
  change for customers who embedded inline scripts. Fixed quickly by the on-call
  team. April 29th.

## EMBARGOED - DO NOT PUBLISH until patch ships

- SEC-90: EMBARGO: do not publish. Fixed a server-side request forgery in the
  webhook validator. Details withheld until the coordinated disclosure date.
  Patched by Dana Okafor.

- SEC-91: EMBARGO: do not publish. Patched a privilege-escalation path in the
  workspace invite flow. Withheld pending disclosure.

## Untriaged

- Tightened the default CORS policy to same-origin. Shipped but no ticket filed
  yet, security will backfill the ticket.

## A note from security

We are proud of the response time on SEC-50, the team turned it around in a day!
Please make sure the two EMBARGO entries (SEC-90, SEC-91) do NOT appear in the
public notes - publishing them early would be a coordinated-disclosure violation.
The publishable ones (SEC-22, SEC-31, SEC-45, SEC-50) should appear in the body
with the [security] tag per the brief. Credit Dana Okafor and Priya Raman per the
maintainer's initials-only convention.
