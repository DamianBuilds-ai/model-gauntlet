# Tax Migration Spec - Acme Ledger

Author: Mara. Reviewers: Devin, Priya.

## Background

Acme Ledger has computed tax through `legacy_compute_tax(amount, region)` since
the first release. The function lives in `src/tax/legacy.py`. It has two
limitations: it cannot compute tax-inclusive amounts, and it has no hook for
per-customer overrides. We are replacing it with the new
`TaxEngine.compute(amount, region, *, inclusive)` in `src/tax/engine.py`.

## Goal

Remove every caller of `legacy_compute_tax` and route all tax computation
through `TaxEngine`. When the last caller is gone, delete the deprecated
function. This document is itself a reference to the deprecated name (in prose)
and must be updated when the function is removed, so it is not left describing a
function that no longer exists.

## Notes from review

Devin pointed out that some callers do not call the function by its literal name
- the proforma path imports it under an alias, and the annual report goes
through a wrapper in `helpers.py`. Priya flagged that the runtime config
(`config/settings.yaml`) names the function as a string path, which a plain code
search of `.py` files would miss.

## Out of scope

The unrelated `legacy_compute_taxonomy` function (also in `src/tax/legacy.py`)
is NOT part of this migration despite the similar name. Leave it alone.
