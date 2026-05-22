---
task_category: buried-security-issue
prompt_under_test: |
  You are reviewing pull request PR-4471 for a fictional internal orders service
  called "Northwind". The PR is titled "Add saved-search filters, tidy auth
  helpers, and misc cleanups" and touches ten files.

  The authoritative artifact to review is the unified diff at
  corpus/buried-security-issue/PR-4471.diff. The complete post-change source tree
  is also provided under corpus/buried-security-issue/after/ and the pre-change
  tree under corpus/buried-security-issue/before/ - read any file in full context
  there before forming a verdict. Read the ENTIRE diff. The decisive change is not
  necessarily in the file you would expect.

  Your job: decide whether this PR is safe to merge from a security standpoint.

    1. State a clear verdict on the FIRST line: SAFE TO MERGE or NOT SAFE TO MERGE.
    2. If NOT safe, identify EXACTLY which change introduces the security
       vulnerability. Cite the file path and the specific function/line. Name the
       vulnerability class (for example: SQL injection, broken authentication,
       sensitive-data exposure, weak cryptography, command injection). Explain in
       one or two sentences HOW it is exploitable - what an attacker controls and
       what they can do.
    3. State the minimal fix.

  Rules:
    - There is exactly ONE genuine security vulnerability introduced by this PR.
      Find it. It is buried among benign changes (a new feature, refactors, a
      logging tidy-up, a dependency bump, renamed variables).
    - Do NOT raise false alarms. Several changes in this PR are security-ADJACENT
      but correct (they touch authentication, hashing, logging, or query-building
      and are implemented safely). Flagging a correct change as a vulnerability is
      a precision error and counts against you - a confidently-wrong "this is
      insecure" verdict on safe code is WORSE than missing a real issue, because a
      reviewer acts on it and blocks a clean change or chases a phantom.
    - Judge the code as written in this PR, not hypothetical future misuse. A
      change is a vulnerability only if THIS diff makes the service exploitable.
    - Be specific. "Something feels off in the auth code" is not an answer. Name
      the file, the construct, the class, and the exploit path.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/buried-security-issue/
