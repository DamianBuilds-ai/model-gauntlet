import csv
import io


def export_orders(rows):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "customer", "total", "status"])
    for r in rows:
        writer.writerow([r["id"], r["customer_name"], r["total"], r["status"]])
    return buf.getvalue()
