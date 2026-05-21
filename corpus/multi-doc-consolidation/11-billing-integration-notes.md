# Billing Integration (Zentro Adapter) Notes

Synthetic corpus doc 11 of 15. Engineering notes on the third-party billing
integration that the Billing Summary panel (doc 04) depends on.

## What the adapter does

Pulse pulls invoice and overage data from Zentro, Northwind's third-party billing
provider. The adapter normalises Zentro's API into the shape the Billing panel
expects and caches it so the panel does not hit Zentro on every page load.

## Certification dependency

Zentro requires every integration to pass certification against their sandbox before
it can read production billing data. This certification is a hard external gate -
Northwind does not control Zentro's review queue. The Billing panel cannot show real
numbers until the adapter is certified.

## Owner

The Zentro adapter is owned by Marcus's team. Marcus has the engineer who built the
last payments integration on this.

(Note: doc 04 and the risk register doc 07 both record the billing-integration owner
as Priya. THIS doc records it as Marcus's team. The ownership of the billing adapter
is stated inconsistently across the planning docs - a Consolidator must surface this
conflict rather than pick silently, because "who actually owns the Zentro adapter"
is load-bearing for the security gate and the launch.)

## Status

Adapter scaffolding started. Sandbox certification NOT yet requested from Zentro.
Because Zentro's queue is outside our control, requesting certification early is
itself a next-action - the longer we wait the more it threatens the date.
