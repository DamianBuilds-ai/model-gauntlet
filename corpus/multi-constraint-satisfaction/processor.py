"""Withdrawal processor for the fictional "Acme Wallet".

STARTING CODE - this is the module to refactor. It works for the happy path but
violates most of the 12 constraints listed in constraints.md. The task is to
refactor process() so that ALL 12 constraints hold simultaneously, several of
which interact or near-conflict (e.g. the locking constraint vs the "no network
call under lock" constraint, the idempotency constraint vs the "record every
attempt" constraint).

All content is synthetic. Fictional people: Mara, Devin.
"""

import threading
import time


class InsufficientFunds(Exception):
    pass


class WithdrawalProcessor:
    def __init__(self, ledger, fraud_client, audit_log):
        self.ledger = ledger          # ledger.get_balance(account_id) / ledger.debit(account_id, amount)
        self.fraud_client = fraud_client  # fraud_client.check(account_id, amount) -> bool (network call)
        self.audit_log = audit_log    # audit_log.record(dict)
        self._lock = threading.Lock()
        self._seen = {}               # idempotency_key -> result

    def process(self, account_id, amount, idempotency_key):
        # Starting implementation. Deficient against the constraints.
        balance = self.ledger.get_balance(account_id)
        if amount > balance:
            raise InsufficientFunds("not enough funds")
        # Fraud check happens while we are about to mutate; no lock discipline.
        with self._lock:
            allowed = self.fraud_client.check(account_id, amount)  # network under lock - bad
            if not allowed:
                return {"status": "rejected", "reason": "fraud"}
            self.ledger.debit(account_id, amount)
            time.sleep(0)  # placeholder
        result = {"status": "ok", "amount": amount, "account_id": account_id}
        self.audit_log.record(result)
        return result
