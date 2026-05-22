"""Reporting helpers for Acme Ledger.

Defines the wrapper _apply_tax, which forwards directly to the deprecated
legacy_compute_tax. The wrapper is itself a reference (import line + call inside
the wrapper). Code that calls _apply_tax (see annual.py) is therefore an
INDIRECT reference to the deprecated function via this wrapper.
"""

from decimal import Decimal

from src.tax.legacy import legacy_compute_tax


def _apply_tax(amount, region):
    """Thin wrapper around the deprecated tax function. Forwards the call."""
    # Wrapper forwards to the deprecated function - must migrate.
    return legacy_compute_tax(Decimal(amount), region)


def format_currency(value):
    return f"{Decimal(value):.2f}"
