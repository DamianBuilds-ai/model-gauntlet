---
task_category: cross-domain-kb-write
prompt_under_test: |
  You are given four files in corpus/cross-domain-kb-write/:

    - shared-findings-schema.md - the column schema for a shared cross-domain findings
      table (the fictional "Confluence" table).
    - QUILL.md - the trunk reference doc for the fictional "Quill" domain.
    - HOLLOWMERE.md - the trunk reference doc for the fictional "Hollowmere" domain.
    - finding-to-record.md - a cross-domain finding that must be recorded.

  Record the finding to ALL THREE write surfaces, keeping it CONSISTENT across all
  three (no drift):

    1. SHARED TABLE ROW: produce one new row for the findings table, with every required
       column filled correctly per the schema (domain, category, finding, date,
       related_domains, status). The category and status MUST be valid values from the
       schema's allowed single-select sets.
    2. HOLLOWMERE.md UPDATE: add the finding to the discovering domain's doc, under its
       "## Infrastructure notes" (and correct any now-stale line there).
    3. QUILL.md UPDATE: add the finding to the affected domain's doc, under its
       "## Known cross-domain dependencies" (reflecting the downstream effect on Quill).

  The finding's substance must read the SAME across all three surfaces (same change,
  same affected domains, same date). Do NOT invent any detail not in finding-to-record.md.
  Where HOLLOWMERE.md currently states the render-cache is "in-process per worker", that
  line is now STALE - update it to reflect the move to shared Redis.

  Output THREE clearly-labelled blocks:
    1. "=== SHARED FINDINGS ROW ===" then the row as a markdown table row.
    2. "=== UPDATED HOLLOWMERE.md ===" then the full updated file in a fenced block.
    3. "=== UPDATED QUILL.md ===" then the full updated file in a fenced block.
  Then the output envelope (schemaVersion, tier, status, tool_budget_used) on separate
  lines OUTSIDE the blocks. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/cross-domain-kb-write/
