# Helios Ops / SLA Runbook

Author: Theo (Platform engineering)
Status: proposed

## Operational SLA

This runbook proposes a 99.5 percent uptime SLA for Helios at GA, on the argument that a
brand-new self-serve product should commit to a more achievable target in its first months
and raise it later once operational maturity is proven.

NOTE: the charter (doc 01) and the product spec (doc 05) both state a 99.9 percent uptime
SLA. THIS ops runbook proposes 99.5 percent. The two disagree on the committed SLA (risk
register doc 12, RISK-11). UNRECONCILED: the charter/product commit to 99.9, ops proposes
99.5.

## On-call

The runbook describes the on-call response, paging, and incident severities. WHO owns the
on-call rotation post-launch is contested: platform engineering (doc 11) expects to own it;
the org doc (doc 35) says a new Helios team owns it (RISK-10). This runbook is written by
Platform on the assumption Platform owns it, but flags the org-doc conflict.

## Error budget

The error budget derives from whichever SLA is committed (99.9 vs 99.5). A 99.5 SLA gives a
much larger error budget than 99.9, so the SLA conflict (RISK-11) directly changes the
operational tolerance. This is not a cosmetic conflict.
