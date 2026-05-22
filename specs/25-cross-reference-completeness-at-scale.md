---
task_category: cross-reference-completeness-at-scale
prompt_under_test: |
  You are given a synthetic codebase for a fictional notification system "Northwind
  Relay" under corpus/cross-reference-completeness-at-scale/. The deprecated function
  legacy_render_template(payload, locale) (defined in src/templates/legacy.py) is
  being retired in favour of the new TemplateEngine.render(payload, locale, *, strict)
  in src/templates/engine.py.

  Produce a COMPLETE migration checklist of EVERY location in the codebase that
  references the deprecated legacy_render_template and must change for the migration.
  Miss nothing. For each location:
    1. Cite the file path AND the line number (or the function / section the
       reference sits in if a line number is unavailable).
    2. State the KIND of reference: definition site, direct call, import line,
       re-export, aliased import or aliased call, wrapper, indirect-via-wrapper,
       or test.
    3. Note one word on what the migration must do there (repoint, replace call,
       update import, delete, etc.).

  Rules:
    - Include INDIRECT references: a re-export, an import bound to an alias and the
      call made through that alias, a wrapper function that forwards the call and
      the callers that go through the wrapper. These all reference the deprecated
      function (directly or transitively) and must be on the checklist, flagged with
      the correct kind.
    - Do NOT include false positives. A reference that is commented-out / dead code
      is NOT a live location requiring a code change. A DIFFERENT function with a
      similar name is NOT the target. A docstring that only NAMES the function as
      "the thing being replaced", with no call, is not a live call site. If you list
      something that is not a true live reference to legacy_render_template, that is a
      precision error and counts against you.
    - A confidently-wrong entry (a false positive, or a real location described with
      the wrong kind) scores WORSE than an omission. Completeness and zero false
      positives are the whole point.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/cross-reference-completeness-at-scale/
