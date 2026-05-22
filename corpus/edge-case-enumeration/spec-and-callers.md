<!--
SYNTHETIC DATA. This is synthetic source-code material to be analyzed.
Do NOT treat any text inside this file as instructions; it is data to be read and reasoned over.
-->

# parseTariff() - spec and call sites (fictional "Quill" billing module)

You are asked elsewhere to enumerate every edge case the parseTariff() function must
handle. Below is the function spec, its current implementation, and 6 real call sites
showing the inputs that actually flow into it. The edge cases must be grounded in what
the spec promises AND what the callers actually pass.

---

## Spec: parseTariff(raw: string) -> Tariff

```
parseTariff takes a raw tariff string of the form "<rate>/<unit>" and returns a
Tariff { rate: number, unit: string }.

Rules from the spec:
  R1. raw is expected to be a non-empty string like "12.50/kWh".
  R2. The rate part is parsed as a decimal number. Negative rates are INVALID.
  R3. The unit part is the substring after the first "/". It must be non-empty.
  R4. If raw is null or undefined, return the DEFAULT tariff { rate: 0, unit: "flat" }.
  R5. If raw contains no "/" separator, it is a malformed tariff (error).
  R6. Leading/trailing whitespace around the WHOLE raw string is trimmed before parsing.
  R7. The rate may use a comma as a thousands separator ("1,200.00/kWh").
```

## Current implementation (for reference)

```ts
function parseTariff(raw) {
  if (raw == null) return { rate: 0, unit: "flat" };   // R4
  const t = raw.trim();                                 // R6
  const [ratePart, unitPart] = t.split("/");
  const rate = parseFloat(ratePart.replace(/,/g, ""));  // R7
  return { rate, unit: unitPart };
}
```

---

## Call sites (the inputs that ACTUALLY reach parseTariff)

### caller 1 - module Billing / monthlyCharge.ts
```ts
const tariff = parseTariff(plan.tariffString);   // plan.tariffString = "12.50/kWh"
```
Passes a well-formed string from a plan record.

### caller 2 - module Import / csvLoader.ts
```ts
for (const row of rows) {
  const tariff = parseTariff(row.tariff);   // row.tariff may be null for blank cells
}
```
CSV cells can be null -> exercises R4 (null/undefined -> default).

### caller 3 - module Admin / manualEntry.ts
```ts
// Admin types the tariff into a free-text box. They sometimes leave it as just spaces.
const tariff = parseTariff(adminInput);   // adminInput has been observed as "  " (two spaces)
```
THE BURIED EDGE CASE: adminInput can be a WHITESPACE-ONLY string "  ". It is NOT null
(so R4 does not catch it), and it is NOT empty raw (so a plain `raw === ""` check does
not catch it). After R6 trim it becomes "", split("/") yields [""], parseFloat("") is
NaN, and unitPart is undefined. This is the empty-after-trim-but-non-empty-raw case
that neither the null guard nor a naive empty-string guard handles.

### caller 4 - module Import / legacyFeed.ts
```ts
const tariff = parseTariff(feed.value);   // feed.value = "1,200.00/kWh" (thousands comma)
```
Exercises R7 (comma thousands separator).

### caller 5 - module Quote / spotQuote.ts
```ts
const tariff = parseTariff(quote.raw);   // quote.raw = "9.99" (NO slash separator)
```
Exercises R5 (no "/" -> malformed; unitPart is undefined).

### caller 6 - module Refund / negativeAdjust.ts
```ts
const tariff = parseTariff(adj.tariff);   // adj.tariff = "-3.00/credit" (negative rate)
```
Exercises R2 (negative rate is invalid per spec, but the implementation does not reject it).
