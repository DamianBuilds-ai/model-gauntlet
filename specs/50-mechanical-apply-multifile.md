---
task_category: mechanical-apply-multifile
prompt_under_test: |
  You are given a small set of files under corpus/mechanical-apply-multifile/ for a
  fictional service (platform "Northwind", company "Globex"):

    - version.txt   - a single version string
    - config.ini    - an INI config with [server] and [logging] sections
    - CHANGELOG.md   - a keep-a-changelog style file, newest entry first
    - hosts.csv     - a CSV of hosts (header: hostname,role,region)
    - notes.txt     - scratch notes (a DECOY - see the spec; do not edit it)

  Apply the following change specification across these files EXACTLY. These are
  precise, deterministic edits. There is exactly one correct end-state. Apply ONLY what
  is listed, in the files named. Do NOT reformat, reorder, or normalise anything the
  spec does not name, and do NOT edit any file the spec does not name.

  CHANGE SPECIFICATION (apply all five):

    C1. version.txt - SET the version from `1.4.2` to `1.5.0`. The file must contain
        exactly the new version string (same single-line, trailing-newline shape as the
        original).

    C2. config.ini, [server] section - SET `port = 8080` to `port = 9090`. Change ONLY
        that value. Leave host, workers, and timeout_seconds unchanged.

    C3. config.ini, [logging] section - INSERT a new line `audit = true` as the LAST
        line of the [logging] section (after `retention_days = 7`). Do not change the
        existing logging lines.

    C4. CHANGELOG.md - INSERT a new release section for version `1.5.0` ABOVE the
        existing `## 1.4.2` section (newest-first order), with exactly this content:

          ## 1.5.0

          - Moved the server port to 9090.
          - Added audit logging.

        Leave the existing `## 1.4.2` and `## 1.4.1` sections unchanged.

    C5. hosts.csv - APPEND one new data row as the LAST line: `nw-app-03,app,ap-southeast`.
        Keep the header and existing rows unchanged.

    DO NOT EDIT notes.txt. It is a decoy: it mentions the old version `1.4.2` and the
    old port `8080` in passing, but the spec does not list it, so it must be left
    byte-identical. Bumping the version or port inside notes.txt is an over-reach error.

  Output the COMPLETE updated content of EACH file that genuinely changes (version.txt,
  config.ini, CHANGELOG.md, hosts.csv), each as its own clearly-labelled fenced code
  block with its path. Then provide a short per-file checklist covering ALL FIVE listed
  files: for each, state whether it changed and what changed, or that it did not change
  and why (notes.txt = decoy, not listed). After the checklist, append the required
  output envelope (schemaVersion, tier, status, tool_budget_used) on separate lines. No
  em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/mechanical-apply-multifile/
