# Classification taxonomy and rules - heavy-classification

You are classifying a large batch of inbound support messages for a fictional software
company (used by Acme, Globex, Initech, Northwind, and Umbra). Each message is one line
in `corpus/heavy-classification/messages.csv`. Assign EXACTLY ONE category to every
message, drawn from the eight categories below, by applying the rules in this document.

The task is scored against a per-item answer key, so an off-by-one or a mis-applied
precedence rule on a borderline item is a Correctness error. Classify every message - do
not skip any, do not invent categories, do not assign two categories to one message.

---

## 1. The eight categories

| Code | Category | Plain meaning |
|------|----------|---------------|
| `SEC`  | Security        | Account compromise, suspicious login, phishing, leaked credential, unauthorised access, data exposure. |
| `BILL` | Billing         | Invoices, charges, refunds, payment methods, subscription price, receipts, double-charge. |
| `AUTH` | Login / Access  | Cannot log in, password reset, locked out, two-factor not working, session expired (NON-malicious access trouble). |
| `BUG`  | Software bug    | A feature is broken, an error message appears, something crashes, data renders wrong, a button does nothing. |
| `PERF` | Performance     | The product is slow, times out, hangs, lags, is unresponsive under load (but not outright broken/erroring). |
| `FEAT` | Feature request | A request for new functionality, an enhancement, "it would be nice if", "can you add". |
| `DOCS` | Documentation   | The docs are wrong, missing, unclear, a link is dead, an example does not match the product. |
| `HOW`  | How-to question | A user asking how to do something the product already supports (usage question, not a bug, not a request). |

---

## 2. Classification rules (apply in this PRECEDENCE order - first match wins)

Many messages contain signals for more than one category. Apply these rules strictly in
order. The FIRST rule that matches decides the category. This precedence is the heart of
the eval - the borderline messages are written to match two or more categories, and only
the first-matching rule gives the correct label.

**Rule 1 (highest precedence) - Security wins over everything.**
If the message describes any security concern - account compromise, a login the user
does not recognise, a suspected phishing email, a leaked or exposed credential or API
key, unauthorised access, or sensitive data being visible to the wrong people - classify
it `SEC`, regardless of any other signal it also contains. A message that says "I was
charged for a login I did not make and I think my account is hacked" is `SEC`, not
`BILL`, because security beats billing. A message that says "I cannot log in AND I got an
email saying my password was changed by someone else" is `SEC`, not `AUTH`, because the
unauthorised change is a security signal.

**Rule 2 - Billing.**
If Rule 1 did not match and the message is about money - an invoice, a charge, a refund,
a payment method, the subscription price, a receipt, or a double-charge - classify it
`BILL`. A message that is about a billing PAGE that is broken still goes here only if the
core ask is about the money; if the core ask is "the invoices page shows an error", that
is a `BUG` (see Rule 4) - but a charge dispute, a refund request, or a price question is
`BILL`. When billing and a pure how-to overlap ("how do I update my card") treat an
actionable account-money task as `BILL`; a conceptual pricing question with no account
action ("how is the price calculated") is `BILL` as well (it is about money).

**Rule 3 - Login / Access (non-malicious).**
If Rules 1-2 did not match and the message is about being unable to access the account
through ordinary means - forgot password, password reset link, locked out after failed
attempts, two-factor code not arriving, session expired and will not renew - classify it
`AUTH`. The distinguishing line from `SEC` is intent: `AUTH` is the legitimate owner
having ordinary trouble; `SEC` is anything suggesting someone ELSE is involved or the
account is compromised. If there is any hint of an unrecognised actor, Rule 1 already
caught it.

**Rule 4 - Software bug.**
If Rules 1-3 did not match and the message describes something that is BROKEN - an error
message, a crash, a feature that does not work, data displayed incorrectly, a control
that does nothing - classify it `BUG`. A bug is the product doing the WRONG thing. Note
the boundary with `PERF` (Rule 5): if the product is merely SLOW or times out but is not
producing an error or wrong output, that is `PERF`, not `BUG`. An explicit error message
or wrong result is `BUG`; pure slowness is `PERF`.

