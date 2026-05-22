#!/usr/bin/env python3
"""
Deterministic corpus generator for eval 36 - heavy-classification.

Emits:
  corpus/heavy-classification/messages.csv         (id, message) - hundreds of rows
  corpus/heavy-classification/.provenance/answer_key.json   (id -> correct category)

The correct category for every message is computed HERE, deterministically, so the
scoring Architect has an objective per-item key. The taxonomy + precedence rules are
documented in corpus/heavy-classification/taxonomy.md and must agree with the labels
produced here.

Categories (codes): SEC, BILL, AUTH, BUG, PERF, FEAT, DOCS, HOW
Precedence (first match wins): SEC > BILL > AUTH > BUG > PERF > DOCS > FEAT > HOW

All companies, names, and details are fictional. Neutral fictional org names only:
Acme, Globex, Initech, Northwind, Umbra.

Run:  python3 generate.py
(writes the two files relative to this script's grandparent corpus dir)
"""

import csv
import json
import os
import random

random.seed(20260522)  # deterministic

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.dirname(HERE)  # corpus/heavy-classification
MESSAGES_CSV = os.path.join(CORPUS_DIR, "messages.csv")
ANSWER_KEY = os.path.join(HERE, "answer_key.json")

ORGS = ["Acme", "Globex", "Initech", "Northwind", "Umbra"]
NAMES = ["Dana", "Marco", "Priya", "Tom", "Sarah", "Yuki", "Elena", "Omar",
         "Lena", "Raj", "Nina", "Carlos", "Mei", "Hassan", "Greta", "Diego"]

# ---------------------------------------------------------------------------
# Single-signal template banks. Each template clearly matches ONE category and
# does NOT contain a higher-precedence signal, so its label is unambiguous.
# {n} = a name, {o} = an org. These are the "clean" items.
# ---------------------------------------------------------------------------