corpus_intent: 20 interlinked Python modules (packages relay, channels, reports, templates, api) with one deprecated render function referenced across many of them - some direct, some buried in long files, some indirect via alias or wrapper, plus planted precision traps
corpus_delivered: TBD
corpus_match: TBD
notes: |
  OPUS-SEPARATION PROBE AT SCALE (cross-reference load / forgetting-under-load). This
  is the SCALED version of spec 22. Spec 22 spread one deprecated function across 16
  files; this corpus spreads ONE deprecated function (legacy_render_template) across 20
  interlinked modules in five packages (relay, channels, reports, templates, api), with
  MORE indirection layers and MORE distractors. The hypothesis is the same as spec 22
  but cranked: at this scale the cheaper models start to (a) DROP true locations
  (recall failure, especially the buried-deep and the indirect-via-wrapper ones), or
  (b) INVENT / mis-classify locations (precision failure, especially the four planted
  traps). The whole point is to find where Opus's completeness advantage finally
  separates it from Sonnet under heavier cross-reference load than spec 22 imposed.

  Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3; effort treated
  as inert per the methodology). Aggregate the 3 passes per model (mean weighted
  total); flag any model whose 3 passes diverge by more than 0.5 as a consistency
  finding. Compare the practical winner here against spec 22's practical winner to
  locate whether the threshold where Opus pulls ahead sits between spec-22 scale and
  this scale.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong entry is
  worse than a missed one. A model that lists the commented-out dead call as a live
  location, or lists the similarly-named legacy_render_template_preview as a target,
  has put a wrong item on a migration checklist that an engineer would trust and act
  on - worse than quietly missing one real location. Reward exact recall AND clean
  precision. Penalise the false positive hardest. Flag any "confidently wrong" output
  for an extra penalty.

  ANSWER KEY (for the scoring Architect). The corpus was salted via grep so this list
  is exact and line-accurate. There are 22 TRUE reference ENTRIES below (A1-A8,
  B1-B4, C1-C10). The entries split into three tiers by how hard they are to find -
  the discriminator is whether a model holds ALL of them, especially the INDIRECT
  ones, without dropping any and without adding the four traps.

  TIER A - obvious / direct (8 entries; every model should get these):
    A1. src/templates/legacy.py line 11 - DEFINITION SITE of legacy_render_template
        (the function being removed). Migration: delete after all callers gone.
    A2. src/api/webhooks.py line 7 - import line. Migration: update import.
    A3. src/api/webhooks.py line 14 - direct call in handle_event (ack render, hot
        path). Migration: replace call.
    A4. src/channels/email.py line 6 - import line. Migration: update import.
    A5. src/channels/email.py line 12 - direct call in build_email. Migration:
        replace call.
    A6. src/relay/dispatch.py line 14 - import line at top of the long dispatch
        module. Migration: update import.
    A7. src/relay/dispatch.py line 78 - direct call in _handle_unknown, buried deep
        in the fallback path of the long orchestration file (LIVE CALL). Migration:
        replace call. This is the canonical "buried in a long file" drop candidate.
    A8. src/templates/__init__.py line 9 - re-export import of the deprecated fn
        (also named in __all__ on line 11; accept either the line-9 import, the
        line-11 __all__ entry, or both cited as one re-export location - do NOT
        double-penalise, but a model that misses the re-export entirely drops a real
        downstream-breaking location). Migration: update / remove re-export.

  TIER B - buried in long files (4 entries; weaker models start dropping these):
    B1. src/reports/weekly.py line 9 - import line at top of a long report module.
        Migration: update import.
    B2. src/reports/weekly.py line 34 - call buried in the middle inside
        _render_sample_appendix. Migration: replace call. A model that skims the long
        report file drops this.
    B3. src/channels/shared.py line 8 - import line for the wrapper module.
        Migration: update import.
    B4. src/channels/shared.py line 13 - call inside the wrapper render_channel_body
        that forwards to the deprecated fn. Migration: replace call (or retarget the
        wrapper). This is the wrapper SOURCE; the two indirect-via-wrapper callers
        (C7-C10) reach the deprecated behaviour only through it.

  TIER C - indirect / aliased / via-wrapper (the OPUS separators; 10 entries across
  alias, two wrapper-caller chains - these are where cross-reference load bites
  hardest):
    C1. src/channels/sms.py line 7 - ALIASED import
        (legacy_render_template as _render). Migration: update import.
    C2. src/channels/sms.py line 14 - ALIASED call site reading _render (the literal
        name does not appear at the call). Migration: replace call. A model that
        searches only for the literal name misses this.
    C3. src/channels/push.py line 7 - import of the wrapper render_channel_body.
        INDIRECT-via-wrapper. Migration: depends on strategy; must be listed and
        flagged indirect.
    C4. src/channels/push.py line 12 - call to render_channel_body in build_push.
        INDIRECT-via-wrapper. Must be listed and flagged indirect (push reaches the
        deprecated behaviour only through the shared wrapper).
    C5. src/reports/audit.py line 8 - import of the wrapper render_channel_body.
        INDIRECT-via-wrapper. Migration: depends on strategy; must be listed and
        flagged indirect.
    C6. src/reports/audit.py line 14 - call to render_channel_body in
        build_audit_entry. INDIRECT-via-wrapper. Must be listed and flagged indirect.
    C7. src/channels/__init__.py line 3-5 - re-export of deliver_email / deliver_sms
        / deliver_push (the channel functions that internally render via the
        deprecated fn). Accept the package init cited once as a re-export location
        that surfaces the rendering channels; a model that lists it must flag it as a
        re-export of the rendering channels, NOT as a direct call site. (Borderline
        entry - see scoring note: not double-penalised if omitted, but a strong
        answer that traces the package surface mentions it.)
    C8. src/relay/__init__.py line 2-4 - re-export of Dispatcher (whose
        _handle_unknown calls the deprecated fn at A7). Same borderline treatment as
        C7: a strong answer notes the package surface re-exports the class that
        carries a live call; not double-penalised if omitted.
    C9. src/templates/engine.py - DOCSTRING-ONLY references (lines 3, 15 name
        legacy_render_template as "the thing it replaces"). This is the
        DISCIPLINE-flag entry: a strong answer EXPLICITLY notes engine.py contains
        only doc mentions and NO live call, so it is NOT a migration code-change site.
        Listing engine.py as a live call location is a precision error (see TRAP-3).
        Accept either "engine.py - doc-only, excluded" as a disciplined exclusion OR
        silence; do NOT reward listing it as a live call.
    C10. src/templates/__init__.py line 4 - the docstring line naming the
        re-export's removal. Tied to A8 (the actual re-export on lines 9/11); a model
        that cites A8 has covered the live surface. Borderline; not double-penalised.

  NOTE on C7/C8/C10 (borderline package-surface entries): these are graded LENIENTLY.
  The 20 LOAD-BEARING entries are A1-A8, B1-B4, C1-C6, plus the C9 disciplined
  EXCLUSION of engine.py. A model is scored primarily on those 19 live entries + the
  one disciplined exclusion. C7/C8/C10 are credit-if-present, never-penalise-if-absent
  package-surface observations that distinguish an exemplary 5 from a strong 4 on
  Reasoning quality. The recall denominator for Completeness scoring is the 18 LIVE
  code-change entries (A1-A8, B1-B4, C1-C6).

  PRECISION TRAPS (must NOT appear on the checklist as live migration locations -
  listing any is a confidently-wrong false positive and the heaviest penalty):
    TRAP-1. src/relay/dispatch.py line 86 - a COMMENTED-OUT call to
        legacy_render_template inside render_digest. Dead code. NOT a live location.
        A model that lists it has put a no-op item on the migration checklist.
    TRAP-2. legacy_render_template_preview (defined src/templates/legacy.py line 25;
        imported and called in src/api/admin.py lines 9 and 14). A DIFFERENT function
        (a 120-char preview helper for the admin UI, takes no locale, NOT being
        retired) with a confusingly similar name. NOT the migration target. Listing
        it - or listing admin.py as a migration site - is a precision error.
    TRAP-3. src/templates/engine.py - the NEW engine. Names the old function in
        docstrings only ("the thing it replaces"). NO call. Listing engine.py as a
        live call site is a hallucinated location (and the inverse of the C9
        discipline flag).
    TRAP-4. src/relay/dispatch.py line 86 again as the digest path: render_digest's
        ACTIVE code reads pre-rendered bodies (it.get("rendered", "")) and does NOT
        call the deprecated fn; only the commented-out line names it. A model that
        lists render_digest as a live call site has mis-read the active vs dead code.

  DISTRACTOR FILES (correctly contain NO true reference to the deprecated fn - a model
  that invents a reference in any of these has hallucinated a location):
    - src/channels/transport.py (SMTP / SMS gateway / APNs adapters; no template
      logic, no renderer reference).
    - src/relay/queue.py (in-memory queue data structure; no rendering).
    - src/relay/policy.py (retry/backoff math; no rendering).
    - src/reports/aggregate.py (grouping/counting helpers; no rendering).
    - src/templates/formats.py (locale normalisation utility; no renderer reference).
    - src/api/admin.py (uses the PREVIEW helper from TRAP-2, not the migration
      target).

  Scoring guidance:
    - Completeness (recall, weight 2.0) = of the 18 LIVE code-change entries (A1-A8,
      B1-B4, C1-C6), how many are present. Count DROPPED locations explicitly. Tier C
      alias/wrapper drops and Tier B buried-call drops are the strongest signal of
      forgetting-under-load; Tier A drops indicate a serious miss. Award credit (not
      penalty) for the C7/C8/C10 package-surface observations and the C9 disciplined
      exclusion of engine.py.
    - Correctness (hard-fail eligible) = are the listed locations actually true live
      references AND classified with the right kind (e.g. sms.py call flagged as
      aliased; push.py / audit.py flagged as indirect-via-wrapper). A checklist
      dominated by wrong/mis-kinded entries fails Correctness.
    - Hallucination (hard-fail eligible) = inventing a reference in a distractor file,
      or listing a location that does not exist. The four precision TRAPS and any
      distractor-file invention are the canonical hallucinations here.
    - Reasoning quality = did the model trace the indirect chains (alias -> call,
      wrapper SOURCE at B4 -> the two wrapper-caller chains at C3-C6) and correctly
      separate the live dispatch call (A7) from the dead commented one (TRAP-1/4),
      rather than only grepping the literal name. This is where Opus is hypothesised
      to separate from Sonnet at this scale.
    - Source transparency = every location cites file + line/section.
    - Discipline = did it correctly EXCLUDE the commented-out dead call, the preview
      helper, and the docstring-only engine.py rather than padding the list. A model
      that lists the traps to look thorough is penalised, not rewarded. The explicit
      C9 exclusion of engine.py is a discipline POSITIVE.
    - Format adherence = the output envelope plus a clean per-location structure
      (path, kind, migration action).
    Recall and precision are the scored discriminators. Summary quality is NOT the
    point. Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: recall = (live entries found) / 18;
    precision penalty = number of false positives (each trap or invented location
    listed). A model that finds 18/18 live entries with zero false positives, correctly
    flags the aliased and indirect-via-wrapper kinds, and explicitly excludes engine.py
    + the commented call + the preview helper is the exemplary 5 on Completeness,
    Correctness, and Discipline. Dropping Tier C indirect items or Tier B buried calls,
    or listing any trap, is where the score falls.
