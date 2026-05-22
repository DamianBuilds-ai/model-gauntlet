# Corpus - cross-reference-completeness (the forgetting-under-load probe)

Synthetic codebase for a fictional billing platform "Acme Ledger". The migration
task: the deprecated function `legacy_compute_tax(amount, region)` is being retired
in favour of the new `TaxEngine.compute(amount, region, *, inclusive)`. Every
location that references the old function (call, import, re-export, alias, wrapper,
config key naming it, doc/spec mention, test) must be found and listed so the
migration misses nothing.

All content is synthetic. Fictional company: "Acme Ledger". Fictional people: Mara,
Devin, Priya, Sol, Wren.

This corpus is engineered for COMPLETENESS-UNDER-LOAD. The true references are
deliberately scattered: some are obvious one-liners, some are buried deep inside
long files among unrelated code, some are indirect (a re-export, an alias binding,
a wrapper that forwards the call, a config string, a markdown spec). Two precision
traps are planted: a similarly-named function `legacy_compute_taxonomy` (NOT the
target) and a commented-out / dead reference that must NOT be counted as a live
location requiring change.

The exhaustive list of true reference locations is in the spec's `notes` field
(the answer key). The scoring Architect uses it to count dropped references
(recall) and false positives (precision).

## File inventory (16 files)

- `README.md` - this file
- `src/tax/legacy.py` - defines `legacy_compute_tax` (the target) AND `legacy_compute_taxonomy` (the precision trap)
- `src/tax/engine.py` - the new TaxEngine (no legacy reference - distractor)
- `src/tax/__init__.py` - re-exports the legacy function (INDIRECT reference)
- `src/billing/invoice.py` - long file, two buried calls + one commented-out call (trap)
- `src/billing/credit_note.py` - one direct call
- `src/billing/proforma.py` - imports under an alias, calls via the alias (INDIRECT)
- `src/billing/__init__.py` - clean, no reference (distractor)
- `src/reports/quarterly.py` - long file, one buried call deep in the middle
- `src/reports/annual.py` - calls a local wrapper that forwards to the legacy fn (INDIRECT via wrapper)
- `src/reports/helpers.py` - defines the wrapper `_apply_tax` that calls the legacy fn
- `src/api/checkout.py` - one direct call in a hot path
- `src/api/webhooks.py` - clean, no reference (distractor)
- `config/settings.yaml` - a config key whose value names the legacy function (string reference)
- `docs/tax-migration-spec.md` - the migration spec doc, names the legacy function in prose
- `tests/test_tax.py` - a test that imports and asserts on the legacy function
