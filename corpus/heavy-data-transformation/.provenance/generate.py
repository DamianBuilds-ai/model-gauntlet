#!/usr/bin/env python3
"""
Deterministic generator for the heavy-data-transformation eval corpus.

Emits:
  - transactions.csv : a large flat ledger of expense line items (hundreds of rows),
    including several deliberately malformed rows the transform must handle precisely.
  - The expected nested target shape is documented in the spec notes (answer key).

This script also PRINTS the computed answer key (the exact aggregated nested JSON the
transform should produce) so the spec author can paste the verified numbers into the
spec notes. Run: python3 _generate.py  (stdout = answer-key JSON + row counts).

No network. No randomness without a fixed seed. Fully reproducible.
All companies, people, codes are fictional and neutral (Northwind, Globex, Acme,
Initech, Umbra, Cardinal).
"""
import csv
import io
import json
import random
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

SEED = 20260522
random.seed(SEED)

# ---- Fictional, neutral reference data ----------------------------------------
ENTITIES = ["Northwind", "Globex", "Acme", "Initech", "Umbra", "Cardinal"]

# department -> list of project codes under it
DEPARTMENTS = {
    "engineering": ["ENG-API", "ENG-WEB", "ENG-DATA"],
    "marketing": ["MKT-BRAND", "MKT-PERF"],
    "operations": ["OPS-WARE", "OPS-FLEET"],
    "research": ["RES-CORE", "RES-LABS"],
}

CATEGORIES = ["travel", "software", "hardware", "services", "supplies"]

# currency -> rate to USD (target settles everything to USD). Fixed table.
FX_TO_USD = {
    "USD": Decimal("1.00"),
    "EUR": Decimal("1.08"),
    "GBP": Decimal("1.27"),
    "AUD": Decimal("0.66"),
}

# ---- Build the clean rows -----------------------------------------------------
# Each row: txn_id, entity, department, project_code, category, currency, amount,
#           status, date
# Target aggregation (per the spec): group by entity -> department -> project_code,
# summing amount_usd for APPROVED rows only, rounding to 2dp half-up. Pending and
# rejected rows are excluded from totals but counted separately. Malformed rows are
# routed to a quarantine list with a reason, never silently dropped, never summed.

rows = []
txn_counter = 1000

def make_txn():
    global txn_counter
    txn_counter += 1
    return f"TX{txn_counter}"

# Generate a deterministic spread of ~300 clean rows.
N_CLEAN = 300
clean_specs = []
for i in range(N_CLEAN):
    entity = ENTITIES[i % len(ENTITIES)]
    dept = list(DEPARTMENTS.keys())[i % len(DEPARTMENTS)]
    proj = DEPARTMENTS[dept][i % len(DEPARTMENTS[dept])]
    cat = CATEGORIES[i % len(CATEGORIES)]
    cur = list(FX_TO_USD.keys())[i % len(FX_TO_USD)]
    # amount: deterministic but varied, 2dp
    amt = Decimal(str(round(50 + (i * 37.13) % 4800, 2)))
    # status cycle: mostly approved, some pending, some rejected
    smod = i % 7
    if smod in (5,):
        status = "pending"
    elif smod in (6,):
        status = "rejected"
    else:
        status = "approved"
    day = 1 + (i % 27)
    month = 1 + (i % 6)
    date = f"2026-{month:02d}-{day:02d}"
    clean_specs.append({
        "txn_id": make_txn(),
        "entity": entity,
        "department": dept,
        "project_code": proj,
        "category": cat,
        "currency": cur,
        "amount": str(amt),
        "status": status,
        "date": date,
    })

rows.extend(clean_specs)

# ---- Inject MALFORMED rows (the precision traps) ------------------------------
# These must be quarantined with a specific reason, NOT summed, NOT dropped silently.
malformed = []

# M1: amount has a thousands separator and currency symbol -> must be cleaned OR
#     quarantined consistently. We define the rule (see spec): amounts with stray
#     non-numeric chars beyond a single decimal point are MALFORMED -> quarantine
#     reason "unparseable_amount".
malformed.append({
    "txn_id": "TX9001", "entity": "Globex", "department": "engineering",
    "project_code": "ENG-API", "category": "software", "currency": "USD",
    "amount": "$1,250.00", "status": "approved", "date": "2026-03-04",
    "_reason": "unparseable_amount",
})