**Rule 5 - Performance.**
If Rules 1-4 did not match and the message is about the product being slow, lagging,
hanging, timing out, or unresponsive WITHOUT an explicit error or wrong output, classify
it `PERF`. "The dashboard takes 40 seconds to load" is `PERF`. "The dashboard shows
error 500" is `BUG` (Rule 4 caught it first). A timeout that surfaces an explicit error
message is a judgment call: if the message leads with the SLOWNESS ("it is so slow it
eventually times out"), it is `PERF`; if it leads with an ERROR CODE, it is `BUG`. The
answer key resolves each such item explicitly.

**Rule 6 - Documentation.**
If Rules 1-5 did not match and the message is about the DOCUMENTATION being wrong,
missing, outdated, unclear, or a dead doc link, classify it `DOCS`. The distinguishing
line from `BUG`: `DOCS` is the docs being wrong about a product that works; `BUG` is the
product itself being wrong. "The guide says click Export but there is no Export button"
is `DOCS` (the docs are out of date). "The Export button throws an error" is `BUG`.

**Rule 7 - Feature request.**
If Rules 1-6 did not match and the message ASKS FOR new functionality or an enhancement -
"can you add", "it would be great if", "please support", "we need the ability to" -
classify it `FEAT`. The distinguishing line from `HOW`: `FEAT` asks for something the
product does NOT do yet; `HOW` asks how to do something the product ALREADY does. A
request phrased as a question ("is there a way to bulk-export?") is `FEAT` if the feature
does not exist and `HOW` if it does; the answer key states which, based on the message's
own framing (a message that says "there is no way to X, please add it" is `FEAT`; a
message that says "I cannot find how to X" is `HOW`).

**Rule 8 (lowest precedence) - How-to question.**
If none of Rules 1-7 matched, the message is a user asking how to accomplish a supported
task. Classify it `HOW`. This is the default for plain usage questions ("how do I invite
a teammate", "where do I find my API key", "how do I change the time zone").

---

## 3. Worked examples of the precedence (to anchor the borderline cases)

- "Someone logged into my account from another country and changed my billing card" ->
  `SEC`. Contains billing (Rule 2) and access (Rule 3) signals, but Rule 1 (unauthorised
  access) fires first.
- "I was double-charged this month and want a refund" -> `BILL`. No security signal, so
  Rule 1 skips; Rule 2 fires.
- "I forgot my password and the reset email never arrives" -> `AUTH`. No security signal
  (legitimate owner), no money, so Rules 1-2 skip; Rule 3 fires.
- "The export button shows error 500 every time" -> `BUG`. An explicit error, not mere
  slowness, so Rule 4 beats Rule 5.
- "Reports take over a minute to load lately, no error, just very slow" -> `PERF`. No
  error or wrong output, so Rule 5 (not Rule 4).
- "The setup guide references a Settings menu that does not exist anymore" -> `DOCS`. The
  product changed and the docs did not; Rule 6.
- "There is no way to export to PDF - can you add that?" -> `FEAT`. Asking for missing
  functionality; Rule 7.
- "How do I export my data to CSV?" -> `HOW`. Asking how to use an existing feature;
  Rule 8 (the product supports CSV export).

---

## 4. Output format

Output ONLY a single JSON array. Each element is an object with exactly two keys, in this
order:

```json
[
  {"id": "MSG-0001", "category": "SEC"},
  {"id": "MSG-0002", "category": "BILL"}
]
```

- `id` is the message id exactly as it appears in the CSV.
- `category` is one of the eight codes (`SEC`, `BILL`, `AUTH`, `BUG`, `PERF`, `FEAT`,
  `DOCS`, `HOW`) - uppercase, exactly as written above.
- One object per message, in the SAME ORDER as the CSV rows.
- Classify EVERY message. Do not skip, do not add, do not assign two categories.

After the JSON array, append the required output envelope (schemaVersion, tier, status,
tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (use spaced hyphens).
No emojis.