corpus_intent: |
  Five files under corpus/mechanical-apply-multifile/ (version.txt, config.ini,
  CHANGELOG.md, hosts.csv, and a decoy notes.txt) modelling a coordinated release bump.
  The eval asks for an exact deterministic apply of five edits across FOUR of the files
  (version set, config value set, config line insert, changelog section insert, CSV row
  append) while leaving the fifth file (the decoy notes.txt, which contains the old
  version and old port in passing) byte-identical. There is one correct end-state.

  THE SETTER TEST AT SLIGHTLY MORE SCOPE (Haiku-lightweight-apply vs Sonnet-Builder).
  Spec 49 tested a fully-specified apply in ONE file; this spec spreads the same
  one-correct-answer determinism across SEVERAL files plus a precision decoy. The
  hypothesis: on a multi-file deterministic apply where every edit is named, Haiku
  should still match Sonnet (the edits require no inference). The failure mode to detect
  is whether the slightly larger surface tips Haiku into confidently-wrong behaviour -
  editing the decoy because it contains the old version/port string, missing one of the
  five edits, mis-placing the changelog section (below instead of above), or reformatting
  a file - where Sonnet holds all five exact and leaves the decoy alone.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a multi-file apply that LOOKS
  done but edited the decoy or mis-placed a section is WORSE than one that honestly
  applies four of five and flags the fifth. The highest-signal traps: (a) bumping the
  version `1.4.2` -> `1.5.0` or the port `8080` -> `9090` INSIDE notes.txt because the
  old strings appear there - this is the canonical over-reach (a global find-replace
  would hit it; the correct apply is file-scoped); (b) inserting the new `## 1.5.0`
  changelog section BELOW `## 1.4.2` instead of above (the file is newest-first); (c)
  inserting `audit = true` into the wrong section ([server] instead of [logging]) or
  changing an unrelated config value; (d) editing the CSV header or an existing row
  instead of appending. A model that applies exactly the five named edits in the four
  named files and leaves notes.txt byte-identical is correct; a blind find-replace that
  also rewrites the decoy is confidently wrong.

  ANSWER KEY (for the scoring Architect - the exact end-state). Verify by comparing each
  produced file line-by-line against its original.

    version.txt AFTER: contains exactly `1.5.0` (was `1.4.2`).

    config.ini AFTER: [server] has host=0.0.0.0, port=9090 (changed from 8080),
    workers=4, timeout_seconds=30. [logging] has level=info, format=json,
    retention_days=7, AND a new last line audit=true. No other value changed.

    CHANGELOG.md AFTER: a new `## 1.5.0` section sits ABOVE `## 1.4.2`, containing the
    two bullets "Moved the server port to 9090." and "Added audit logging." The existing
    `## 1.4.2` (two bullets) and `## 1.4.1` (one bullet) sections are unchanged and still
    in newest-first order: 1.5.0, then 1.4.2, then 1.4.1.

    hosts.csv AFTER: header unchanged (hostname,role,region), the three original rows
    unchanged, and a new last row `nw-app-03,app,ap-southeast`. Four data rows total.

    notes.txt AFTER: BYTE-IDENTICAL to the original. It still says `1.4.2` and `8080`.
    Editing it is an over-reach error.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - version.txt is exactly `1.5.0`. The token `1.4.2` does NOT appear in version.txt.
    - `1.4.2` STILL appears in CHANGELOG.md (the historical 1.4.2 section is kept) and
      STILL appears in notes.txt (decoy unchanged). It must NOT have been deleted from
      either.
    - In config.ini: `port = 9090` appears once, `port = 8080` appears zero times,
      `audit = true` appears once and is under [logging].
    - In CHANGELOG.md the section order top-to-bottom is `## 1.5.0`, `## 1.4.2`,
      `## 1.4.1`.
    - hosts.csv has exactly 4 data rows plus the header; `nw-app-03` appears once.
    - notes.txt is unchanged: it still contains `1.4.2` and `8080` (the apply was
      file-scoped, not a global find-replace).

  Scoring guidance:
    - Correctness (hard-fail eligible) = all five edits applied exactly in the four named
      files AND the decoy untouched. Editing notes.txt, mis-placing the changelog section,
      inserting audit into the wrong section, or changing an unrelated value is
      Correctness=1 (a confidently-wrong multi-file apply).
    - Completeness = all five of C1-C5 present and a checklist covering all five files.
    - Hallucination (hard-fail eligible) = editing the decoy notes.txt, inventing a sixth
      edit, adding a changelog bullet not in the spec, or claiming a file is unchanged when
      it was edited (or vice versa).
    - Format adherence = each changed file as its own labelled fenced block + the per-file
      checklist + envelope outside.
    - Discipline = applied ONLY the five named edits in ONLY the four named files, left the
      decoy and all unrelated lines byte-identical. This is the load-bearing Setter
      discriminator: a file-scoped apply, not a global find-replace.
    - Reasoning quality = SKIP-eligible; if shown, the in-scope/out-of-scope (decoy)
      distinction should be correct.
    - Source transparency = the checklist correctly maps each of the five files to its
      change or to the reason it did not change.
    Voice match does NOT apply. The scored discriminators are exact application of the
    five edits across the four files and ZERO over-reach onto the decoy or unrelated lines.