CLEAN = {
    "SEC": [
        "I just got an alert about a login from a device I do not recognise - I think someone else is in my account.",
        "There is a sign-in from another country on my account that was not me. Please secure it.",
        "I received an email asking me to confirm my password by clicking a link - it looks like phishing.",
        "Someone accessed our workspace and I can see activity I did not perform. This looks like a compromise.",
        "Our API key got committed to a public repo by mistake and may be leaked - what do we do?",
        "A teammate can see another customer's records in the app - that data should not be visible to us.",
        "I found a session active on a computer that is not mine and cannot explain it.",
        "My account password was changed by someone else without my knowledge.",
        "We think an attacker is using a stolen credential to reach our data.",
        "There is unauthorised access on the {o} workspace - unfamiliar IP addresses in the audit log.",
        "Got a suspicious message pretending to be your support team asking for my login - is this a scam?",
        "An old employee still has access and is logging in after leaving - please revoke it, this is a security issue.",
    ],
    "BILL": [
        "I was charged twice for this month's subscription and need one charge refunded.",
        "My invoice shows a higher amount than the plan I signed up for - can you explain the charge?",
        "I want a refund for the annual plan I cancelled within the trial window.",
        "The receipt for last month never arrived in my email - can you resend it?",
        "My card was declined but I was still billed - please check the payment.",
        "Why did the price go up on my latest invoice compared to last quarter?",
        "I need to update the credit card on file for the {o} account billing.",
        "There is a charge on my statement from you that I do not recognise on the billing side.",
        "Can you switch our billing from monthly to annual and adjust the invoice?",
        "I was promised a discount that is not reflected on my invoice.",
        "How is the per-seat price calculated on our bill? The total seems off.",
        "Please remove the extra user from billing - we are being charged for a seat we do not use.",
    ],
    "AUTH": [
        "I forgot my password and the reset email never arrives - I just cannot get back in.",
        "I am locked out after too many failed attempts and the unlock link does not work.",
        "My two-factor code is not arriving by SMS so I cannot complete login.",
        "The password reset link says it has expired every time I click it.",
        "My session keeps expiring after a minute and I have to log in again and again.",
        "I cannot log in - the page just reloads to the sign-in screen with no error.",
        "The authenticator app is no longer in sync and rejects my codes at login.",
        "I changed my email and now cannot sign in with either the old or new address.",
        "The single sign-on button does nothing and I have no other way to log in.",
        "I need to reset my password but the 'forgot password' link is missing from the login page.",
        "My account is locked and the support article on unlocking does not help me get in.",
        "Two-factor is enabled but I lost my phone - how do I regain access to my own account?",
    ],
    "BUG": [
        "The export button throws an error 500 every single time I click it.",
        "The dashboard renders the totals as NaN instead of the real numbers.",
        "Saving a record shows a success message but the record is not actually saved.",
        "The date picker crashes the page whenever I select a range spanning two months.",
        "Filtering by status returns the wrong rows - it shows cancelled items under active.",
        "The app throws 'undefined is not a function' when I open the reports tab.",
        "Uploading a CSV produces duplicate entries for every row.",
        "The settings toggle does nothing - it flips back immediately and never saves.",
        "Numbers in the chart do not match the numbers in the table for the same period.",
        "The mobile view overlaps two buttons so I cannot tap either one.",
        "Deleting an item removes the wrong item from the list.",
        "The search box returns results for a query I did not type.",
    ],
    "PERF": [
        "The reports page takes over a minute to load lately, no error, it is just very slow.",
        "Everything lags badly in the afternoon - clicks take seconds to register.",
        "The dashboard hangs for 30 to 40 seconds before anything appears, then it works.",
        "Exports are extremely slow now - a file that took seconds takes many minutes.",
        "The app becomes unresponsive when we have many users on at once, then recovers.",
        "Search is painfully slow - it spins for a long time before showing results.",
        "Loading a large project times out because it is so slow, no error code shown.",
        "The page is sluggish and scrolling stutters, though nothing actually errors.",
        "Saving takes ages compared to last week - it eventually completes but very slowly.",
        "The {o} workspace crawls during peak hours - heavy lag, no crash.",
        "Switching tabs takes several seconds each time now, it used to be instant.",
        "The API responses are very slow today, just delayed, not failing.",
    ],
    "FEAT": [
        "There is no way to export to PDF right now - can you add that?",
        "It would be great if we could schedule reports to email automatically. Please support this.",
        "We need the ability to assign tags to multiple records at once - can you build bulk tagging?",
        "Please add a dark mode, the bright theme is hard on the eyes.",
        "Can you support webhooks so we can push events to our own system? There is none today.",
        "We would love a way to clone a project as a template - that option does not exist.",
        "Add an audit export so we can download the full activity history, which is not possible now.",
        "It would help if the calendar supported recurring events, which it currently cannot do.",
        "Please give us role-based permissions - right now everyone has the same access.",
        "Can you add a Spanish language option? The product is English only at the moment.",
        "We need an API endpoint for invoices - there is no programmatic access to them yet.",
        "A bulk import from a spreadsheet would save us hours - please add it, there is no importer.",
    ],
    "DOCS": [
        "The setup guide references a Settings menu that does not exist in the product anymore.",
        "Your docs say click Export under Tools, but Export is under File now - the guide is out of date.",
        "The API reference is missing the parameters for the create-stream call entirely.",
        "The link to the migration guide in your docs is dead - it returns a 404.",
        "The example in the tutorial does not match what the product actually shows on screen.",
        "The help article on two-factor setup skips the step where you scan the code.",
        "The documentation for the webhook payload lists fields that the real payload does not include.",
        "Your getting-started page still shows the old logo and an outdated screenshot.",
        "The docs claim a limit of 50 but the product enforces 100 - the documentation is wrong.",
        "The code sample in the guide uses a method name that the SDK no longer has.",
        "The onboarding doc links to a video that has been removed.",
        "The pricing explanation in the docs contradicts what the billing page says - the doc is unclear.",
    ],
    "HOW": [
        "How do I invite a teammate to my workspace?",
        "Where do I find my API key in the settings?",
        "How do I change the time zone for my account?",
        "How can I export my data to CSV?",
        "What is the way to rename a project?",
        "How do I set up a recurring report - I think the feature exists, I just cannot find it?",
        "Where is the option to enable email notifications?",
        "How do I move a record from one project to another?",
        "Can you tell me how to archive an old workspace rather than delete it?",
        "How do I share a read-only link to a dashboard?",
        "Where do I change the default currency display?",
        "How do I connect the {o} account to the mobile app?",
    ],
}