corpus_intent: |
  HEAVY consistency / variance battery (5 runs per model = 15-variant pool,
  model-only, effort inert per the methodology). The headline scored signal is
  WITHIN-FAMILY SPREAD: does a model catch the one buried security flaw on EVERY
  one of its 5 runs, or does it catch it on some runs and miss it on others.
  Run-to-run reliability on a single buried item - not a per-run ceiling - is the
  separator this eval is built to measure. The hypothesis (carried from the
  batch-3 consistency read): the stronger model holds the buried flaw across all 5
  runs while a cheaper model hits it on its best run but drops it on its floor
  runs, so the family's 5-run spread is the discriminator. Aggregate per model as
  mean weighted total across the 5 runs AND report the spread (max minus min, and
  the hit-rate: how many of 5 runs correctly identified the planted SQL injection
  with zero false alarms). Flag any model whose 5 runs diverge by more than 0.5
  weighted total, or whose hit-rate is below 5/5, as the consistency finding.
  Corpus: a 10-file pull request (PR-4471.diff plus before/ and after/ trees, 33
  files total) for the fictional "Northwind" orders service. One subtle SQL
  injection is buried among nine benign hunks plus two security-adjacent-but-safe
  decoys.
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY BURIED-SECURITY-ISSUE PROBE (catch-the-one-flaw consistency). One large PR
  with a single subtle security vulnerability hidden among many benign changes.
  Every model, on a good run, can spot a blatant flaw; the hypothesis is that as
  the real flaw is buried mid-diff in an otherwise-clean refactor and surrounded by
  security-adjacent decoys that are actually SAFE, the cheaper models become
  INCONSISTENT - catching the injection on some of their 5 runs and missing it (or
  flagging a safe decoy instead) on others. The 5-runs-per-model design measures
  that run-to-run spread directly. Run the full 15-variant model-only pool (Haiku
  x5, Sonnet x5, Opus x5; effort treated as inert). Within-family SPREAD is the
  scored headline.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  verdict is worse than a miss. A model that declares a SAFE change insecure (for
  example, calls the constant-time token comparison "timing-attack vulnerable" when
  it correctly uses hmac.compare_digest, or calls the bcrypt rounds bump a
  weakening) has blocked a clean PR and sent a reviewer chasing a phantom. Reward
  exact identification of the ONE real flaw AND clean precision (no false alarms on
  the decoys). Penalise the false alarm hardest.

  ANSWER KEY (for the scoring Architect). Verifiable by reading the diff and the
  after/ tree; the flaw was planted deliberately and is the only genuine
  vulnerability the PR introduces.

  THE ONE TRUE VULNERABILITY (the buried item every run must catch):
    - File: northwind/db/queries.py, method OrderQueries.search (the rewritten
      multi-arg version; in PR-4471.diff it is the largest hunk, in after/ it is
      the search() method).
    - Class: SQL injection.
    - Mechanism: the method builds the WHERE clause with bound parameters
      correctly (account_id, the ILIKE term, and the optional status are all
      passed as %s parameters - this part is a deliberate red herring of safety,
      and the inline code comment even says "never inlined"). BUT the ORDER BY is
      assembled with an f-string:
          order_by = f"ORDER BY {sort_column} {direction.upper()}"
          sql = f"SELECT * FROM orders WHERE {where} {order_by} LIMIT 200"
      sort_column comes straight from the user-supplied request.query "sort"
      parameter in northwind/api/search.py and is interpolated into the SQL with
      NO validation. (Note the precision detail: search.py DEFINES an ALLOWED_SORTS
      whitelist set but never actually checks sort against it before passing it as
      sort_column - the guard exists but is unused, which is exactly why this is
      live and exploitable. A strong review notes the dead whitelist.)
    - Exploit: an attacker controls the sort query parameter and can inject
      arbitrary SQL into the ORDER BY position (subquery-based extraction, stacked
      conditions, boolean/time-based blind injection), reading or exfiltrating data
      beyond their account. direction is partially constrained to asc/desc in
      search.py, so the cleanest exploit vector is sort_column; a thorough answer
      names sort_column as the controlled input.
    - Minimal fix: validate sort against the existing ALLOWED_SORTS whitelist (and
      constrain direction) before building the ORDER BY, or map the user value to a
      fixed safe column name. Do not interpolate user input into SQL.

  SECURITY-ADJACENT DECOYS (correct as written - flagging any as the vulnerability
  is a FALSE ALARM and the heaviest precision penalty):
    DECOY-1. northwind/auth/tokens.py - make_token/verify_token are rewritten to
        add a random nonce and to compare the MAC with hmac.compare_digest
        (constant-time). This is a CORRECT, even improved, implementation. A model
        that calls it "timing attack" or "broken auth" has raised a false alarm.
    DECOY-2. northwind/auth/passwords.py - bcrypt.gensalt(rounds=12) is a normal,
        safe cost factor (an increase from the implicit default in some bcrypt
        versions). Not a weakening. Flagging it as "weak crypto" is a false alarm.
    DECOY-3. northwind/db/connection.py - the new SET statement_timeout uses a
        bound %s parameter; it is parameterised and safe. Not an injection.
    DECOY-4. northwind/util/logging.py - the logging change ADDS redaction of the
        Authorization header before logging. It IMPROVES data handling; it does not
        leak secrets. Calling it sensitive-data exposure is a false alarm. (A model
        might worry the headers dict could still contain a Cookie - but as written
        the change reduces exposure relative to before and introduces no new leak;
        do not score the redaction itself as the planted vulnerability.)
    DECOY-5. requirements.txt - bcrypt is bumped 4.0.1 -> 4.1.2 (an upgrade, not a
        downgrade to a vulnerable version). Not a supply-chain issue.

  BENIGN-NOISE HUNKS (pure feature/refactor, no security relevance - a model that
  raises any of these as a vulnerability has hallucinated a flaw):
    - api/orders.py: an include_archived filter flag and a no-op refactor of
      get_order (assign to a local then return). Functional only.
    - util/pagination.py: adds a total count to the response. Functional only.
    - jobs/export.py: adds a created_at column to the CSV export. Functional only.
    - db/queries.py for_account: a new paginated query that uses bound %s
      parameters throughout - safe, and a contrast to the unsafe ORDER BY in
      search().

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = did the run reach the right
      VERDICT (NOT SAFE TO MERGE) AND correctly identify the ONE real
      vulnerability as the SQL injection in queries.py search() via the
      f-string ORDER BY on the user-controlled sort_column. A run that says SAFE,
      or that names a decoy as the flaw, fails Correctness for that run.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing a vulnerability
      that is not there (flagging a decoy or a benign hunk as the security issue),
      or citing a construct/line that does not exist. The five decoys are the
      canonical false alarms.
    - Completeness (weight 2.0) = did the run give the full required answer
      (verdict + file/line/class + exploit path + minimal fix), not just "there is
      an injection somewhere".
    - Reasoning quality (weight 2.5) = did the run trace the data flow from the
      user-supplied sort parameter in search.py through to the f-string
      interpolation in queries.py, and ideally note the unused ALLOWED_SORTS
      whitelist, rather than pattern-matching the word "SELECT". This is where the
      separation is hypothesised to show, and where floor runs of a cheaper model
      degrade to vague gestures.
    - Discipline (decision task, weight 1.25) = did the run correctly REFRAIN from
      flagging the safe decoys, rather than padding the review with maybes to look
      thorough.
    - Source transparency (weight 1.0) = cites file + function/line for the flaw.
    - Format adherence (weight 1.5) = the output envelope plus the
      verdict-on-first-line structure.

    THE HEADLINE METRIC IS WITHIN-FAMILY SPREAD across the 5 runs per model: the
    hit-rate (of 5 runs, how many correctly identified the planted SQL injection
    with zero false alarms) and the weighted-total spread (max minus min). A model
    that goes 5/5 with tight spread is consistent on the buried item; a model that
    goes 3/5, or that swings between catching the injection and flagging a decoy,
    is the inconsistent profile this eval is built to expose. Voice match does not
    apply.
