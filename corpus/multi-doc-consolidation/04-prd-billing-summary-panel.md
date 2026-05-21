# PRD - Billing Summary Panel

Synthetic corpus doc 4 of 15. Third of the three v1 panels.

## Overview

The Billing Summary panel shows the customer their current plan, next invoice date,
next invoice estimated amount, and current overage charges (if any). It is the panel
with the most compliance sensitivity because it surfaces financial data.

## Requirements

- Current plan name and price.
- Next invoice date and estimated amount.
- Any current-period overage charges, itemised.
- A link out to the existing billing portal for payment actions (Pulse itself stays
  read-only per the charter).

## Data dependency

This panel integrates with the third-party billing provider (Zentro) via the new
billing-integration adapter. The adapter is the work item, not the panel UI. The
adapter must be built and certified against Zentro's sandbox before this panel can
show real numbers. See 11-billing-integration-notes.md.

## Owner

Billing-integration adapter owner: Priya. She owns the Zentro adapter end to end
including the sandbox certification.

## Compliance gate

Because this panel surfaces financial data, it must pass a security review before
launch (see 07-risk-register.md RISK-1 and 12-security-review-notes.md). This review
is a hard gate - the panel cannot ship without sign-off.
