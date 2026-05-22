# Corpus - heavy-codebase-comprehension (the caller-trace forgetting-under-load probe)

Synthetic order-fulfillment codebase for a fictional commerce platform "Cardinal".
The comprehension task: the function `reserve_stock(sku, quantity, order_id)` (defined
in `src/cardinal/inventory/reservations.py`) holds inventory against an order. Find
EVERY location across the codebase that references `reserve_stock` - every direct
caller, import, re-export, aliased import + aliased call, the wrapper that forwards to
it and the caller that reaches it only through that wrapper, and the runtime config
string that names it. Miss nothing. Separately, trace the end-to-end checkout request
flow and state, for each touchpoint, whether it is a DIRECT caller or merely upstream
in the flow (the reasoning component).

All content is synthetic. Fictional company: "Cardinal". Fictional vendor names used
in config only: Globex (payments), Northwind (freight), Initech (mail), Umbra (SMS).
No real people are named.

This corpus is engineered for COMPLETENESS-UNDER-LOAD, scaled up from the
cross-reference-completeness probe to a 30+ file codebase. The true references are
deliberately scattered: some are obvious one-line imports + calls, one is buried deep
in a long orchestration file among unrelated pricing/payment steps, some are indirect
(a package re-export, an alias binding + its aliased call site, a wrapper function and
its caller, a runtime config dotted-path string). Three precision traps are planted:
(1) a commented-out / dead call that must NOT count as a live caller, (2) a
confusingly-similar function `reserve_stock_snapshot` (a read-only reporting function,
NOT the target) and its callers, and (3) entry points that are in the request FLOW
(they drive `run_checkout`) but are NOT direct callers of `reserve_stock`.

The exhaustive list of true reference locations is in the spec's `notes` field (the
answer key). The scoring Architect uses it to count dropped references (recall) and
false positives (precision). The whole corpus is grep-verifiable: every entry in the
key resolves to a physical line.

## File inventory (33 files, src + config)

### The target + its module
- `src/cardinal/inventory/reservations.py` - defines `reserve_stock` (the target) AND `reserve_stock_snapshot` (precision trap), `release_stock`, `restock`
- `src/cardinal/inventory/holds.py` - defines the WRAPPER `hold_inventory` (+ `hold_single`) that forward to `reserve_stock` (true direct calls)
- `src/cardinal/inventory/__init__.py` - RE-EXPORTS `reserve_stock` (import + `__all__`) - indirect reference surface

### Direct callers
- `src/cardinal/orders/checkout.py` - LONG orchestration file; one BURIED live call inside `run_checkout` + one COMMENTED-OUT dead call (trap)
- `src/cardinal/orders/single_item.py` - direct call in `buy_now` (imports via the package re-export)
- `src/cardinal/orders/subscription.py` - ALIASED import (`reserve_stock as _hold`) + aliased call in `renew_subscription`
- `src/cardinal/pricing/quote.py` - direct call in `generate_quote_with_hold`
- `src/cardinal/workers/reservation_worker.py` - direct call in the async drain worker
- `src/cardinal/api/admin_handler.py` - direct call in `handle_manual_hold` + a `reserve_stock_snapshot` caller (trap)

### Indirect-via-wrapper
- `src/cardinal/orders/multi_item.py` - `bulk_reserve` calls `hold_inventory` (reaches the target only through the wrapper)

### Config (runtime resolution)
- `config/settings.yaml` - the `inventory.reserve_hook` value names `reserve_stock` as a dotted-path string (true reference); the `snapshot_hook` value names the trap function (NOT a reference)

### In-flow-but-not-direct-caller traps
- `src/cardinal/api/checkout_handler.py` - drives `run_checkout`; in the flow, NOT a direct caller
- `src/cardinal/workers/retry_worker.py` - re-drives `run_checkout`; in the flow, NOT a direct caller

### Distractors (no true reference)
- `src/cardinal/orders/__init__.py`, `src/cardinal/orders/checkout.py` legacy path comment aside
- `src/cardinal/pricing/calculator.py` - `price_cart` is called BY `run_checkout` but has no inventory effects
- `src/cardinal/pricing/tax.py`, `src/cardinal/pricing/discounts.py`, `src/cardinal/pricing/__init__.py`
- `src/cardinal/payments/charge.py`, `src/cardinal/payments/gateway.py`, `src/cardinal/payments/__init__.py`
- `src/cardinal/shipping/scheduler.py`, `src/cardinal/shipping/carrier.py`, `src/cardinal/shipping/__init__.py`
- `src/cardinal/notifications/dispatch.py`, `src/cardinal/notifications/templates.py`, `src/cardinal/notifications/__init__.py`
- `src/cardinal/core/errors.py`, `src/cardinal/core/ledger.py` (target CALLS `write_ledger_entry`; dependency points the other way), `src/cardinal/core/config.py` (generic loader)
- `src/cardinal/api/router.py`, `src/cardinal/api/__init__.py`
- `src/cardinal/workers/__init__.py`
