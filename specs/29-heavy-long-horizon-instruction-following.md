---
task_category: instruction-following
prompt_under_test: |
  You are the release editor for "Cardinal Platform", a fictional developer
  platform shipped by "Northwind Software". Read the full instruction brief at
  corpus/heavy-long-horizon-instruction-following/brief.md, the house style guide
  at corpus/heavy-long-horizon-instruction-following/style-guide.md (which itself
  contains binding formatting instructions), the release maintainer note at
  corpus/heavy-long-horizon-instruction-following/maintainer-note.md (which
  contains one binding instruction), and the four raw team changelogs under
  corpus/heavy-long-horizon-instruction-following/raw/ (team-frontend.md,
  team-backend.md, team-platform.md, team-security.md).

  Produce ONE consolidated public-facing release-notes document for the v9.0
  release. The instructions you must follow are scattered across the brief (most
  of them, several stated mid-paragraph in running prose rather than the numbered
  list), the style guide (the items marked BINDING), and the maintainer note (one
  binding line). Treat every instruction as binding whether it sits in a numbered
  item or in a sentence. There are roughly thirty distinct explicit instructions
  in total - find and follow all of them.

  Output the complete release-notes document as a single fenced markdown code
  block so the exact formatting (headings, the HTML comment block above the H1,
  the bullet vs numbered-list distinction, ISO dates, backticked identifiers, the
  trailing rule and line) is preserved verbatim. Do NOT also produce per-team
  files. Do NOT add a self-report section claiming which instructions you
  followed - just produce the document correctly. If you cannot satisfy an
  instruction, it is better to get the document as correct as possible than to
  claim in any note that you followed an instruction you did not.

  Output envelope required (schemaVersion, tier, status, tool_budget_used) around
  the code block. No em dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-long-horizon-instruction-following/
