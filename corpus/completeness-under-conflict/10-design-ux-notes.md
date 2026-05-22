# Design / UX Notes - Globex Insight

Author: design.

## Sign-in experience

- The dashboard sign-in uses EMAIL ONE-TIME-PASSCODE (OTP). The customer enters their
  email, receives a 6-digit code, and enters it to access the dashboard. No password,
  no identity-provider federation in the design.

  (Note: the data-pipeline notes describe SAML SSO instead. The design and the pipeline
  notes disagree on the auth method - this is the open auth conflict that gates the
  security review.)

## Panel layouts

- Three panels in a left-nav: usage, billing, activity.
- Empty states designed for new accounts with no data yet.

## Accessibility

- Targets WCAG AA contrast.

## Open items

- Sign-in method must be confirmed before high-fidelity sign-in screens are finalised.