# M2: negative amount (refund posted to expense ledger) -> rule: negative amounts are
#     MALFORMED for this expense-only target -> quarantine "negative_amount".
malformed.append({
    "txn_id": "TX9002", "entity": "Acme", "department": "marketing",
    "project_code": "MKT-PERF", "category": "services", "currency": "EUR",
    "amount": "-300.00", "status": "approved", "date": "2026-02-11",
    "_reason": "negative_amount",
})

# M3: unknown currency code -> cannot FX-convert -> quarantine "unknown_currency".
malformed.append({
    "txn_id": "TX9003", "entity": "Northwind", "department": "operations",
    "project_code": "OPS-WARE", "category": "hardware", "currency": "JPY",
    "amount": "5000.00", "status": "approved", "date": "2026-01-19",
    "_reason": "unknown_currency",
})

# M4: project_code does not belong to the stated department (cross-dept mismatch) ->
#     quarantine "project_department_mismatch". (ENG-API under marketing.)
malformed.append({
    "txn_id": "TX9004", "entity": "Initech", "department": "marketing",
    "project_code": "ENG-API", "category": "travel", "currency": "GBP",
    "amount": "420.00", "status": "approved", "date": "2026-04-02",
    "_reason": "project_department_mismatch",
})

# M5: missing required field (empty entity) -> quarantine "missing_entity".
malformed.append({
    "txn_id": "TX9005", "entity": "", "department": "research",
    "project_code": "RES-CORE", "category": "supplies", "currency": "USD",
    "amount": "75.00", "status": "approved", "date": "2026-05-06",
    "_reason": "missing_entity",
})

# M6: invalid status value -> quarantine "invalid_status".
malformed.append({
    "txn_id": "TX9006", "entity": "Umbra", "department": "engineering",
    "project_code": "ENG-WEB", "category": "software", "currency": "AUD",
    "amount": "199.00", "status": "APPROVED?", "date": "2026-03-30",
    "_reason": "invalid_status",
})

# M7: malformed date -> quarantine "invalid_date". (Amount otherwise fine.)
malformed.append({
    "txn_id": "TX9007", "entity": "Cardinal", "department": "operations",
    "project_code": "OPS-FLEET", "category": "services", "currency": "USD",
    "amount": "640.00", "status": "approved", "date": "2026-13-40",
    "_reason": "invalid_date",
})

# M8: duplicate txn_id of an existing clean row -> quarantine "duplicate_txn_id".
#     We duplicate the FIRST clean row's id.
dup_id = clean_specs[0]["txn_id"]
malformed.append({
    "txn_id": dup_id, "entity": "Globex", "department": "research",
    "project_code": "RES-LABS", "category": "hardware", "currency": "EUR",
    "amount": "880.00", "status": "approved", "date": "2026-02-22",
    "_reason": "duplicate_txn_id",
})

# M9: amount is empty -> quarantine "unparseable_amount".
malformed.append({
    "txn_id": "TX9009", "entity": "Acme", "department": "marketing",
    "project_code": "MKT-BRAND", "category": "services", "currency": "USD",
    "amount": "", "status": "approved", "date": "2026-04-15",
    "_reason": "unparseable_amount",
})

# M10: text in amount field -> quarantine "unparseable_amount".
malformed.append({
    "txn_id": "TX9010", "entity": "Northwind", "department": "research",
    "project_code": "RES-CORE", "category": "supplies", "currency": "GBP",
    "amount": "two hundred", "status": "approved", "date": "2026-01-08",
    "_reason": "unparseable_amount",
})

# Splice malformed rows at varied positions so they are not all clustered at the end.
positions = [12, 45, 88, 130, 171, 205, 244, 270, 290, 299]
for pos, m in zip(positions, malformed):
    insert = {k: v for k, v in m.items() if k != "_reason"}
    rows.insert(pos, insert)

# ---- Write the CSV ------------------------------------------------------------
FIELDNAMES = ["txn_id", "entity", "department", "project_code", "category",
              "currency", "amount", "status", "date"]

