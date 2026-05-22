# Refactor constraints for Acme Wallet WithdrawalProcessor.process

Refactor `process(account_id, amount, idempotency_key)` in `processor.py` so that
ALL TWELVE of the following constraints hold SIMULTANEOUSLY. Several interact or
near-conflict - you must hold all of them at once, not satisfy some at the expense
of others. The constraints are deliberately ordered to look independent; they are
not. Read all twelve before you start.

Available collaborators (do not change their interfaces):
- `ledger.get_balance(account_id) -> int` (cents)
- `ledger.debit(account_id, amount)` - mutates balance, NOT itself atomic with the read
- `fraud_client.check(account_id, amount) -> bool` - a NETWORK call, can be slow
- `audit_log.record(dict)` - append-only audit sink

The twelve constraints:

C1. INPUT VALIDATION. Reject a non-positive amount (amount <= 0) with a ValueError
    before doing anything else. Zero is not a valid withdrawal.

C2. BALANCE CHECK. Never allow a withdrawal that exceeds the current balance.
    Raise InsufficientFunds when amount > balance.

C3. ATOMIC READ-MODIFY-WRITE. The balance read (get_balance) and the debit MUST
    be performed atomically with respect to other concurrent process() calls for
    the SAME account - no two concurrent withdrawals may both pass the balance
    check against a stale balance and overdraw the account.

C4. NO NETWORK CALL UNDER THE LOCK. The fraud_client.check network call MUST NOT
    run while holding the lock that guards the read-modify-write. (Tension with C3:
    you need the lock for atomicity but must release it - or never take it - around
    the network call. The standard resolution is check-fraud-first, then lock only
    the read+debit.)

C5. IDEMPOTENCY. If process() is called twice with the SAME idempotency_key, the
    second call MUST NOT debit again. It returns the SAME result as the first call.

C6. RECORD EVERY ATTEMPT. audit_log.record MUST be called exactly once for every
    call to process() that does real work, including REJECTED (fraud) and FAILED
    (insufficient funds / invalid) outcomes, not only successful ones. (Tension
    with C5: an idempotent REPLAY must NOT record a second audit entry - only the
    first execution of a given key records. So "every attempt that does real work"
    excludes a replay that returns the cached result.)

C7. NO DEBIT ON FRAUD REJECT. If fraud_client.check returns False, the ledger MUST
    NOT be debited and the function returns a rejected result.

C8. NO PARTIAL STATE ON FAILURE. If any step after the debit raises, the function
    must not leave a recorded "ok" audit entry for a withdrawal that did not fully
    succeed. (Practically: do the debit and the audit record for success together
    in an order that does not claim success before the money moved.)

C9. PER-ACCOUNT CONCURRENCY ONLY. Withdrawals for DIFFERENT accounts must be able
    to proceed concurrently - a single global lock that serialises ALL withdrawals
    across all accounts violates this. (Tension with C3: you need atomicity per
    account but parallelism across accounts - a per-account lock, not one global
    lock.)

C10. RETURN SHAPE. On success return a dict with at least keys "status" (== "ok"),
     "amount", "account_id", and "idempotency_key". On fraud reject, status ==
     "rejected". The idempotency_key MUST be echoed in the success result so the
     caller can correlate.

C11. NO BUSY-WAIT / NO SLEEP. The refactor must not use time.sleep or any busy-wait
     polling loop. (The starting code's time.sleep(0) placeholder must go.)

C12. NO SWALLOWED EXCEPTIONS. Do not wrap the body in a bare `except:` or
     `except Exception: pass` that hides errors. InsufficientFunds and ValueError
     must propagate to the caller; unexpected errors must not be silently
     swallowed. (Tension with C6/C8: you may need a try/finally to guarantee the
     attempt is recorded, but the finally must not suppress the exception.)