notes: |
  NEW task type and the second of the three Setter-vs-Builder probes (49-51). Spec 49
  tested a fully-specified deterministic apply in ONE file; this spec spreads the same
  one-correct-answer determinism across SEVERAL files - a coordinated release bump
  (version set, config port set, config line insert, changelog section insert, CSV row
  append) - plus a precision decoy (notes.txt) that contains the old version and old port
  in passing and must be left byte-identical. The question is whether the slightly larger
  surface still lets Haiku match Sonnet on a fully-deterministic multi-file apply, or tips
  it into confidently-wrong behaviour: editing the decoy via a global find-replace,
  mis-placing the changelog section, inserting into the wrong config section, or missing
  one of the five edits, where Sonnet holds all five exact and leaves the decoy alone.

  The corpus (corpus/mechanical-apply-multifile/) is five small files in four formats
  (plain version string, INI, keep-a-changelog Markdown, CSV, plus the decoy text file).
  The canonical trap is the over-reach: bumping `1.4.2` or `8080` inside notes.txt because
  the old strings appear there - the correct apply is file-scoped, not a global
  find-replace. Secondary traps: changelog section placed below instead of above
  (newest-first), audit line inserted into [server] instead of [logging], or a CSV header
  / existing row edited instead of appended. The correctness-first principle holds: a
  confidently-wrong multi-file apply (decoy edited, section mis-placed) is worse than an
  honest partial. Correctness and Hallucination are hard-fail eligible; Discipline (a
  file-scoped apply touching only the four named files) is the load-bearing discriminator.
  The answer key gives the exact per-file end-state plus grep-verifiable invariants. Voice
  match does not apply. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert per the
  methodology). The corpus is the directory corpus/mechanical-apply-multifile/.
---

# Spec 50 - mechanical-apply-multifile (the Setter test at multi-file scope)

Apply a set of precise, fully-specified edits across several files exactly - set a
version string, set one config value, insert one config line, insert one changelog
section in the right place, append one CSV row - while leaving an unrelated decoy file
byte-identical. This is the second of three Setter-vs-Builder probes (49 exact-single
file, 50 exact-multifile, 51 patch-application).

A "Setter" is Damian's term for a lightweight write/apply agent (Haiku) that applies a
fully-specified change after a Scout retrieves, as opposed to the Builder (Sonnet,
execution plus verification). Spec 49 located whether the Setter is safe on a
fully-deterministic apply in one file; this spec asks the same question at slightly
more scope - the same one-correct-answer determinism spread across several files plus a
precision decoy. The hypothesis is that named, inference-free edits should still let
Haiku match Sonnet; the failure mode to detect is whether the larger surface tips Haiku
into a global find-replace that rewrites the decoy, a mis-placed changelog section, a
wrong-section config insert, or a missed edit, where Sonnet keeps the apply file-scoped
and exact.

The corpus (`corpus/mechanical-apply-multifile/`) is five small files - a version
string, an INI config, a keep-a-changelog Markdown file, a CSV, and a decoy
`notes.txt`. The five edits (C1 version 1.4.2 to 1.5.0, C2 port 8080 to 9090, C3 insert
`audit = true` under [logging], C4 insert a `## 1.5.0` changelog section above 1.4.2,
C5 append a CSV host row) each have exactly one correct result. The canonical trap is
over-reach: `notes.txt` contains the old version and old port in passing, so a blind
global find-replace would wrongly edit it - the correct apply is file-scoped. Secondary
traps are the changelog section placed below instead of above, the audit line inserted
into the wrong section, and a CSV header or existing row edited instead of appended.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle holds: a confidently-wrong multi-file apply (the
decoy edited, a section mis-placed, a wrong value changed) is worse than an honest
partial that applies four of five and flags the fifth. Correctness and Hallucination
are hard-fail eligible; Discipline - a file-scoped apply that touches only the four
named files and leaves the decoy and all unrelated lines byte-identical - is the
load-bearing discriminator, and the answer key provides the exact per-file end-state
plus grep-verifiable invariants for the scoring Architect. Voice match does not apply.
The variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is
the directory `corpus/mechanical-apply-multifile/`.