with open("transactions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in FIELDNAMES})

# ---- Compute the ANSWER KEY (the exact nested target) -------------------------
# Rules (mirrors the spec):
#  - A row is MALFORMED (quarantined) if ANY: unparseable amount (stray chars/empty/
#    non-numeric), negative amount, unknown currency, project not in its department,
#    missing entity, invalid status (not in {approved,pending,rejected}), invalid date,
#    duplicate txn_id. Quarantine with the first matching reason (priority order below).
#  - amount_usd = round(amount * fx_rate, 2) half-up.
#  - totals_usd sums APPROVED, valid rows only, per entity -> department -> project.
#  - approved_count / pending_count / rejected_count per project from valid rows.
#  - quarantine list: {txn_id, reason}.

VALID_STATUSES = {"approved", "pending", "rejected"}
seen_ids = set()
dup_ids = set()
# first pass: detect duplicates by txn_id across the whole file
id_counts = defaultdict(int)
for r in rows:
    id_counts[r["txn_id"]] += 1

def is_valid_date(s):
    parts = s.split("-")
    if len(parts) != 3:
        return False
    try:
        y, mo, d = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return False
    if not (1 <= mo <= 12):
        return False
    if not (1 <= d <= 31):
        return False
    return True

def parse_amount(s):
    # valid = optional sign then digits with at most one dot, no other chars
    s2 = s.strip()
    if s2 == "":
        return None
    neg = s2.startswith("-")
    body = s2[1:] if neg else s2
    if body == "":
        return None
    if not all(c.isdigit() or c == "." for c in body):
        return None
    if body.count(".") > 1:
        return None
    try:
        val = Decimal(s2)
    except Exception:
        return None
    return val

def classify(r):
    # returns reason string if malformed else None. Priority order matters and is
    # documented in the spec.
    # 1 missing entity
    if r["entity"].strip() == "":
        return "missing_entity"
    # 2 invalid status
    if r["status"] not in VALID_STATUSES:
        return "invalid_status"
    # 3 invalid date
    if not is_valid_date(r["date"]):
        return "invalid_date"
    # 4 duplicate txn_id (only the SECOND+ occurrence is flagged; the first valid one
    #    stays). We flag the row whose txn_id count > 1 AND that we have already seen.
    # handled in main loop with seen set.
    # 5 unparseable amount
    amt = parse_amount(r["amount"])
    if amt is None:
        return "unparseable_amount"
    # 6 negative amount
    if amt < 0:
        return "negative_amount"
    # 7 unknown currency
    if r["currency"] not in FX_TO_USD:
        return "unknown_currency"
    # 8 project/department mismatch
    if r["project_code"] not in DEPARTMENTS.get(r["department"], []):
        return "project_department_mismatch"
    return None

# nested totals
agg = {}  # entity -> dept -> proj -> {total, approved, pending, rejected}
quarantine = []
processed_ids = set()

for r in rows:
    tid = r["txn_id"]
    # duplicate detection: first occurrence is processed normally; later ones quarantined
    if id_counts[tid] > 1 and tid in processed_ids:
        quarantine.append({"txn_id": tid, "reason": "duplicate_txn_id"})
        continue
    reason = classify(r)
    if reason is not None:
        quarantine.append({"txn_id": tid, "reason": reason})
        processed_ids.add(tid)
        continue
    processed_ids.add(tid)
    amt = parse_amount(r["amount"])
    usd = (amt * FX_TO_USD[r["currency"]]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    e, d, p = r["entity"], r["department"], r["project_code"]
    node = agg.setdefault(e, {}).setdefault(d, {}).setdefault(p, {
        "total_usd": Decimal("0.00"), "approved_count": 0,
        "pending_count": 0, "rejected_count": 0,
    })
    if r["status"] == "approved":
        node["total_usd"] += usd
        node["approved_count"] += 1
    elif r["status"] == "pending":
        node["pending_count"] += 1
    elif r["status"] == "rejected":
        node["rejected_count"] += 1

# Build the answer key in a stable, sorted, JSON-friendly shape.
def to_out(agg):
    out = {"entities": []}
    for e in sorted(agg):
        edict = {"entity": e, "departments": []}
        for d in sorted(agg[e]):
            ddict = {"department": d, "projects": []}
            for p in sorted(agg[e][d]):
                n = agg[e][d][p]
                ddict["projects"].append({
                    "project_code": p,
                    "total_usd": float(n["total_usd"]),
                    "approved_count": n["approved_count"],
                    "pending_count": n["pending_count"],
                    "rejected_count": n["rejected_count"],
                })
            edict["departments"].append(ddict)
        out["entities"].append(edict)
    return out

answer = to_out(agg)
answer["quarantine"] = sorted(quarantine, key=lambda x: (x["reason"], x["txn_id"]))
answer["_meta"] = {
    "total_rows_in_csv": len(rows),
    "valid_rows": len(rows) - len(quarantine),
    "quarantined_rows": len(quarantine),
}

print(json.dumps(answer, indent=2))
