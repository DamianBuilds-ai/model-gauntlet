---
task_category: format-conversion
prompt_under_test: |
  You are given a single legacy configuration file at
  corpus/format-conversion-xl/service-config.properties written in a dotted-key
  "properties" format. Convert the ENTIRE file into one strict nested JSON object,
  applying the conversion rules below exactly.

  Conversion rules (apply all of them):
    1. COMMENTS: any line whose first non-whitespace character is '#' or ';' is a
       comment and is dropped entirely. Blank lines are dropped. There are NO inline
       comments - a '#' that appears after a value is part of the value.
    2. KEY/VALUE SPLIT: a line is split on its FIRST unescaped '=' into a key (left)
       and value (right). Whitespace around the '=' is trimmed. Leading and trailing
       whitespace of the value is trimmed; whitespace INSIDE an unquoted value is
       preserved. A backslash immediately before an '=' (\=) is a literal '=' inside
       the value and does NOT count as the separator.
    3. NESTING: each '.' in the key creates a nested object level. So a.b.c = x
       becomes {"a": {"b": {"c": "x"}}}. Merge keys that share prefixes into the same
       nested objects.
    4. DUPLICATE KEYS: if the same fully-qualified key is assigned more than once, the
       LAST assignment wins; earlier assignments are discarded entirely.
    5. SCALAR TYPING for UNQUOTED values:
         - the bare tokens true and false (lowercase only) become JSON booleans;
         - the bare token null (lowercase only) becomes JSON null;
         - a value that is a valid integer becomes a JSON integer;
         - a value that is a valid decimal becomes a JSON number;
         - everything else is a JSON string (this includes True, FALSE, yes, no - only
           lowercase true/false are booleans).
    6. QUOTED values: a value wrapped in double quotes is ALWAYS a JSON string. Strip
       the surrounding double quotes and keep the inside verbatim (so "5432" is the
       string "5432", "true" is the string "true", "null" is the string "null").
    7. LISTS: an UNQUOTED value that contains one or more commas is a JSON array. Split
       on commas, trim each element, and type each element by the scalar rules in (5).
       A value with NO comma is a scalar, never a one-element array. An empty value
       (nothing after the '=') is the empty string "".

  Output ONLY a single valid JSON object - one fenced ```json block is acceptable, but
  no prose or commentary outside it. Use 2-space indentation. After the JSON block,
  append the required output envelope (schemaVersion, tier, status, tool_budget_used)
  as separate lines OUTSIDE the JSON. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/format-conversion-xl/
corpus_intent: 1 legacy properties config file converted to one strict nested JSON object
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): every conversion rule has
  exactly one correct outcome, computed below. A model that mis-types a value (quotes a
  string as a number, keeps an earlier duplicate, treats a one-element value as a list,
  swallows the '#' in database.comment, mishandles the escaped '=' in routing.rule.match,
  or coerces "true"/"5432"/"null" out of string form) has produced confidently-wrong
  output a downstream parser would trust. A model that nests correctly but fumbles one
  trap is partially correct; a model that silently drops a key or invents a key is worse.
  Correctness and Hallucination are hard-fail eligible. There is no inference required -
  the rules are total.

  Why XL / harder: this is a LARGE conversion (40+ assignments after comment-stripping,
  five-deep nesting in places) with SEVEN distinct edge-case classes layered together -
  duplicate-last-wins (x3), quoted-forces-string (x4), list-split-with-per-element-typing
  (x3), one-element-is-scalar-not-list, escaped-separator, hash-inside-value, and
  casing-sensitive booleans. A weaker model holds two or three of these and drops the
  rest; the spread is in how many edge classes survive simultaneously across one long
  output.

  ANSWER KEY (computed - the EXACT JSON the rules produce; the scoring Architect compares
  field-by-field. Key order within an object is not scored, only keys + values + types):

  {
    "service": {
      "name": "orders-api",
      "version": "2.14.0",
      "enabled": true,
      "replicas": 4,
      "weight": 0.75,
      "owner": {
        "team": "payments",
        "email": "oncall@northwind.example",
        "pager": {
          "primary": "+61-400-000-111",
          "escalation": "+61-400-000-222"
        }
      },
      "timeout_ms": 2500
    },
    "database": {
      "host": "db.internal.northwind.example",
      "port": 5432,
      "ssl": true,
      "pool": {
        "min": 2,
        "max": 20,
        "idle_timeout_ms": 30000
      },
      "replica": null,
      "password_rotated": false,
      "schema": "public",
      "label": "5432",
      "dr_enabled": "true",
      "comment": "primary cluster # do not failover manually"
    },
    "features": {
      "regions": ["ap-southeast-2", "us-east-1", "eu-west-1"],
      "flags": ["beta", true, 7, "canary"],
      "fallback": "",
      "retry_codes": [429, 500, 502, 503],
      "default_region": "ap-southeast-2"
    },
    "limits": {
      "min_balance": -50,
      "free_tier": 0,
      "burst_multiplier": 1.5,
      "note": "null"
    },
    "telemetry": {
      "exporter": {
        "otlp": {
          "endpoint": "collector.northwind.example:4317",
          "timeout_ms": 10000,
          "compression": "gzip"
        }
      },
      "sampling": {
        "ratio": 0.1,
        "parent_based": true
      }
    },
    "routing": {
      "rule": {
        "path": "/api/v2/orders",
        "match": "method=POST",
        "description": "legacy order intake path",
        "priority": 10
      }
    },
    "auth": {
      "enabled": true,
      "strict": "True",
      "allow_anonymous": "no",
      "provider": "oidc",
      "token_ttl_seconds": 3600
    },
    "audit": {
      "enabled": false,
      "sink": "stdout",
      "redact_fields": ["password", "token", "abn"]
    }
  }

  TRAP / EDGE INDEX (the eight places a weaker model goes wrong):
    A. service.timeout_ms - duplicate, LAST wins: 2500 (not 1000).
    B. audit.enabled - duplicate spanning other keys, LAST wins: false (not true).
    C. database.label "5432" / database.dr_enabled "true" / limits.note "null" -
       quotes force STRING; must NOT become number 5432, boolean true, or JSON null.
    D. database.comment - the '#' is INSIDE the quoted value; must NOT be stripped as a
       comment. Full string "primary cluster # do not failover manually".
    E. features.flags - list with mixed per-element types: string, boolean true,
       integer 7, string. Must type each element independently.
    F. features.default_region - no comma, so a SCALAR string, NOT a one-element array.
    G. features.fallback - empty value is "" (empty string), not null, not [].
    H. routing.rule.match - escaped '\=' yields literal "method=POST"; the first
       UNESCAPED '=' (after "match") is the separator.
    Plus: auth.strict=True / auth.allow_anonymous=no are STRINGS (casing/word not a
    lowercase boolean); negative -50 and zero 0 are integers; weight 0.75 / ratio 0.1 /
    burst_multiplier 1.5 are numbers; five-deep nesting under service.owner.pager and
    telemetry.exporter.otlp must merge correctly under shared prefixes.

  Scoring guidance: Correctness = value + type accuracy across all 41 leaf assignments
  (post de-dup) and correct nesting structure. Hallucination (hard-fail) = inventing a
  key/value not in the file, or fabricating a value for a key. Format adherence = single
  valid JSON object, clean fenced block, envelope outside the JSON. Completeness = every
  surviving key present (41 leaves after the 3 duplicates collapse). Discipline =
  honoured the typing + quoting + comment rules rather than guessing. Reasoning quality
  applies (the rules must be applied, not pattern-matched). Source transparency applies
  weakly (one source file). Voice match does NOT apply.

  Leaf count check: post de-dup the object has 41 leaf values (service: 5 scalars +
  owner.team/email + pager.primary/escalation + timeout_ms = 10; database: host/port/ssl
  + pool.min/max/idle + replica/password_rotated/schema/label/dr_enabled/comment = 12;
  features: regions/flags/fallback/retry_codes/default_region = 5; limits: 4; telemetry:
  endpoint/timeout/compression/ratio/parent_based = 5; routing.rule: 4; auth: 5; audit:
  redact_fields + enabled/sink = 3 -> 10+12+5+4+5+4+5+3 = 48 raw lines minus 3 collapsed
  duplicates = the listed structure). Architect: count leaves against the key above.
---

# Spec 58 - format-conversion-XL (large nested config, dotted-key properties to strict JSON)

Convert one large legacy dotted-key properties configuration file at
`corpus/format-conversion-xl/service-config.properties` into a single strict nested JSON
object, applying seven layered conversion rules exactly: comment/blank-line stripping,
first-unescaped-`=` key/value splitting (with `\=` as a literal escaped equals),
dot-driven nesting that merges shared prefixes, duplicate-key last-wins, casing-sensitive
scalar typing (only lowercase `true`/`false`/`null` are special), quotes-always-force-string,
and comma-split lists with per-element typing (one-element values stay scalars).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
conversion is total - there is one computed-correct JSON output (the answer key in
notes), so the correctness-first quality principle bites hard: a mis-typed value, a kept
earlier duplicate, a swallowed in-value `#`, a mishandled escaped `=`, or a one-element
value promoted to an array is confidently-wrong output a parser would trust. Correctness
and Hallucination are hard-fail eligible. Format adherence (single valid JSON object,
envelope outside) and Discipline (apply the rules, do not guess) are the load-bearing
differentiators. Voice match does not apply. The corpus is the directory
`corpus/format-conversion-xl/`.
