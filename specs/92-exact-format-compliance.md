---
task_category: exact-format-compliance
prompt_under_test: |
  You are given a single source file at
  corpus/exact-format-compliance/release-data.md - it lists five fictional software
  releases in free-form prose, plus an EXACT output template that a brittle downstream
  parser requires.

  Convert the five releases into the exact single-line record format defined in the
  source file. Output EXACTLY five lines, one per release, in the order the releases
  are listed in the source.

  The format for each line is, verbatim:

    REL-<id> | <name> | <owner> | <status> | <date>

  Rules (the parser is strict - any deviation breaks the import):
    - Fields separated by " | " (space, pipe, space). No leading or trailing pipe.
    - <id> is the digits only, prefixed with REL- (e.g. REL-4471).
    - <name> is the release name only (no quotes).
    - <owner> is the team name (e.g. "storage team").
    - <status> is exactly one of: shipped, rolled-back, partial.
    - <date> is YYYY-MM-DD (you must normalise the prose dates to this format).

  Output ONLY the five lines. No header, no title, no intro sentence, no trailing
  comment, no blank line before or after, no code fence, no explanation. After the
  five lines, append the output envelope (schemaVersion, tier, status,
  tool_budget_used) as separate lines. No em dashes. No emojis.
variant_pool: 9
corpus: corpus/exact-format-compliance/
corpus_intent: |
  One source file (corpus/exact-format-compliance/release-data.md): five releases stated
  in deliberately varied free-form prose (dates written four different ways, names in
  quotes, owners as "the X team", statuses phrased differently - "shipped", "was rolled
  back", "partial rollout finished"). The task demands a byte-exact single-line record
  format with positional pipe-delimited fields, ordered, with normalised dates. The corpus
  is salted with TEMPTATION TO ADD PROSE: a "Background" section, an explicit "notes the
  team usually adds" block, and a stated history of people pasting helpful explanations
  that break the parser. A disciplined model emits exactly five lines and nothing else; an
  undisciplined one prepends a "Here are the records:" header, wraps in a code fence, or
  appends one of the tempting notes.

  THE FORMAT IS THE ANSWER KEY. The five correct lines are EXACTLY (byte-level):
    REL-4471 | Aurora | storage team | shipped | 2026-03-14
    REL-4472 | Borealis | network team | rolled-back | 2026-03-12
    REL-4473 | Cascade | storage team | shipped | 2026-03-19
    REL-4474 | Drift | identity team | partial | 2026-03-22
    REL-4475 | Ember | network team | shipped | 2026-03-27

  Note the normalisations that test care: 4472's "rolled back" -> the enum token
  "rolled-back" (hyphen, lowercase); 4474's "partial rollout finished" -> "partial";
  every prose date normalised to YYYY-MM-DD ("2026 March 14" -> 2026-03-14; "12 March
  2026" -> 2026-03-12; "the 27th of March 2026" -> 2026-03-27).

  QUALITY PRINCIPLE (format-first): the value of this output is that a brittle parser can
  read it. A line that is "almost right" but has a trailing pipe, a leading "Here are
  the records:" header, a code fence, an extra blank line, or a stray helpful note is a
  FAIL even if the data is correct - because it breaks the import. Exact-format compliance
  is the whole task; richer/friendlier output is worse, not better.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The output body is EXACTLY five lines matching the regex
      `^REL-[0-9]{4} \| [A-Za-z]+ \| [a-z]+ team \| (shipped|rolled-back|partial) \| [0-9]{4}-[0-9]{2}-[0-9]{2}$`
      (the envelope lines are separate, after the five).
    - No code fence (```), no markdown header (#), no "Here are" / "records:" / colon-led
      intro line, no blank line between records, no leading/trailing pipe on any line.
    - Each date matches `[0-9]{4}-[0-9]{2}-[0-9]{2}`; the four prose-date formats are all
      normalised. The status field uses ONLY the three enum tokens, hyphenated/lowercase.
    - None of the "notes the team usually adds" bullets (Aurora-was-the-big-one, DNS bug,
      ping the data team) appears anywhere in the output - DISCIPLINE FAIL if any does.

  Scoring guidance:
    - Format adherence (hard-fail eligible, LOAD-BEARING) = five lines, exact delimiter,
      exact field order, no header/fence/blank/extra-prose, dates normalised. Any
      structural deviation = Format 1.
    - Correctness = each field value matches the source (right name, owner, status enum,
      normalised date).
    - Completeness = all five releases present, in source order.
    - Discipline = no added prose, header, fence, or tempting note. Load-bearing alongside
      Format.
    - Hallucination (hard-fail eligible) = inventing a sixth release, a field value not in
      the source, or appending a note as if it were a record.
    - Reasoning quality = SKIP-eligible. Voice match does NOT apply.
notes: |
  NEW output-discipline eval (Chat D battery, 91-96). Probes exact-format compliance: can
  a model emit a byte-exact, positional, pipe-delimited record format with NOTHING extra,
  when the source naturally tempts it to add a header, a code fence, or a "helpful note".
  The corpus states a brittle downstream parser and explicitly lists the prose notes that
  "usually get added and break the import" - the temptation is baked in. It also tests
  careful normalisation: four different prose date formats must all become YYYY-MM-DD, and
  loose status phrasings must map to three exact enum tokens (shipped / rolled-back /
  partial).

  The load-bearing discriminators are Format adherence (exactly five lines, exact
  delimiter and order, no header/fence/blank/extra-prose) and Discipline (no tempting note
  leaks into the output). An "almost right" line with a trailing pipe or a friendly intro
  header is a FAIL because it breaks the parser - richer output is worse, not better. The
  answer key in corpus_intent gives the five exact lines plus a line-matching regex and the
  list of notes that must NOT appear. Hallucination is hard-fail eligible; reasoning is
  skip-eligible; voice does not apply. Standard four-phase /eval-pit flow against the
  frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert per the
  methodology). The corpus is the directory corpus/exact-format-compliance/.
---

# Spec 92 - exact-format-compliance

Convert five free-form release descriptions into a byte-exact, pipe-delimited,
positional single-line record format that a brittle downstream parser requires - and
emit NOTHING else. The catch: the source file is salted with a "Background" section
and an explicit block of "notes the team usually adds", and it states outright that
people keep breaking the parser by pasting helpful explanations. The temptation to
add a header, wrap the output in a code fence, or append a friendly note is built in.

This is an exact-format-compliance probe. The corpus
(`corpus/exact-format-compliance/release-data.md`) also tests careful normalisation:
the five dates are written four different ways and must all become YYYY-MM-DD, and the
loose status phrasings ("was rolled back", "partial rollout finished") must map to the
three exact enum tokens. A disciplined model produces exactly five lines in the
template, in source order, with normalised fields, and stops.

The load-bearing discriminators are Format adherence (five lines, exact delimiter and
field order, no header / code fence / blank line / extra prose) and Discipline (none of
the tempting "usually added" notes leaks in). A line that is "almost right" but carries
a trailing pipe, a "Here are the records:" intro, or a code fence is a FAIL - it breaks
the parser, so richer output is worse, not better. The answer key in `corpus_intent`
gives the five exact lines, a per-line regex, and the explicit list of notes that must
not appear. Hallucination is hard-fail eligible; reasoning is skip-eligible; voice does
not apply. Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`.
The variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is
the directory `corpus/exact-format-compliance/`.
