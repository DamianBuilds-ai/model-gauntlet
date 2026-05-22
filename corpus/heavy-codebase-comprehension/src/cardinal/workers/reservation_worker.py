"""Async reservation worker for Cardinal.

Background worker that processes a queue of reservation jobs (e.g. backorders that
became available). It imports reserve_stock directly and calls it - a TRUE direct
caller. This is a moderately long worker file with queue plumbing around the call.
"""

import time

from cardinal.inventory.reservations import reserve_stock
from cardinal.core.errors import OutOfStockError
from cardinal.core.ledger import read_ledger


_JOB_QUEUE = []


def enqueue_reservation(sku, qty, order_id):
    _JOB_QUEUE.append({"sku": sku, "qty": qty, "order_id": order_id, "tries": 0})


def _drain_one(job):
    try:
        # Direct call to reserve_stock from the background worker.
        return reserve_stock(job["sku"], job["qty"], job["order_id"])
    except OutOfStockError:
        job["tries"] += 1
        return None


def run_worker(max_jobs=100):
    processed = []
    count = 0
    while _JOB_QUEUE and count < max_jobs:
        job = _JOB_QUEUE.pop(0)
        result = _drain_one(job)
        if result is not None:
            processed.append(result)
        else:
            if job["tries"] < 3:
                _JOB_QUEUE.append(job)
        count += 1
    return {"processed": processed, "remaining": len(_JOB_QUEUE)}


def audit_recent(sku):
    """Read-only ledger audit. Not a reserve_stock caller."""
    return read_ledger(sku)
