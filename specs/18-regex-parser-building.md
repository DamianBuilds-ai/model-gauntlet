---
task_category: regex-parser-building
prompt_under_test: |
  You are given a log file at corpus/regex-parser-building/sample.log written in a
  custom application log format. Each log ENTRY begins with a bracketed ISO-8601 UTC
  timestamp and has this shape:

    [TIMESTAMP] LEVEL component: msg="..." key=value key=value ...

  where:
    - TIMESTAMP is the ISO-8601 instant inside the square brackets (e.g.
      2026-03-01T08:14:02Z).
    - LEVEL is one of INFO, WARN, ERROR, DEBUG (note: LEVEL may be followed by extra
      spaces for alignment before the component).
    - component is a single token followed by a colon (e.g. api, auth, db, cache).
    - msg is ALWAYS a double-quoted string and MAY contain commas, spaces, and equals
      signs inside the quotes.
    - the remaining fields are zero or more key=value pairs. A value is EITHER a
      double-quoted string (which may contain commas, spaces, and = signs) OR a bare
      token with no spaces. Different entries have different keys, and some keys are
      OPTIONAL (for example, user is present on some entries and absent on others).
    - an ERROR entry MAY be followed by one or more indented continuation lines (a
      multiline stack trace) that belong to the entry above them and do NOT start a new
      entry.

  Write ONE regex plus a short Python parse function that, together, extract the
  documented fields from EVERY sample entry, including the tricky ones. Specifically:

    1. The parser must return, for each of the log ENTRIES (not the continuation
       lines), a dict with at least: timestamp, level, component, msg, and a fields
       dict (or equivalent) holding the remaining key=value pairs with correct values.
    2. It must correctly extract quoted values that contain commas, spaces, and equals
       signs WITHOUT splitting them on the comma or the inner equals (for example
       query="red, blue, and green" is ONE value, and sql="SELECT * FROM t WHERE a=1,
       b=2" is ONE value).
    3. It must handle entries that lack optional keys (no crash, no fabricated key).
    4. It must NOT treat the indented stack-trace continuation lines as new entries -
       attach them to the preceding entry (e.g. as a "trace" field) or otherwise
       account for them, but do not emit a bogus entry per continuation line.
    5. State briefly which lines were the tricky ones and how your pattern handles each.

  Give the regex, the Python function, and (if you assert it works) say so honestly -
  do not claim it parses lines it does not. Output envelope required (schemaVersion,
  tier, status, tool_budget_used). No em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/regex-parser-building/
corpus_intent: |
  One custom-format log file (corpus/regex-parser-building/sample.log): 23 physical
  lines = 19 log ENTRIES plus a single 4-line multiline stack-trace body. The format is
  [ISO-timestamp] LEVEL component: msg="..." then zero-or-more key=value pairs. The file
  deliberately contains the cases that break a naive split-on-comma or split-on-equals
  parser.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a regex that parses the EASY
  lines and silently mangles or drops the tricky ones is WORSE than an honest, partial
  solution that says which lines it does not yet handle. The dangerous failure mode is a
  parser that looks complete and confident - it returns a clean dict for every easy line
  - but quietly produces WRONG values on the hard lines (splitting query="red, blue, and
  green" into three fields, truncating sql="..." at the first comma or inner =, or
  emitting four junk entries for the stack-trace continuation lines). A downstream system
  would trust those wrong values. Reward a parser that actually handles the quoted-comma,
  inner-equals, optional-field, and multiline cases (or honestly flags any it misses).
  Penalise hardest the confident parser that claims it works on every line while
  corrupting the tricky ones.

  ANSWER KEY (for the scoring Architect - the tricky lines and the correct handling).

  Structure: 19 entries (lines that start with "["), 4 continuation lines (physical
  lines 10-13, the indented Traceback block) that belong to the ERROR worker entry on
  line 9. A correct parser yields exactly 19 entry records, not 23.

  The TRICKY cases a strong parser must get right (these are the differentiators):

    T1. QUOTED VALUE WITH COMMAS (line 4): query="red, blue, and green". This is ONE
        value. A split-on-comma parser wrongly yields three pieces. Correct: a single
        field query = "red, blue, and green".

    T2. QUOTED VALUE WITH INNER EQUALS AND COMMA (line 5): sql="SELECT * FROM t WHERE
        a=1, b=2". One value containing both "=" and ",". A split-on-"=" or split-on-","
        parser corrupts it. Correct: sql = "SELECT * FROM t WHERE a=1, b=2".

    T3. QUOTED msg WITH COMMA (lines 8, 18, 19, 23 and others): e.g. msg="threshold
        approaching, 80% used", msg="deadlock detected, retrying", msg="evicted entries,
        freeing memory", msg="unhandled, returning 500". The msg field itself contains
        commas and must not be split.

    T4. QUOTED VALUE WITH COMMA in a non-msg field (line 19): reason="ttl, expired".
        Same trap as T1 but on an arbitrary key.

    T5. QUOTED VALUE WITH A LEADING SYMBOL (line 11... no - line with billing): line 12
        in entry terms billing: amount="$19.99". The quotes must be stripped to $19.99
        (or kept consistently); the "$" must not break tokenisation.

    T6. OPTIONAL FIELD ABSENT (lines 1, 5, 9, 18, 19, 21, 22): no user= key. The parser
        must NOT crash and must NOT fabricate a user key for these entries. Correct: the
        fields dict simply omits user for those entries.

    T7. THE MULTILINE STACK TRACE (physical lines 10-13, under the ERROR worker entry on
        line 9): four indented lines that are NOT new entries. A correct parser attaches
        them to the line-9 entry (e.g. as a trace field) or otherwise associates them,
        and crucially does NOT emit four bogus entry dicts. This is the hardest case
        because a per-line regex with re.match on each physical line will, without extra
        logic, either error or silently skip these - and a naive "every line is an entry"
        loop produces four garbage records. The correct approach groups continuation
        lines (lines not starting with "[") with the preceding entry, OR uses a
        multiline/DOTALL strategy that captures the trace as part of entry 9.

    T8. LEVEL ALIGNMENT PADDING: INFO and WARN are followed by TWO spaces, ERROR and
        DEBUG by ONE, for column alignment (e.g. "INFO  api" vs "ERROR db"). The regex
        must tolerate variable whitespace between LEVEL and component (\s+), not assume a
        single space.

  The EASY lines (health checks, simple request-received lines with bare-token fields
  like method=GET path=/health status=200 dur_ms=3) are where a weak parser succeeds and
  thereby looks fine. Getting only those right is the trap.

  Confidently-wrong signatures (penalise): a regex like (\w+)=(\S+) that stops a quoted
  value at the first space (truncating query to "red,); a comma-split that explodes T1-T4
  into extra fields; a per-physical-line loop that emits 23 records or 4 junk records for
  the trace; or a claim "this parses every line" when the pattern visibly cannot capture
  a space-containing quoted value.

  Scoring guidance:
    - Correctness (hard-fail eligible): does the regex + function actually extract the
      documented fields correctly for the TRICKY lines (T1-T8), yielding 19 entries with
      uncorrupted quoted values and no junk trace entries? A parser that mangles the
      quoted-comma/inner-equals values or emits per-continuation-line entries is
      Correctness=1 (confidently wrong if it also claims to work).
    - Reasoning quality (the differentiator): does it correctly identify WHY the naive
      split fails and design for the quoted-value and multiline cases deliberately (e.g.
      a quote-aware value pattern like "[^"]*"|\S+, and a continuation-line grouping
      pass), rather than stumbling onto a fragile pattern?
    - Hallucination (hard-fail eligible): inventing a field that is not in the data, or
      claiming the regex handles a case it provably cannot.
    - Completeness: covers all the tricky cases T1-T8 (or honestly enumerates any it does
      not handle) and addresses the multiline lines explicitly.
    - Format adherence: a single regex + a short Python function (not a 200-line parser),
      the per-entry dict shape requested, and a clean envelope.
    - Discipline: stayed within "one regex + short function", did not over-engineer into
      a full grammar, and did not silently drop the hard lines.
    - Source transparency: names which sample lines are the tricky ones and how the
      pattern handles each (rule 5).
    Voice match does NOT apply.
notes: |
  New task type. Tests building a parser (one regex plus a short Python function) for a
  custom log format whose difficulty is concentrated in a handful of tricky lines:
  double-quoted values containing commas, spaces, and inner equals signs; optional fields
  absent on some entries; level-alignment whitespace padding; and a 4-line multiline stack
  trace that must attach to its parent entry rather than spawn bogus records.

  The eval is built so a weaker model can be CONFIDENTLY WRONG. The easy lines (health
  checks, bare-token key=value request logs) are trivially parseable, so a naive
  (\w+)=(\S+)-style regex returns clean dicts for most of the file and looks complete -
  while silently truncating query="red, blue, and green" at the first space, splitting
  sql="SELECT * FROM t WHERE a=1, b=2" on its inner comma/equals, and emitting four junk
  entries for the indented traceback. That confident, well-formed, wrong output is worse
  than an honest partial parser that flags the lines it cannot yet handle. The 19-entries
  -not-23 count (the multiline trace) and the quoted-comma/inner-equals values are the
  load-bearing differentiators. See corpus_intent for the full tricky-case answer key
  (T1-T8) and the structure (19 entries, one 4-line trace body on the ERROR worker entry).

  Correctness and Hallucination are hard-fail eligible (a parser that corrupts the quoted
  values or claims to handle lines it cannot is a wrong answer / a fabrication). Reasoning
  quality is the central differentiator: deliberately designing a quote-aware value
  pattern and a continuation-line grouping pass, versus stumbling onto a fragile regex
  that only fits the easy lines. Voice match does not apply. The corpus is the directory
  corpus/regex-parser-building/.
---

# Spec 18 - regex-parser-building (custom log format)

Write one regex plus a short Python parse function that extracts the documented fields
from EVERY entry in the custom-format log at `corpus/regex-parser-building/sample.log`,
including the tricky lines. Standard four-phase `/eval-pit` flow against the frozen
`rubric/rubric.md`.

The format is `[ISO-timestamp] LEVEL component: msg="..." key=value ...`. The file is 23
physical lines but only 19 log entries: one ERROR entry is followed by a 4-line indented
stack trace that belongs to it and must not spawn new records. The difficulty is
concentrated in a few lines: double-quoted values that contain commas, spaces, and inner
equals signs (`query="red, blue, and green"`, `sql="SELECT * FROM t WHERE a=1, b=2"`,
`reason="ttl, expired"`), optional fields absent on some entries (no `user=`),
level-alignment whitespace padding, and the multiline trace.

This is the correctness-first quality principle in a parser-building setting: the easy
request-log lines are trivially parseable, so a naive `(\w+)=(\S+)` regex returns clean
dicts for most of the file and LOOKS complete - while truncating the space-containing
quoted values, splitting on inner commas/equals, and emitting four junk entries for the
traceback. That confident-but-wrong parser is worse than an honest partial one that flags
what it cannot handle. Correctness and Hallucination are hard-fail eligible; the
quoted-value handling and the 19-entries-not-23 multiline grouping are the load-bearing
differentiators, and Reasoning quality (deliberately designing for the hard cases)
separates the strong answers. Voice match does not apply. The corpus is the directory
`corpus/regex-parser-building/`.
