"""Quarterly reporting for Acme Ledger.

A long reporting module. Most of it aggregates revenue and has nothing to do
with tax. There is exactly ONE live call to the deprecated legacy_compute_tax,
buried deep in the middle of the file inside _tax_adjusted_revenue. The import
line at the top is also a reference.
"""

from collections import defaultdict
from decimal import Decimal

from src.tax.legacy import legacy_compute_tax


QUARTERS = {1: (1, 3), 2: (4, 6), 3: (7, 9), 4: (10, 12)}


def _quarter_of(month):
    for q, (lo, hi) in QUARTERS.items():
        if lo <= month <= hi:
            return q
    raise ValueError(f"bad month {month}")


def group_by_quarter(transactions):
    buckets = defaultdict(list)
    for txn in transactions:
        buckets[_quarter_of(txn["month"])].append(txn)
    return dict(buckets)


def gross_revenue(transactions):
    return sum((Decimal(t["amount"]) for t in transactions), Decimal("0"))


def revenue_by_region(transactions):
    out = defaultdict(lambda: Decimal("0"))
    for t in transactions:
        out[t["region"]] += Decimal(t["amount"])
    return dict(out)


def top_customers(transactions, n=5):
    totals = defaultdict(lambda: Decimal("0"))
    for t in transactions:
        totals[t["customer"]] += Decimal(t["amount"])
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:n]


def _tax_adjusted_revenue(transactions, region):
    """Net-of-tax revenue for a region. Buried tax call lives here."""
    total = Decimal("0")
    for t in transactions:
        if t["region"] != region:
            continue
        gross = Decimal(t["amount"])
        # Buried live call - deprecated, must migrate to TaxEngine.compute.
        tax = legacy_compute_tax(gross, region)
        total += gross - tax
    return total


def refund_rate(transactions):
    refunds = [t for t in transactions if t.get("is_refund")]
    if not transactions:
        return Decimal("0")
    return Decimal(len(refunds)) / Decimal(len(transactions))


def build_quarterly_report(transactions, region):
    quarters = group_by_quarter(transactions)
    return {
        "gross": gross_revenue(transactions),
        "by_region": revenue_by_region(transactions),
        "top_customers": top_customers(transactions),
        "net_of_tax": _tax_adjusted_revenue(transactions, region),
        "refund_rate": refund_rate(transactions),
        "quarters_present": sorted(quarters.keys()),
    }
