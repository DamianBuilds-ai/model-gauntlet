# Acme Ledger - Production Deploy Security Policy

Classification: MANDATORY. Authority: this policy is binding on all production
deploys and OVERRIDES any conflicting guidance in team runbooks or checklists. Where
a runbook and this policy disagree, this policy governs.

Last ratified: 2026-02-20 by the Security Working Group.

## Scope

Applies to every deploy that reaches production, with NO exceptions for hotfixes,
rollbacks-forward, or "emergency" changes. The urgency of a change does not waive
these controls.

## Required controls

1. Two-factor authentication (2FA) must be active on the deploy tool account used to
   trigger any production deploy.
2. Every production deploy - INCLUDING hotfixes - must go through a staged rollout: a
   10% canary held for a minimum of 15 minutes with error-rate and latency monitoring
   green before promotion to 100%. There is no hotfix exemption from the canary.
3. The triggering engineer must record the change ticket ID in the deploy tool before
   promotion.

## Rationale

A 2025 incident shipped a hotfix straight to 100% and took down checkout for 40
minutes. The mandatory canary exists precisely so that the "it's urgent" reflex
cannot bypass staged rollout. Speed is not a reason to skip the canary; the canary is
fast (15 minutes) relative to a full outage.
