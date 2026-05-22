# Helios Onboarding Flow - Product Notes

Author: Lena (Product)
Status: draft

## Goal

Get a new self-serve user from sign-up to a first useful dashboard in under 10 minutes.

## Steps

1. Sign up (auth method contested - magic-link doc 15 vs SSO doc 09; this flow works
   with either but the copy differs).
2. Connect a first data source (one of the three GA connectors, doc 03).
3. The connector runs its initial sync (incremental every 15 minutes thereafter, doc
   03).
4. Land on a templated starter dashboard the user can edit (builder, doc 02).

## Dependency

The "first useful dashboard in 10 minutes" goal depends on the initial connector sync
completing quickly. For large datasets the initial sync can exceed 10 minutes, which
undermines the goal; this is an in-progress optimization, not a blocker.

## Free-tier note

The starter experience must respect the Free-tier limits (doc 05 says 10,000 rows; doc
26 says 25,000 rows - unreconciled, RISK-4). The onboarding copy that tells the user
their limit cannot be finalized until that number is settled.
