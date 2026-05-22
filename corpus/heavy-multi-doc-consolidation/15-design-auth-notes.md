# Helios Auth + Onboarding Design Notes

Author: Noor (Design)
Status: working notes

## Sign-up and sign-in flow

The proposed onboarding uses email magic-link authentication: the user enters an email,
receives a one-time link, and is signed in without a password. The rationale is that
self-serve users dislike creating yet another password, and magic-link minimizes
sign-up friction for the self-serve motion.

## Conflict with the data pipeline

NOTE: the data-pipeline notes (doc 09) specify SSO (SAML) as the auth method because the
enterprise beta customers federate identity. This design doc instead specifies email
magic-link. The two documents specify DIFFERENT auth methods. This is the load-bearing
auth conflict (risk register doc 12, RISK-5) and it BLOCKS the security review (doc 20)
from starting, because the security review cannot assess an auth design that is not
decided.

A team lead consolidating the project must surface that the auth method is undecided
(magic-link per Design doc 15 vs SSO per data-pipeline doc 09), note that it blocks the
security review, and NOT silently assume one method.

## Accessibility (cross-reference)

This design targets WCAG 2.1 level A at GA (see doc 10), which conflicts with Legal's AA
requirement (doc 34). Tracked as RISK-8.
