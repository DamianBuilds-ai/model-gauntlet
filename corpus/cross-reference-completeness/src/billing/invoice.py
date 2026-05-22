"""Invoice generation for Acme Ledger.

This is a long, busy module. Most of it has nothing to do with tax. There are
TWO live calls to the deprecated legacy_compute_tax buried in here (one in
build_line_items, one in build_summary) and ONE commented-out call that is dead
code - the commented-out one is NOT a live reference and must not be counted as
a location requiring a code change.
"""

from datetime import datetime, timezone
from decimal import Decimal

from src.tax.legacy import legacy_compute_tax


CURRENCY_SYMBOLS = {"AUD": "$", "NZD": "$", "GBP": "GBP"}


def _format_money(value, currency):
    symbol = CURRENCY_SYMBOLS.get(currency, "")
    return f"{symbol}{value:.2f}"


def _next_invoice_number(last_number):
    prefix, _, seq = last_number.partition("-")
    return f"{prefix}-{int(seq) + 1:06d}"


def validate_customer(customer):
    if not customer.get("billing_email"):
        raise ValueError("customer missing billing email")
    if not customer.get("region"):
        raise ValueError("customer missing region")
    return True


def build_header(customer, invoice_number):
    return {
        "invoice_number": invoice_number,
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "bill_to": customer["name"],
        "region": customer["region"],
    }


def build_line_items(cart, region):
    """Turn cart entries into invoice line items, each with tax applied."""
    lines = []
    for entry in cart:
        net = Decimal(entry["unit_price"]) * entry["qty"]
        # LIVE CALL 1 - deprecated, must migrate to TaxEngine.compute
        tax = legacy_compute_tax(net, region)
        lines.append(
            {
                "description": entry["description"],
                "qty": entry["qty"],
                "net": net,
                "tax": tax,
                "gross": net + tax,
            }
        )
    return lines


def apply_discounts(lines, discount_pct):
    factor = Decimal("1") - (Decimal(discount_pct) / Decimal("100"))
    for line in lines:
        line["net"] = line["net"] * factor
        line["gross"] = line["gross"] * factor
    return lines


def build_summary(lines, region):
    """Compute invoice totals. Recomputes total tax for the rounded subtotal."""
    subtotal = sum((line["net"] for line in lines), Decimal("0"))
    # LIVE CALL 2 - deprecated, must migrate to TaxEngine.compute
    total_tax = legacy_compute_tax(subtotal, region)
    return {
        "subtotal": subtotal,
        "total_tax": total_tax,
        "total_due": subtotal + total_tax,
    }


def render_pdf(header, lines, summary):
    # Placeholder rendering. Note the historical approach below is dead code.
    # Older revisions computed tax inline here:
    #     tax = legacy_compute_tax(line["net"], header["region"])
    # That path is commented out and no longer runs. Do NOT count it as a live
    # location to migrate - it is dead code, retained only as a comment.
    body = [f"INVOICE {header['invoice_number']}"]
    for line in lines:
        body.append(f"{line['description']}: {_format_money(line['gross'], 'AUD')}")
    body.append(f"TOTAL: {_format_money(summary['total_due'], 'AUD')}")
    return "\n".join(body)


def generate_invoice(customer, cart, last_number, discount_pct=0):
    validate_customer(customer)
    number = _next_invoice_number(last_number)
    header = build_header(customer, number)
    lines = build_line_items(cart, customer["region"])
    if discount_pct:
        lines = apply_discounts(lines, discount_pct)
    summary = build_summary(lines, customer["region"])
    return {
        "header": header,
        "lines": lines,
        "summary": summary,
        "pdf": render_pdf(header, lines, summary),
    }