corpus_intent: |
  Four files. The schema (allowed category set {infra, model, decision, bugfix,
  security}; allowed status set {active, resolved, superseded}; 6 required columns), the
  two domain trunks (QUILL.md, HOLLOWMERE.md), and the finding to record. Mirrors
  a personal-ops cross-domain write (a shared-findings row + both domain docs) on the
  fictional Quill/Hollowmere domains (codename hygiene mandatory; no real domain names).
  The eval probes a CONSISTENT write across three surfaces with no drift, valid
  single-select values, and the correction of one now-stale line.

  QUALITY PRINCIPLE (correctness-first): the load-bearing requirement is CONSISTENCY -
  the same finding, same affected domains, same date must appear at all three surfaces.
  A write where the row says "Redis" but a doc still says "in-process", or where the
  related_domains differ between row and docs, is a confidently-wrong drift - worse than
  a write that is verbose but consistent. A second hard requirement is fixing the STALE
  HOLLOWMERE line ("in-process per worker") rather than leaving the doc self-contradictory.

  ANSWER KEY (exact expected end-state):

    THE FINDING: the Hollowmere render-cache MOVED from in-process to a shared Redis
    instance, best-effort with fall-through to a live render on miss/outage; this means
    the cache survives Hollowmere deploys, so Quill no longer sees post-deploy cold-start
    slowness.

    SHARED FINDINGS ROW (every column, exact values):
      - domain = Hollowmere (the discovering domain).
      - category = infra (MUST be a valid single-select; "infra" is in the allowed set).
        NOTE: "decision" is also defensible, but the finding-to-record.md states
        "category is infra" - so infra is the keyed-correct value. Using a value OUTSIDE
        the allowed set (e.g. "infrastructure", "redis", "deploy") is WRONG.
      - finding = render-cache moved to shared Redis (best-effort, fall-through), survives
        deploys. (one or two sentences, matching the finding.)
      - date = 2026-05-22 (today's date stated in finding-to-record.md). Must be YYYY-MM-DD.
      - related_domains = Hollowmere, Quill (both affected domains; order not scored).
      - status = active (a valid single-select; the finding is active).

    UPDATED HOLLOWMERE.md:
      - "## Infrastructure notes" now records the render-cache is on shared Redis
        (best-effort, fall-through) AND the STALE line "The render-cache is currently
        in-process per worker." is CORRECTED/removed (no longer says in-process).
      - "Hollowmere owns the render-cache subsystem." line preserved.
      - "## Known cross-domain dependencies" section preserved.

    UPDATED QUILL.md:
      - "## Known cross-domain dependencies" now reflects the downstream effect: the
        Hollowmere render-cache is on shared Redis and survives deploys, so Quill no
        longer hits post-deploy cold-start slowness.
      - The pre-existing dependency line and "## Infrastructure notes" preserved.

  GREP-VERIFIABLE INVARIANTS (for the scoring Architect):
    - SHARED FINDINGS ROW: contains "Hollowmere" as domain, a category that is EXACTLY
      one of {infra, model, decision, bugfix, security} (keyed value: infra), status
      EXACTLY one of {active, resolved, superseded} (keyed value: active), date
      "2026-05-22", and related_domains naming BOTH "Hollowmere" AND "Quill".
    - "Redis" appears in ALL THREE blocks (row, HOLLOWMERE.md, QUILL.md) - consistency.
    - In UPDATED HOLLOWMERE.md: the literal stale phrase "in-process per worker" does NOT
      remain as a current-state claim (it is corrected). (Stale-line trap.)
    - In UPDATED QUILL.md: "cold-start" or "survives deploys" appears (downstream effect
      captured) AND "Redis" appears.
    - "2026-05-22" appears in the row (date consistency); no other date invented.
    - related_domains in the row == the two domains referenced in both docs (no drift:
      not a third invented domain).
    - No category/status value outside the schema's allowed sets.

  Scoring guidance:
    - Correctness (hard-fail eligible) = the finding is consistent across all three
      surfaces, schema values are valid, the stale line is fixed.
    - Completeness = all three surfaces written; all 6 row columns filled.
    - Hallucination (hard-fail eligible) = inventing a domain, a date, a category/status
      outside the allowed set, or a detail not in finding-to-record.md.
    - Discipline = three labelled blocks; other doc content preserved; no extra surfaces.
    - Format adherence = labelled blocks + envelope outside.
    - Voice match does NOT apply.
notes: |
  CHAT C domain-realistic personal-ops eval. Mirrors a personal-ops cross-domain write
  (shared-findings row + both affected domain docs) on the fictional Quill/Hollowmere
  domains (codename hygiene mandatory). Probes a CONSISTENT three-surface write with no
  drift: a valid findings-table row (category/status from the allowed single-select
  sets, both related_domains, today's date), plus updates to both domain trunks. Two
  load-bearing requirements: (1) consistency - "Redis" and the same affected domains and
  date appear at all three surfaces; (2) fixing the now-stale HOLLOWMERE line ("in-process
  per worker") so the doc is not self-contradictory after the write. Traps: drifting the
  related_domains, using a category/status outside the schema set, or leaving the stale
  line. Correctness and Hallucination are hard-fail eligible. The answer key gives exact
  values and grep invariants. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. variant_pool 9 (3 models x N=3, effort inert). Corpus is the
  directory corpus/cross-domain-kb-write/.
---

# Spec 85 - cross-domain-kb-write

Given a shared-findings table schema, two fictional domain trunk docs (QUILL.md,
HOLLOWMERE.md), and a cross-domain finding to record, write the finding to all three
surfaces and keep it consistent. This mirrors a personal-ops cross-domain knowledge-write
step (a shared findings row plus both affected domain docs) on the neutral fictional
Quill and Hollowmere domains so no real codename leaks.

The finding: the Hollowmere render-cache moved from in-process to a shared Redis
instance, best-effort with fall-through to a live render, so it now survives deploys and
Quill no longer suffers post-deploy cold-start slowness. The three writes are a fully
populated findings-table row (with a category and status drawn from the schema's allowed
single-select sets, both affected domains in related_domains, and today's date), an
update to the discovering domain's doc (Hollowmere), and an update to the affected
domain's doc (Quill).

Two requirements are load-bearing. First, consistency: the same change, the same pair of
affected domains, and the same date must appear at all three surfaces - a row that says
Redis while a doc still says in-process is confidently-wrong drift. Second, the stale
line: HOLLOWMERE.md currently claims the render-cache is "in-process per worker", which
this change makes false, so the write must correct it rather than leave the doc
self-contradictory. The schema also constrains the category and status to fixed
single-select sets; a value outside those sets is an error.

Correctness and Hallucination are hard-fail eligible; Discipline covers using exactly
the three required write surfaces and preserving the other doc content. The answer key in
corpus_intent gives the exact values for the row, the expected doc edits, and
grep-verifiable invariants for the scoring Architect. Voice match does not apply. Standard
four-phase /eval-pit flow against the frozen rubric/rubric.md. The variant pool is 9 (3
models x N=3, effort inert per the methodology). The corpus is the directory
corpus/cross-domain-kb-write/.
