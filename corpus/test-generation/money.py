"""Money / rounding utilities. Fully synthetic corpus for the test-generation eval -
a fictional "Acme" billing helper. All amounts are handled in integer cents internally
to avoid float drift; the public functions document their exact edge-case behaviour.

The eval asks for a pytest suite covering the PUBLIC functions (round_cents,
split_amount, parse_dollars, format_cents) and their documented edge cases. The
private helper `_normalise` must NOT be tested directly.
"""

from decimal import Decimal, ROUND_HALF_EVEN


def _normalise(value):
    """PRIVATE. Coerce an int, float, or numeric string to a Decimal. Internal only;
    not part of the public API and not to be tested directly."""
    if isinstance(value, bool):
        raise TypeError("bool is not a valid amount")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def round_cents(amount_cents):
    """Round a fractional cent amount to a whole number of cents using BANKER'S
    ROUNDING (round half to even).

    Examples (note the half-to-even behaviour):
        round_cents(2.5)  -> 2   (2.5 rounds to the even neighbour, 2)
        round_cents(3.5)  -> 4   (3.5 rounds to the even neighbour, 4)
        round_cents(2.4)  -> 2
        round_cents(2.6)  -> 3
        round_cents(-2.5) -> -2  (half-to-even applies symmetrically)
        round_cents(-3.5) -> -4
        round_cents(5)    -> 5   (already whole)

    Returns an int.
    """
    d = _normalise(amount_cents)
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))


def split_amount(total_cents, n):
    """Split an integer number of cents into n shares as evenly as possible, with the
    remainder distributed deterministically so the shares ALWAYS sum back to total_cents.

    The first (total_cents mod n) shares each get one extra cent. Order is largest
    shares first.

        split_amount(100, 3) -> [34, 33, 33]   (sums to 100, not [33,33,33])
        split_amount(100, 4) -> [25, 25, 25, 25]
        split_amount(10, 3)  -> [4, 3, 3]
        split_amount(-100, 3) -> [-34, -33, -33]  (remainder distributed on the
                                                   negative side; sums to -100)
        split_amount(5, 1)   -> [5]

    total_cents must be an int (whole cents). n must be an int >= 1; n < 1 raises
    ValueError. A non-int total_cents raises TypeError.
    """
    if not isinstance(total_cents, int) or isinstance(total_cents, bool):
        raise TypeError("total_cents must be an int number of cents")
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be an int >= 1")
    base, remainder = divmod(abs(total_cents), n)
    shares = [base + 1 if i < remainder else base for i in range(n)]
    if total_cents < 0:
        shares = [-s for s in shares]
    return shares


def parse_dollars(text):
    """Parse a dollar string into an integer number of cents.

    Accepts an optional leading '$', surrounding whitespace, and at most two decimal
    places. Examples:
        parse_dollars("12.34")  -> 1234
        parse_dollars("$12.34") -> 1234
        parse_dollars("  7 ")   -> 700
        parse_dollars("0.09")   -> 9
        parse_dollars("-3.50")  -> -350

    More than two decimal places raises ValueError (this function does NOT round -
    callers must round first). A non-numeric string raises ValueError.
    """
    s = text.strip()
    if s.startswith("$"):
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
        if len(frac) > 2:
            raise ValueError("more than two decimal places")
    try:
        d = Decimal(s)
    except Exception:
        raise ValueError("not a valid dollar amount: %r" % text)
    cents = (d * 100).to_integral_value(rounding=ROUND_HALF_EVEN)
    return int(cents)


def format_cents(amount_cents):
    """Format an integer number of cents as a dollar string with exactly two decimal
    places and a leading '$'. Negative amounts get the sign before the dollar sign.

        format_cents(1234) -> "$12.34"
        format_cents(9)    -> "$0.09"
        format_cents(-350) -> "-$3.50"
        format_cents(0)    -> "$0.00"
    """
    if not isinstance(amount_cents, int) or isinstance(amount_cents, bool):
        raise TypeError("amount_cents must be an int number of cents")
    sign = "-" if amount_cents < 0 else ""
    whole, frac = divmod(abs(amount_cents), 100)
    return "%s$%d.%02d" % (sign, whole, frac)