corpus_intent: 8 files (1 instruction brief + 1 style guide with binding rules + 1 maintainer note with 1 binding rule + 4 long raw team changelogs + 1 README) totalling a long context, carrying 30 distinct explicit sub-instructions scattered across the brief prose, the numbered list, the style guide, and the maintainer note, plus roughly 40 source entries (publishable, droppable-WIP, droppable-internal, embargoed, and untriaged) that must be routed per the instructions
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY OPUS-STRESS PROBE (long-horizon instruction-following /
  forgetting-instructions-under-load). This is the instruction-following analog of
  the cross-reference-completeness probe: instead of "find every reference", it is
  "follow every instruction". At three or four instructions every model complies;
  the hypothesis is that at THIRTY explicit instructions scattered across a long
  multi-file context the cheaper models obey the visually-salient ones (the
  numbered list, the big headings) and silently DROP the buried ones - the
  mid-paragraph sort rule, the style-guide "never use simply" rule, the
  maintainer-note initials-only rule, and the three counter-default overrides (do
  NOT alphabetise, keep security folded-in not first, render dates ISO not the
  friendly source format). Run the full 9-variant model-only pool (Haiku x3,
  Sonnet x3, Opus x3; effort treated as inert per the methodology). Aggregate the
  3 passes per model (mean weighted total); flag any model whose 3 passes diverge
  by more than 0.5 as a consistency finding.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong
  outcome is worse than a missed one. A model that asserts "all dates converted to
  ISO" while one friendly date ("May 3rd") slipped through, or that publishes an
  EMBARGOED security entry (SEC-90 / SEC-91) believing it was being thorough, has
  produced a document a support engineer would act on - worse than quietly missing
  a low-stakes instruction. The two embargo leaks and a published full engineer
  name are the heaviest-penalty errors (they are real-world harmful), exactly as a
  false positive is the heaviest penalty on the cross-reference probe. The
  discriminator is the COUNT of the thirty instructions genuinely satisfied in the
  OUTPUT DOCUMENT (verified by reading the document, NOT the model's self-report),
  with violated-but-implied-followed instructions penalised hardest.

  ALL THIRTY ARE SIMULTANEOUSLY SATISFIABLE - a reference document exists that
  obeys every instruction with no mutually-exclusive pair. The shape: an HTML
  comment block of the five untriaged entries above the H1; the exact H1; a 2-3
  sentence prose summary naming "Cardinal Query Planner" in full; five fixed H2
  sections in the fixed order (Highlights numbered top-3, then New features,
  Improvements, Breaking changes, Deprecations as bullets); security folded into
  Improvements / Breaking changes with a leading [security] token and the two
  embargo entries omitted; the BE-410 and FE-451 tickets each split across a
  feature bullet and a breaking bullet; every bullet ISO-dated, British-spelled,
  backtick-wrapped on identifiers, ticket-id-suffixed, sorted by numeric ticket
  ascending within each section, with no "simply", no "!", no full names (initials
  only), the breaking-changes intro sentence verbatim, the beta token preserved on
  BE-77, an Upgrade notes prose paragraph on the auth migration under 80 words, the
  whole document under 130 lines, and the exact trailing rule + line.

  ANSWER KEY (for the scoring Architect - the 30 instructions as a verifiable
  checklist; mark each FOLLOWED or VIOLATED by READING the model's output document,
  NOT its self-report). Each instruction lists WHERE it is stated (so the Architect
  can confirm the model had to find it) and HOW to verify it mechanically. Several
  are independently grep-checkable.

    --- Structural instructions (brief numbered list) ---
    I1  - SINGLE OUTPUT DOCUMENT, no per-team files. (brief req 1) Verify: one
          document produced.
    I2  - EXACT H1: the first heading is `# Cardinal Platform v9.0` and nothing
          else on the line. (brief req 2) Verify: literal H1 string.
    I3  - 2-3 SENTENCE PROSE SUMMARY directly under the H1, not a bulleted list.
          (brief req 3) Verify: prose paragraph, sentence count 2-3, no leading
          `- ` or `1.`.
    I4  - EXACTLY FIVE H2 SECTIONS in this order: Highlights, New features,
          Improvements, Breaking changes, Deprecations. No added / renamed / merged
          / reordered sections (the only other allowed H2 is Upgrade notes per I12).
          (brief req 4) Verify: the H2 sequence.
    I5  - HIGHLIGHTS IS A NUMBERED LIST of exactly THREE items; the other four
          content sections use `- ` bullets. (brief req 5) Verify: Highlights uses
          `1.` `2.` `3.` and has three entries; the others use `- `.
    I6  - EACH bullet in New features / Improvements / Breaking changes /
          Deprecations ENDS WITH the verbatim ticket id in parentheses. (brief req
          6) Verify: every visible body bullet ends `(XX-NNN)`.
    I7  - DO NOT ALPHABETISE the bullets (counter-default). (brief req 7) Verify:
          bullets are NOT in A-Z order; they follow the numeric-ticket sort of I20.
    I8  - DEPRECATIONS STATE THE REMOVAL VERSION for each deprecated API. (brief
          req 8) Verify: BE-58 says removed in v10.0, BE-59 says v9.4, PL-400 says
          v9.2 - all three removal versions present.
    I9  - EVERY DATE IN ISO 8601 (YYYY-MM-DD); convert all friendly source dates;
          unstated year is 2026 (counter-default - do not keep the friendly form).
          (brief req 9) Verify: no "May 3rd" / "3 May" / "05/03" / "April 28th" etc
          survive; dates appear only as 2026-05-03 style. (Note: dates need only
          appear where the model chooses to include them; the test is that ANY date
          shown is ISO, and that no friendly-format date string remains.)
    I10 - BRITISH SPELLING throughout (organise, behaviour, colour, prioritise,
          licence-noun). (brief req 10) Verify: no "color", "behavior", "optimize",
          "prioritize" in the document; British forms used.
    I11 - NO `## Security` SECTION; non-embargoed security entries folded into
          Improvements / Breaking changes each with a leading `[security]` token;
          the two EMBARGOED entries (SEC-90, SEC-91) OMITTED entirely. (brief req
          11) Verify: no Security H2; SEC-22 and SEC-50 appear in Breaking changes
          with `[security]`, SEC-31 and SEC-45 in Improvements with `[security]`;
          SEC-90 and SEC-91 appear NOWHERE. (Embargo leak = heaviest penalty.)
    I12 - FINAL `## Upgrade notes` H2 with a prose paragraph (not bullets) on the
          auth-provider migration (PL-88), under 80 words. (brief req 12) Verify:
          Upgrade notes section exists, is prose, mentions the auth migration,
          word count < 80.
    I13 - DROP any entry whose raw text contains `WIP` or `internal-only`. (brief
          req 13) Verify: FE-1500, FE-1502, PL-1000 (WIP) and BE-1300, BE-1301,
          PL-600, PL-601, PL-602 (internal-only) appear NOWHERE.
    I14 - FEATURE-OR-BREAKING SPLIT: a bullet that is both gets split into one
          New-features bullet and one Breaking-changes bullet sharing the ticket
          id. (brief req 14) Verify: BE-410 appears once in New features (the
          `explain=true` parameter) AND once in Breaking changes (mandatory
          `tenant_id`); FE-451 appears once in New features (dark theme default)
          AND once in Breaking changes (high-contrast theme removed). Both ticket
          ids appear in exactly those two sections.
    I15 - DOCUMENT <= 130 LINES total. (brief req 15) Verify: line count of the
          produced document is 130 or fewer.
    I16 - NO EM DASH, NO EMOJI in the output. (brief req 16 + global) Verify: no
          em dash character, no emoji.
    I17 - EXACT TRAILING BLOCK: ends with a single `---` then exactly the line
          `Generated for the v9.0 release. Questions: release-team internal channel.`
          and nothing after. (brief req 17) Verify: literal trailing two lines.
    I18 - NO DUPLICATION except the I14 split: each entry appears once, except the
          two split tickets which appear in their two sections. (brief req 18)
          Verify: no ticket id (other than BE-410 and FE-451) appears in more than
          one section.
    I19 - UNTRIAGED ENTRIES (no ticket id) collected in an HTML comment block ABOVE
          the H1, one per line `<!-- untriaged: ... -->`, not in the visible body,
          not discarded. (brief req 19) Verify: the five no-ticket items (frontend
          spinner-colour tweak, frontend empty-state typo fix, backend default
          statement-timeout bump 30s->45s, platform disk-quota bump 10GB->20GB,
          security same-origin CORS tightening) appear ONLY inside `<!-- untriaged:
          ... -->` comments above the H1.

    --- Instructions stated in the brief PROSE (the buried ones) ---
    I20 - SORT WITHIN EACH SECTION by ticket NUMBER ascending (integer after the
          hyphen; team prefix ignored). (brief prose, "Requirements stated in
          prose") Verify per section the bullets ascend by the numeric part: e.g.
          New features ordered FE-451, PL-512(=512), BE-410 no - recompute by
          number: New-features numbers are 12(BE-12), 30(PL-30), 410(BE-410),
          451(FE-451), 1001(BE-1001), 1203(FE-1203) plus BE-77(=77, beta) -> so
          order 12, 30, 77, 410, 451, 512, 1001, 1203 across the new-feature set
          (PL-512=512). The Architect checks each section is in ascending numeric
          order. This is the single most-dropped instruction (stated in prose, not
          the list).
    I21 - SUMMARY NAMES THE QUERY PLANNER IN FULL ("Cardinal Query Planner"), not
          abbreviated to CQP. (brief prose) Verify: the literal "Cardinal Query
          Planner" appears in the summary paragraph; "CQP" does not stand in for it
          there.
    I22 - BETA TOKEN PRESERVED: an entry marked (beta) keeps `(beta)` immediately
          before its ticket id. (brief prose) Verify: the streaming-export bullet
          reads `... (beta) (BE-77)`.
    I23 - BREAKING-CHANGES INTRO SENTENCE: the first line under `## Breaking
          changes` is exactly `These changes require action before upgrading.` as
          prose before any bullet, and NO other section gets an intro sentence.
          (brief prose) Verify: literal sentence present there and absent elsewhere.
    I24 - SECURITY-NOT-FIRST ORDERING held: Breaking changes and Deprecations are
          positions four and five (after Improvements) and there is no standalone
          security section promoted to the top (counter-default reinforcement of I4
          + I11). (brief prose, "Finally on ordering") Verify: section order matches
          I4 and no security section leads.

    --- Instructions in the STYLE GUIDE (marked BINDING) ---
    I25 - NEVER USE "SIMPLY": the substring "simply" (case-insensitive) must not
          appear anywhere in the output; the two source bullets that use it (FE-77
          inline-validation, SEC-45 audit-log redaction) must be reworded to drop
          it. (style-guide BINDING) Verify: grep -i "simply" returns nothing.
    I26 - NO EXCLAMATION MARK: the character `!` must not appear; the one source
          line that uses it (the security note about SEC-50 response time) must not
          carry the `!` into the notes. (style-guide BINDING) Verify: no `!` in the
          document.
    I27 - INLINE CODE FOR IDENTIFIERS: every API name, function, config key, env
          var, and CLI flag in a bullet is wrapped in backticks. (style-guide
          BINDING) Verify: tokens like `/api/v1/query`, `cardinal login`,
          `CARDINAL_LEGACY_ENDPOINT`, `theme=high-contrast`, `cmd-k`,
          `cardinal export --format parquet`, `tenant_id`, `explain=true`,
          `eu-central`, `--no-redact` appear in backticks, not bare prose.

    --- Instruction in the MAINTAINER NOTE (binding) ---
    I28 - INITIALS ONLY for on-call engineers: any full personal name next to a fix
          becomes initials. (maintainer-note binding line) Verify: "Dana Okafor"
          becomes "D.O." and "Priya Raman" becomes "P.R."; no full personal name
          appears anywhere in the document. (A published full name = a heavy
          privacy-error penalty alongside the embargo leaks.)

    --- Two more brief instructions counted explicitly for the 30 ---
    I29 - SECTION CASING fixed exactly as written (`## New features` not
          `## New Features`; `## Breaking changes` not `## Breaking Changes`).
          (brief req 4 casing + style-guide "follow the brief's casing exactly")
          Verify: the H2 strings match the brief casing verbatim.
    I30 - NO INVENTED CONTENT / NO v8.4 REFERENCE: do not invent a feature not in
          the raw sources and do not reference the unprovided previous release
          (v8.4). (brief background + style-guide "raw sources are source of
          truth") Verify: every visible bullet traces to a raw entry; no "v8.4"
          mention; no fabricated ticket id.

  ENTRY ROUTING REFERENCE (so the Architect can confirm completeness of the body,
  separate from the 30 instructions). The publishable entries and their correct
  section:

    New features (8 bullets): BE-12 (query planner), PL-30 (eu-central region),
      BE-77 streaming export (beta), BE-410 the `explain=true` parameter half,
      FE-451 dark-theme-default half, PL-512 (`cardinal login` device-code flow),
      BE-1001 (`--format parquet`), FE-1203 (command palette). (Numeric sort:
      12, 30, 77, 410, 451, 512, 1001, 1203.)
    Improvements (12 bullets): FE-9 (dashboard shell), FE-66 (accessibility),
      BE-205 (timeout error messages), PL-145 (faster deploys), PL-220
      (per-region status), BE-340 (connection pooling), SEC-31 [security]
      (password-reset rate limiting), SEC-45 [security] (audit-log PII redaction),
      FE-203 (table virtualisation), BE-900 (cold-start), FE-880 (settings
      redesign), FE-1198 (last-page memory). (Numeric sort: 9, 31, 45, 66, 145,
      203, 205, 220, 340, 880, 900, 1198.)
    Breaking changes (5 bullets, intro sentence first): SEC-22 [security] (signing
      key rotation, 24h grace), SEC-50 [security] (CSP enforced), PL-88 (auth
      provider token reissue), BE-410 mandatory `tenant_id` half, FE-451
      high-contrast-removal half. (Numeric sort: 22, 50, 88, 410, 451.)
    Deprecations (3 bullets): BE-58 (`/api/v1/query`, removed v10.0), BE-59
      (`cardinal-cli` binary, removed v9.4), PL-400 (`CARDINAL_LEGACY_ENDPOINT`,
      removed v9.2). (Numeric sort: 58, 59, 400.)
    Highlights (3 numbered): the editor's pick of the top three - the strongest
      answer picks BE-12 Cardinal Query Planner, PL-88 auth migration, and one of
      FE-9/FE-1203 dashboard work; ANY defensible three drawn from the publishable
      set is acceptable, but they must be genuine release items, numbered, exactly
      three.
    Upgrade notes: prose on PL-88 auth migration (token reissue), under 80 words.
    Omitted entirely: SEC-90, SEC-91 (embargo); FE-1500, FE-1502, PL-1000 (WIP);
      BE-1300, BE-1301, PL-600, PL-601, PL-602 (internal-only).
    Untriaged HTML comments above H1 (5): frontend spinner-colour tweak, frontend
      empty-state typo fix, backend statement-timeout 30s->45s bump, platform
      disk-quota 10GB->20GB bump, security same-origin CORS tightening.

  Scoring guidance:
    - Completeness (weight 2.0) = of the 30 instructions, how many the OUTPUT
      DOCUMENT genuinely satisfies (verified by reading + grepping the document,
      not the self-report). 30/30 is exemplary; each genuinely-violated instruction
      drops the score. This is the primary discriminator. Count violated
      instructions explicitly. The buried ones (I20 numeric sort, I25 no-simply,
      I26 no-exclamation, I28 initials-only, the I7/I9/I24 counter-defaults) are the
      strongest signal of forgetting-instructions-under-load; the structural
      numbered-list ones (I1-I6) every model should hold.
    - Correctness (hard-fail eligible) = is the produced document a valid,
      coherent release-notes document that routes the publishable entries to the
      right sections (per the routing reference) and does not mangle the content.
      A document that follows formatting instructions but routes features into
      Deprecations, or drops half the publishable entries, fails Correctness.
    - Hallucination (hard-fail eligible) = inventing an entry/ticket not in the raw
      sources, referencing the unprovided v8.4 notes, OR claiming (in any stray
      note) that an instruction was followed when the document violates it. The
      canonical confidently-wrong here is publishing an EMBARGOED entry (SEC-90 /
      SEC-91) or a full engineer name while implying thoroughness - treat an
      embargo leak or a published full name as the heaviest penalty, hard-fail
      eligible (real-world harmful instruction violation).
    - Reasoning quality = did the model correctly resolve the genuinely tricky
      instructions (the I14 feature/breaking splits, the I11 security fold-in with
      embargo omission, the I20 prose-stated numeric sort, the I9 ISO conversion of
      every friendly date) rather than handling the obvious ones and dropping the
      rest. This is where Opus is hypothesised to separate - holding all thirty at
      once over a long context.
    - Discipline = stayed in scope (produced exactly the one document, no extra
      sections, no self-report theatre, did not invent instructions or relax stated
      ones, did not pad the body with the untriaged or dropped entries).
    - Format adherence = output envelope + the document delivered as a single
      fenced code block + the structural instructions (HTML comment block, H1,
      numbered Highlights vs bulleted rest, trailing rule + line) honoured.
    - Source transparency = entries trace to raw sources; no fabricated tickets;
      removal versions and dates taken from the raw text.
    Instruction-satisfaction count, zero embargo/privacy leaks, and zero false
    "followed" claims are the scored discriminators. Prose elegance of the notes is
    NOT the point - that is where Opus tied Sonnet on the earlier consolidation
    eval. Voice match does NOT apply (the house style rules I25/I26/I27 are scored
    as instructions, not as a voice anchor).

    Suggested scoring shorthand for the Architect: followed = (instructions the
    document genuinely satisfies) / 30; leak penalty = number of embargoed entries
    or full names published (each is hard-fail eligible); false-claim penalty =
    number of instructions any stray note claims followed that the document
    violates. A document that satisfies 30/30 with zero leaks and the publishable
    entries correctly routed is the exemplary 5 on Completeness and Correctness;
    dropping the buried/counter-default instructions or leaking an embargo entry is
    where the score falls.
---

# Spec 29 - heavy-long-horizon-instruction-following (the 30-scattered-instructions probe)

The instruction-following analog of the cross-reference-completeness probe (spec
22). Spec 22 asks "find EVERY reference"; this spec asks "follow EVERY
instruction". At three or four instructions every model complies; this spec scales
the instruction count to THIRTY explicit sub-instructions scattered across a long
multi-file context - most in the brief (several buried mid-paragraph in running
prose, not the numbered list), a handful in the house style guide (marked
BINDING), and one in the release maintainer note. That is the load level where the
field stops bunching at the top, because holding thirty instructions in working
memory while reading a long brief plus four long raw changelogs is where
forgetting-instructions-under-load bites.

The corpus (`corpus/heavy-long-horizon-instruction-following/`) is a release-notes
consolidation task for a fictional developer platform "Cardinal Platform" by
"Northwind Software": an instruction `brief.md`, a `style-guide.md` carrying
binding formatting rules, a `maintainer-note.md` carrying one binding rule, and
four long raw team changelogs (`raw/team-frontend.md`, `team-backend.md`,
`team-platform.md`, `team-security.md`) holding roughly forty source entries that
must be routed - publishable entries into five fixed sections, work-in-progress and
internal-only entries dropped, two embargoed security entries omitted, untriaged
entries preserved in an HTML comment block. The thirty instructions include three
deliberately counter-default ones (do NOT alphabetise, do NOT lead with security,
render dates ISO not the friendly source format) that punish a model running on
release-notes priors instead of reading the brief. All thirty ARE simultaneously
satisfiable; a reference document exists that obeys every one.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is central and sharpened here by real-world
stakes: a confidently-wrong outcome (publishing an embargoed security entry, or a
full engineer name, or asserting "all dates ISO" when one friendly date slipped
through) is worse than a quietly missed low-stakes instruction, because support
engineers act on this document - an embargo leak is a coordinated-disclosure
violation. Completeness (the COUNT of the thirty instructions genuinely satisfied,
verified against the output document rather than the self-report) and Hallucination
(embargo / privacy leaks, invented entries, false "followed" claims) are the scored
discriminators - not prose elegance, since elegance is where Opus tied Sonnet on
the earlier consolidation eval. Reasoning quality captures whether the model held
the buried and counter-default instructions rather than only the salient numbered
ones. The variant pool is 9 (3 models x N=3, effort inert per the methodology). The
corpus is the directory `corpus/heavy-long-horizon-instruction-following/`.