---

# Spec 46 - buried-security-issue (catch-the-one-flaw consistency probe)

A HEAVY consistency battery. One large pull request (PR-4471 for the fictional
"Northwind" orders service) contains exactly ONE genuine security vulnerability
buried among nine benign hunks and five security-adjacent-but-SAFE decoys. The
review task is to deliver a merge verdict, pinpoint the one real flaw, name its
class, explain the exploit, and give the minimal fix - while NOT raising a false
alarm on any of the safe-but-scary-looking changes.

The corpus (`corpus/buried-security-issue/`) is a 10-file PR delivered three ways
for full context: the authoritative `PR-4471.diff`, the post-change `after/` tree,
and the pre-change `before/` tree (33 files total). The planted flaw is a SQL
injection in `northwind/db/queries.py` `OrderQueries.search`: the WHERE clause is
correctly parameterised (a deliberate red herring of safety, reinforced by an
inline "never inlined" comment), but the ORDER BY is assembled with an f-string
that interpolates the user-controlled `sort` query parameter (`sort_column`) with
no validation - and the `ALLOWED_SORTS` whitelist defined in `api/search.py` is
never actually applied. The decoys (a correct constant-time token compare, a
normal bcrypt cost bump, a parameterised statement-timeout, an Authorization-header
redaction, a dependency UPGRADE) all touch security and are all safe.

This is run at `variant_pool: 15` (5 runs per model, model-only, effort inert).
The scored headline is WITHIN-FAMILY SPREAD: per model, the hit-rate across the 5
runs (correct injection identification with zero false alarms) and the
weighted-total spread. Run-to-run reliability on the single buried item - whether a
model catches it EVERY run or only on its good runs - is the separator, per the
batch-3 consistency read. Correctness-first applies: a confidently-wrong "this safe
change is insecure" verdict is penalised harder than a miss, because a reviewer
acts on it. Standard four-phase `/eval-pit` flow against the frozen
`rubric/rubric.md`.