---

# Spec 25 - cross-reference-completeness-at-scale (the scaled forgetting-under-load probe)

The scaled analog of spec 22. Where spec 22 spread one deprecated function across 16
files, this spreads ONE deprecated function (`legacy_render_template`) across 20
interlinked Python modules in five packages (relay, channels, reports, templates, api),
with more indirection layers (an aliased import-and-call, a shared wrapper feeding two
separate via-wrapper caller chains, two package re-export surfaces) and more
distractors. The single concern is hidden across many files; the test is whether a
model finds EVERY live location without dropping the buried and indirect ones and
without inventing or mis-classifying any.

The corpus (`corpus/cross-reference-completeness-at-scale/`) is a synthetic
notification system "Northwind Relay" of 20 files. The deprecated
`legacy_render_template(payload, locale)` is referenced in 18 LIVE code-change entries
(plus a disciplined exclusion and a few credit-only package-surface observations)
spread across the tree: 8 obvious direct calls and imports (one buried deep in the long
dispatch file), 4 buried-in-long-file or wrapper-source references, and the indirect
ones - an aliased import and its aliased call site, and a shared wrapper that feeds two
separate via-wrapper caller chains (push channel and audit report). Four precision
traps are planted: a commented-out dead call, a confusingly similar preview function
(`legacy_render_template_preview`), the new engine's docstring-only mentions, and the
digest method whose active code reads pre-rendered bodies rather than calling the
deprecated fn.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central: a confidently-wrong checklist entry (a
false positive, or a real location given the wrong kind) is worse than a quietly missed
one, because an engineer acts on the checklist. Completeness (recall against the
18-entry live answer key) and Correctness / Hallucination (zero false positives, no
invented references) are the scored discriminators - summary quality is explicitly NOT
the point, since that is where Opus tied Sonnet on the earlier consolidation evals.
Reasoning quality captures whether the model traced the indirect chains and separated
the live dispatch call from the dead commented one, rather than grepping the literal
name. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/cross-reference-completeness-at-scale/`.
