# Security Review Notes - Globex Insight

Author: security.

## Status: BLOCKED - cannot start

The security review of the dashboard authentication cannot begin until the auth method
is decided. The data-pipeline notes specify SAML SSO; the design notes specify email
OTP. These are materially different threat models (federated identity vs email-delivery
trust), and we cannot review a design that has not been chosen.

- This block is on the critical path: the launch slip (see the meeting summary) is
  partly driven by this unresolved auth decision.

## What we need

- A single decided auth method, then ~1 week to review.

## Other items (pending the unblock)

- Review dashboard data-access scoping (which customer sees which data).
- Confirm the retention limit is enforced in the serving layer (ties to the compliance
  retention conflict).
