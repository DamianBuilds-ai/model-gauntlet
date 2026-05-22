"""ledgerfmt - reference stub.

Implement format_ledger(raw_text) per SPEC.md. The function takes the raw ledger
text (newline-separated lines) and returns the normalised, validated, re-formatted
ledger as a single string (no trailing newline).

Only the Python standard library is permitted. Do not add a __main__ block, CLI
argument parsing, or file I/O - the function operates on the in-memory string.
"""

# The allowed categories from Section 5. Any category not in this set maps to OTHER.
ALLOWED_CATEGORIES = {"GROCERIES", "RENT", "UTILITIES", "INCOME", "TRANSFER", "OTHER"}

# The exact header line from Section 10.
HEADER = "DATE        PAYEE                 CATEGORY    AMOUNT        BALANCE"


def format_ledger(raw_text: str) -> str:
    """Return the normalised ledger per SPEC.md.

    Implement the full specification here. The signature and the constants above
    are fixed; everything else is your implementation.
    """
    raise NotImplementedError