# ---------------------------------------------------------------------------
# BORDERLINE bank. Each message contains TWO+ category signals; the precedence
# rule decides. We HAND-LABEL each with the correct code under the documented
# precedence (SEC > BILL > AUTH > BUG > PERF > DOCS > FEAT > HOW). These are the
# rule-application tests. (message, correct_code, why)
# ---------------------------------------------------------------------------

BORDERLINE = [
    ("Someone logged into my account from another country and changed my billing card on file.", "SEC",
     "security (unauthorised access) beats billing - Rule 1"),
    ("I was charged for a subscription I never bought and I think my account was hacked.", "SEC",
     "security suspicion beats billing - Rule 1"),
    ("I cannot log in and I got an email saying my password was changed by someone else.", "SEC",
     "unauthorised change beats plain login trouble - Rule 1 over Rule 3"),
    ("The login page is broken AND I think a stranger accessed my account yesterday.", "SEC",
     "security beats bug - Rule 1 over Rule 4"),
    ("My reports are extremely slow and meanwhile I noticed an unfamiliar device on my account.", "SEC",
     "security beats performance - Rule 1 over Rule 5"),
    ("Your docs on enabling two-factor are wrong, and separately someone tried to log into my account.", "SEC",
     "security beats docs - Rule 1 over Rule 6"),
    ("The billing page shows error 500 whenever I open it.", "BUG",
     "the core ask is a broken page (error), not a money dispute - Rule 4 over Rule 2"),
    ("I was double-charged - please refund one of the charges.", "BILL",
     "pure money dispute, no security - Rule 2"),
    ("I cannot log in because my card expired and the account is suspended for non-payment.", "BILL",
     "the root cause is billing (non-payment), not ordinary access trouble - Rule 2 over Rule 3"),
    ("The invoices page is so slow it takes two minutes to show my charges.", "PERF",
     "no error and no money dispute - the complaint is slowness - Rule 5 over Rule 2 and Rule 4"),
    ("I forgot my password and the reset page throws an error when I submit it.", "AUTH",
     "ordinary access trouble; no security actor - Rule 3 (Rule 1 does not fire)"),
    ("The password reset feature is completely broken - it errors for everyone in our team.", "BUG",
     "a broken feature affecting everyone with an explicit error is a bug, not one user's access issue - Rule 4 over Rule 3"),
    ("Login is really slow today, it eventually logs me in after about a minute.", "PERF",
     "it succeeds, just slowly - slowness leads, no error - Rule 5 over Rule 3"),
    ("The export button does nothing and the docs say it should be under Tools.", "BUG",
     "the product control is broken (does nothing) - product wrong beats docs wrong - Rule 4 over Rule 6"),
    ("The guide says there is an Export button but I do not see one anywhere in the app.", "DOCS",
     "the docs describe a control the product no longer has - docs out of date, product not erroring - Rule 6"),
    ("Reports time out with a 504 error every time after about a minute.", "BUG",
     "an explicit error code leads - Rule 4 over Rule 5"),
    ("Reports are so slow they eventually time out, no error code, just spinning forever.", "PERF",
     "slowness leads, no error code surfaced - Rule 5 over Rule 4"),
    ("There is no bulk-delete and it would really help - can you add it?", "FEAT",
     "asking for missing functionality - Rule 7 (not a how-to)"),
    ("How do I bulk-delete records? I am sure it is possible, I just cannot find the option.", "HOW",
     "asking how to use an existing capability - Rule 8 (not a feature request)"),
    ("Is there a way to export to PDF? If not, please add it - we really need it.", "FEAT",
     "framed as missing-then-please-add - Rule 7 over Rule 8"),
    ("The pricing in your documentation does not match my invoice - which is right?", "DOCS",
     "the complaint is the docs contradicting reality, not a charge dispute - Rule 6 (Rule 2 needs a money ask)"),
    ("I want to dispute a charge that does not match the price your docs quote.", "BILL",
     "the core ask is a charge dispute (money) - Rule 2 over Rule 6"),
    ("The app is laggy and also the Settings docs are outdated.", "PERF",
     "performance outranks docs in precedence - Rule 5 over Rule 6"),
    ("Can you add a way to reset two-factor myself? Right now I have to email support every time.", "FEAT",
     "asking for new self-service functionality that does not exist - Rule 7 (not an access incident)"),
    ("My two-factor codes are rejected and I am locked out of my own account.", "AUTH",
     "legitimate owner, ordinary 2FA trouble, no other actor - Rule 3"),
    ("A button in the billing section is broken and throws an error when I click pay.", "BUG",
     "explicit error on a control - product broken - Rule 4 over Rule 2"),
    ("Please support exporting invoices via API - there is no endpoint for it today.", "FEAT",
     "request for missing functionality (about billing data, but the ask is a new feature) - Rule 7 (Rule 2 needs a money dispute, not a feature ask)"),
    ("How do I download my past invoices as PDF?", "HOW",
     "usage question about an existing capability - Rule 8 (Rule 2 needs a money dispute)"),
    ("Everything errors out with 'server unavailable' since this morning.", "BUG",
     "explicit error message - product broken - Rule 4 (not mere slowness)"),
    ("The whole app just feels sluggish since this morning, but nothing actually errors.", "PERF",
     "no error, pure slowness - Rule 5"),
]

# ---------------------------------------------------------------------------
# Build the message list. We aim for ~300 messages: a balanced spread of clean
# items across the 8 categories plus the borderline bank. Deterministic order
# is shuffled once with the fixed seed so borderline items are interleaved.
# ---------------------------------------------------------------------------

def fill(t):
    return t.replace("{o}", random.choice(ORGS)).replace("{n}", random.choice(NAMES))

records = []  # list of (message, code)

# Clean items: repeat each category's templates enough times to reach a target
# per-category count, filling placeholders each time so wording varies slightly.
PER_CATEGORY_CLEAN = 34  # 8 * 34 = 272 clean items
for code, templates in CLEAN.items():
    count = 0
    i = 0
    while count < PER_CATEGORY_CLEAN:
        t = templates[i % len(templates)]
        records.append((fill(t), code))
        count += 1
        i += 1

# Borderline items (30) - already hand-labelled.
for msg, code, _why in BORDERLINE:
    records.append((fill(msg), code))

# Shuffle so borderline + clean are interleaved (deterministic seed).
random.shuffle(records)

# Assign ids in final order.
rows = []
answer = {}
for idx, (msg, code) in enumerate(records, start=1):
    mid = f"MSG-{idx:04d}"
    rows.append({"id": mid, "message": msg})
    answer[mid] = code

# ---------------------------------------------------------------------------
# Write messages.csv (id,message) and answer_key.json (id -> code).
# ---------------------------------------------------------------------------

with open(MESSAGES_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "message"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

with open(ANSWER_KEY, "w", encoding="utf-8") as f:
    json.dump(
        {
            "total_messages": len(rows),
            "categories": ["SEC", "BILL", "AUTH", "BUG", "PERF", "DOCS", "FEAT", "HOW"],
            "precedence": "SEC > BILL > AUTH > BUG > PERF > DOCS > FEAT > HOW (first match wins)",
            "per_category_counts": {
                c: sum(1 for v in answer.values() if v == c)
                for c in ["SEC", "BILL", "AUTH", "BUG", "PERF", "DOCS", "FEAT", "HOW"]
            },
            "borderline_count": len(BORDERLINE),
            "labels": answer,
        },
        f,
        indent=2,
    )

# Also write a borderline rationale file so the Architect can see WHY each
# borderline item resolves the way it does (id is resolved post-shuffle).
msg_to_id = {r["message"]: r["id"] for r in rows}
borderline_lines = ["# Borderline rationale (heavy-classification)",
                    "",
                    "Each borderline message matches 2+ categories; the precedence rule decides.",
                    "Resolved id shown for the scoring Architect.",
                    ""]
for msg, code, why in BORDERLINE:
    filled = None
    # borderline messages contain no placeholders, so msg == filled
    rid = msg_to_id.get(msg, "UNKNOWN")
    borderline_lines.append(f"- {rid} -> {code}: {why}")
    borderline_lines.append(f"    msg: {msg}")
with open(os.path.join(HERE, "borderline-rationale.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(borderline_lines) + "\n")

print(f"Wrote {len(rows)} messages to {MESSAGES_CSV}")
print(f"Wrote answer key ({len(answer)} labels) to {ANSWER_KEY}")
print("Per-category counts:")
for c in ["SEC", "BILL", "AUTH", "BUG", "PERF", "DOCS", "FEAT", "HOW"]:
    print(f"  {c}: {sum(1 for v in answer.values() if v == c)}")
