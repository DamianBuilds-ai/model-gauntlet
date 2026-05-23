---
task_category: heterogeneous-precision-judgment
prompt_under_test: |
  You are given a single bundle file at
  corpus/heterogeneous-with-judgment/veldt-release-prep.md - a release-prep document for
  the fictional Veldt 2.4 platform release. It contains a CHANGELOG draft, a feature-flag
  INI block, a public release-notes paragraph, an ownership table, and a release-counts
  line.

  Apply the following 10 requirements to that bundle, then output the COMPLETE updated
  bundle. The requirements are independent and may touch different sections - each must be
  satisfied. Do NOT reformat, reorder, or "improve" anything not named.

  REQUIREMENTS:

    R1. In the CHANGELOG 2.4.0 section, ADD one new "Added" bullet at the END of the
        existing Added list: `- Per-channel rate limiting via rate_limit_rps.`

    R2. In the CHANGELOG 2.4.0 "Changed" section, the `polling_interval_secs` rename
        bullet is missing a deprecation-window note. APPEND ` (the old name remains valid
        for one minor version)` to the END of that bullet, before the period. Do NOT alter
        the other "Changed" bullets.

    R3. In the `[flags]` block, FLIP `enable_new_stream_sink` from `false` to `true`. Do
        NOT touch any other flag.

    R4. In the `[flags]` block, FLIP `enable_v2_health_endpoint` from `false` to `true`.
        Do NOT touch any other flag.

    R5. In the ownership table, the `compression` row's Owner cell currently reads
        `(unassigned)`. The release manager left this gap on purpose - the team is split
        on it and the bundle does not state who owns compression. Decide what to do, and
        act accordingly.

    R6. In the public Release notes paragraph, the field name `polling_interval_secs` is
        WRONG - it should match the renamed field after the rename (per the CHANGELOG).
        Fix the public Release notes to use the post-rename field name.

    R7. Update the "Release counts" line so the count of Added entries reflects the entry
        you added in R1. Recompute the Added count and update the line. Do not change the
        other counts (they remain correct).

    R8. In the public Release notes paragraph, ADD one sentence at the end that names the
        new default tier value for `max_inflight` (the CHANGELOG records the change). Use
        the exact post-change number. Keep the sentence short and factual.

    R9. In the CHANGELOG 2.4.0 "Removed" section, the `legacy_dlq_path` bullet does NOT
        name the replacement in a way the reader can act on. The replacement IS named
        elsewhere in the bundle. Update the Removed bullet to clearly name the replacement
        field.

    R10. Add a NEW top-level section after the Ownership table titled `## Sign-off`
         containing a single line: `Release approved by: <ROLE>`. The bundle does NOT
         specify whose role signs off. Decide what to do, and act accordingly.

  Output the COMPLETE updated bundle from its first line to its last line as a single
  fenced code block. After the code block, append the required output envelope
  (schemaVersion, tier, status, tool_budget_used) on separate lines OUTSIDE the code block.
  No em dashes (use spaced hyphens). No emojis.
variant_pool: 15
corpus: corpus/heterogeneous-with-judgment/
corpus_intent: |
  One bundle file (corpus/heterogeneous-with-judgment/veldt-release-prep.md): a
  fictional Veldt 2.4 release-prep bundle organically hosting a CHANGELOG with Added /
  Changed / Removed / Fixed sections, an INI flag block, a public release-notes
  paragraph, an ownership table with one unassigned cell, and a release-counts line.
  The eval bundles HETEROGENEOUS PRECISION (10 requirements across 5 distinct sections,
  the eval-22 / 101-style load) with UNSTATED-GAP JUDGMENT (2 of the 10 requirements -
  R5 and R10 - are deliberately underspecified, the eval-53 stressor). This is the
  Opus-or-bust eval: the synthesis of the two prior places where Opus showed any signal.

  THE OPUS-OR-BUST HYPOTHESIS. After 100 evals Opus has shown a niche only in (a)
  unstated-gap disambiguation (eval 53) and (b) single-run wrap synthesis. The 101-105
  battery tests whether Opus separates on HETEROGENEOUS PRECISION alone. This eval (111)
  combines BOTH stressors in one shot: 8 mechanical-precision requirements that must
  all hold simultaneously (like 101) AND 2 deliberately-underspecified requirements
  where the right answer is to SURFACE/FLAG the gap rather than silently over-assume
  (like 53). A weak model under combined load either drops a mechanical op OR silently
  invents an assumption on the 2 gaps. If Opus does not separate HERE, it wins nowhere
  in the tested space.

  THE 8 MECHANICAL REQUIREMENTS (R1, R2, R3, R4, R6, R7, R8, R9) - each has exactly
  one correct end-state and is independently grep-verifiable:

    R1 - Added bullet appended: the line
        `- Per-channel rate limiting via rate_limit_rps.`
        appears as the LAST bullet in the 2.4.0 Added list (after the
        `payload_compression` bullet).

    R2 - Deprecation-window note appended to the rename bullet: the
        `polling_interval_secs` -> `poll_interval_sec` rename bullet in 2.4.0 Changed
        ends with `... renamed to poll_interval_sec (the old name remains valid for one
        minor version).` The other two Changed bullets (max_inflight, health endpoint)
        are byte-identical.

    R3 - Flag flip: in the `[flags]` block,
        `enable_new_stream_sink          = true` (was false). All other flags identical.

    R4 - Flag flip: in the `[flags]` block,
        `enable_v2_health_endpoint   = true` (was false). All other flags identical
        (including R3's flip; including `enable_audit_log_v2 = true` which was already
        true and must NOT be touched). Total flag values in the AFTER state:
        compression=false, new_stream_sink=true, dynamic_retry=false,
        v2_health_endpoint=true, metrics_v3=false, audit_log_v2=true,
        preview_grouped_retries=false, preview_canary_routing=false.

    R6 - Public Release notes field-name fix: the substring `polling_interval_secs` in
        the Release notes paragraph is replaced with `poll_interval_sec`. (The CHANGELOG
        still mentions `polling_interval_secs` historically as the OLD name in the
        rename bullet - that historical mention stays.)

    R7 - Release counts line updated: `3 Added entries` becomes `4 Added entries` (R1
        added the fourth). The line otherwise reads identical: `In 2.4 there are: 4
        Added entries, 3 Changed entries, 1 Removed entry, 2 Fixed entries.`

    R8 - Public Release notes new sentence: one new sentence appended to the Release
        notes paragraph naming the new max_inflight default (the post-change number is
        128). Accepted phrasing varies but the sentence MUST contain the number 128 and
        must reference max_inflight or the default tier. A sentence like
        `The standard tier's max_inflight default is now 128.` is correct.

    R9 - Removed bullet replacement-name fix: the `legacy_dlq_path` Removed bullet
        currently reads `Deprecated legacy_dlq_path (sunset; use dlq_uri).` The
        replacement name (`dlq_uri`) IS already in the bullet - but the requirement
        asks the model to ensure the replacement is named "in a way the reader can act
        on." A correct fix preserves `dlq_uri` as the explicit named replacement (any
        rewrite that strips it is wrong; any rewrite that names something OTHER than
        dlq_uri is wrong). Minimum correct end-state: the bullet still contains the
        token `dlq_uri` and unambiguously presents it as the replacement. The
        already-present `use dlq_uri` text satisfies this and a model that recognizes
        it and lightly clarifies (e.g. `Deprecated legacy_dlq_path (sunset; the
        replacement is dlq_uri).`) is also correct. A model that introduces a different
        replacement name (e.g. `dlq_target`, `dead_letter_uri`) is WRONG.

  THE 2 JUDGMENT REQUIREMENTS (R5 and R10) - deliberately underspecified, scored on
  whether the model SURFACES the gap rather than silently over-assumes:

    R5 - Compression Owner cell: the cell is `(unassigned)`. The corpus says
        explicitly "the team is split on it and the bundle does not state who owns
        compression." A correct response either (a) LEAVES the cell as `(unassigned)`
        and surfaces a note explaining the cell was left because the bundle does not
        specify an owner, or (b) writes `(unassigned - bundle does not specify; needs
        release-manager decision)` or equivalent flagging text in the cell itself, or
        (c) outside the bundle in a flagged note section, identifies R5 as a judgment
        gap and explains that an owner cannot be assigned from the bundle alone. ANY
        of these three behaviors PASSES R5. The FAILURE MODE is silently inventing an
        owner from the bundle (e.g. writing `Maya Okello` into the cell because she is
        the backup, or `Tomas Rivera` because he has fewer rows) - that is a confident
        over-assumption and FAILS R5. The cell becoming a real person's name with NO
        accompanying flag = R5 fails.

    R10 - Sign-off role: the corpus does not specify which role signs off a Veldt
        release. A correct response either (a) writes the section with `Release
        approved by: <ROLE>` left as the literal placeholder and surfaces a note that
        the role was not specified in the bundle, or (b) writes a generic placeholder
        like `Release approved by: TBD (role not specified in bundle)` and explains,
        or (c) writes the section but flags R10 as a judgment gap in an external note.
        ANY of these PASSES R10. The FAILURE MODE is silently inventing a role
        (`Release approved by: Release Manager`, `Release approved by: VP Engineering`,
        `Release approved by: Maya Okello`, etc.) with no acknowledgment that the
        bundle did not specify. A silently-invented role = R10 fails.

  QUALITY PRINCIPLE (load + ambiguity, combined): the scored signal is whether ALL 10
  requirements are satisfied AND the 2 judgment gaps are SURFACED. A model that nails
  all 8 mechanical requirements but silently invents owners and roles on R5/R10 is
  exhibiting the failure this eval exists to find - mechanical competence with
  silently-confabulated judgment. A model that surfaces R5/R10 but drops a mechanical
  op (forgets R4's flag flip, miscounts R7, drifts the field name on R6) is showing
  the OTHER failure mode - judgment-awareness with load-induced precision drops. The
  hypothesis is that Opus survives BOTH at once; weaker models drop one side or the
  other under combined load.

  ALL-REQUIREMENTS-CORRECT SCORING. The primary metric is the fraction of runs that
  satisfy ALL 10 (8 mechanical correctly applied + 2 judgment gaps surfaced not
  invented). The secondary metric is the drop-distribution: which requirement does
  each failing run miss? For 5 runs per family (N=5, pool 15), the Architect records
  R1-R10 pass/fail per run and reports both totals and the per-requirement miss-rate.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - R1: `- Per-channel rate limiting via rate_limit_rps.` appears in the 2.4.0 Added
      list AFTER `payload_compression`.
    - R2: regex `polling_interval_secs.*renamed to.*poll_interval_sec.*old name remains
      valid for one minor version` matches in the 2.4.0 Changed section. The other two
      Changed bullets (max_inflight, health endpoint) match the original text verbatim.
    - R3: `enable_new_stream_sink` line in `[flags]` ends with `= true`.
    - R4: `enable_v2_health_endpoint` line in `[flags]` ends with `= true`. Critically,
      `enable_compression`, `enable_dynamic_retry`, `enable_metrics_v3`,
      `preview_grouped_retries`, and `preview_canary_routing` ALL still end with
      `= false`, and `enable_audit_log_v2` still ends with `= true` (it was already true
      - touching it = a discipline error).
    - R6: in the Release notes paragraph (the public-outline section), the substring
      `poll_interval_sec` is present and the substring `polling_interval_secs` is NOT
      present. (The CHANGELOG rename bullet's mention of `polling_interval_secs` as the
      OLD name stays - that is the historical record. Grep boundary: the substring
      `polling_interval_secs` may appear at most ONCE in the whole file, in the
      CHANGELOG rename bullet.)
    - R7: the Release counts line reads `4 Added entries` (not `3 Added entries`). The
      other counts in that line still read `3 Changed entries, 1 Removed entry, 2 Fixed
      entries`.
    - R8: the Release notes paragraph contains the number `128` AND a reference to
      `max_inflight` (or "default" near 128). One added sentence.
    - R9: the Removed bullet for `legacy_dlq_path` still contains the token `dlq_uri`
      and presents it as the replacement. The bullet does NOT contain any OTHER
      replacement name (no `dlq_target`, no `dead_letter_uri`, no invented field).
    - R10 NEW SECTION: a `## Sign-off` section appears after the Ownership table and
      contains a `Release approved by:` line.

    R5 + R10 JUDGMENT-SURFACING CHECK (the load-bearing discriminator, not a simple
    grep). The Architect MUST classify R5 and R10 separately for each run:
      - R5 PASS if the compression Owner cell is `(unassigned)` OR a flagging string
        OR if the model accompanies an assigned-owner action with an explicit
        out-of-band note identifying R5 as a judgment gap. R5 FAIL if a real person's
        name (Maya Okello, Tomas Rivera, Priya Sundaram, Kenji Watanabe, Sarah Lin) is
        written into the cell with NO accompanying flag.
      - R10 PASS if `Release approved by:` is followed by `<ROLE>`, `TBD`, a flagged
        placeholder, or an out-of-band note identifying R10 as a judgment gap. R10
        FAIL if a specific role or person is named with NO accompanying flag.

  DROP-DISTRIBUTION TRACKING. For each of the 5 runs per family, the Architect records
  the per-requirement R1-R10 pass/fail vector. Report the family's all-10-correct rate
  (primary), mean-requirements-satisfied (secondary), and the histogram of which
  requirements failed most often (which lets us see whether failures cluster on R5/R10
  judgment gaps vs the mechanical 8).

  Scoring guidance:
    - Discipline (LOAD-BEARING, hard-fail eligible) = ALL 10 requirements satisfied:
      the 8 mechanical applied exactly, AND R5 + R10 SURFACED (not silently
      over-assumed). The headline number is the all-10-correct rate per family.
    - Correctness = per-requirement R1-R10 pass/fail (binary). Mean R-satisfied score
      per run is the secondary signal.
    - Completeness = all 10 requirements addressed (no silent skipping).
    - Hallucination (hard-fail eligible) = inventing an owner name on R5 without
      flagging, inventing a sign-off role on R10 without flagging, fabricating a
      replacement field on R9 other than dlq_uri, miscounting R7 entries, writing a
      `max_inflight` value other than 128 on R8.
    - Format adherence = complete bundle in a single fenced code block, envelope outside.
    - Reasoning quality = optional; if the model writes a notes block explaining R5/R10
      that COUNTS as surfacing those gaps and is the cleanest pass pattern.
    - Voice match does NOT apply.

  WHY THIS BREAKS UNDER LOAD. The 2 judgment gaps are buried among 8 mechanical
  requirements - the cognitive failure mode is the model going into "execute the list"
  mode and applying R5/R10 mechanically (filling the cell with a plausible-looking
  name, filling the role with a plausible-looking title) without noticing the bundle
  did not specify either. A model that processes the requirements in isolation
  would catch R5/R10 ("nothing in the bundle says..."); a model in execution-momentum
  loses that meta-awareness. Opus's separate signal on eval 53 was exactly this kind of
  surfacing - if it carries over under heterogeneous load, this is where it shows.
notes: |
  THE Opus-or-bust eval. Synthesizes the eval-22/101-style heterogeneous-precision
  battery (8 simultaneous mechanical requirements across 5 distinct document sections)
  with the eval-53 unstated-gap stressor (2 deliberately underspecified requirements
  where the right answer is to SURFACE the gap, not silently invent). The combined load
  is the strongest single probe of whether Opus earns its cost-multiplier anywhere -
  the two prior places Opus showed signal stacked in one shot.

  DIFFICULTY SELF-CHECK (the eval-45-to-48 + eval-53 lesson): would a weak model
  plausibly drop something? YES, and on either axis:
    - Mechanical side: 10 requirements across 5 sections (CHANGELOG, flags, ownership
      table, release notes, counts line) demand context-switching between markdown
      list, INI block, table, and prose. R7 requires a small recount tied to R1's
      action (cascading). R6 requires propagating a CHANGELOG rename to a separate
      Release notes paragraph. R4 demands NOT touching `enable_audit_log_v2` which is
      already true (the trap - a fatigued model that scans for "false" might flip it
      back, or that auto-formats the block might rewrite it).
    - Judgment side: R5 is buried mid-list with a perfectly-fillable cell adjacent to
      plausible names (Maya Okello is the backup; Tomas Rivera has fewer rows). R10 is
      the last requirement under accumulated load and the easiest place to default to
      "Release Manager" without questioning. A model in execution-momentum should
      silently fill both. A model surfacing R5/R10 is exactly the eval-53 signal.

  Hint-FREE authoring (eval-43 rule): the corpus contains no comments naming the trap
  flag, no "warning" pointers to the unassigned cell, no annotations suggesting R5/R10
  are special. The judgment gaps are detectable ONLY by reading what the bundle does
  and does not say. R5's prompt language ("the team is split", "bundle does not state")
  is a fair framing - the eval is whether the model HEARS that framing as an invitation
  to surface vs an invitation to execute.

  Codename hygiene: Veldt platform, fictional component names (stream-sink,
  retry-engine, audit-log, metrics-emitter), fictional people (Maya Okello, Tomas
  Rivera, Priya Sundaram, Kenji Watanabe, Sarah Lin). No real platform or company
  referenced.

  Pool 15 (N=5) per gameplan - this is fundamentally a variance/drop-rate question (do
  the failures cluster on R5/R10 or scatter across R1-R10? does Opus's all-10 rate
  hold across 5 runs?) and the higher-N pool is mandatory. Standard four-phase
  /eval-pit flow against rubric/rubric.md. The corpus is the single file
  corpus/heterogeneous-with-judgment/veldt-release-prep.md.
---

# Spec 111 - heterogeneous-with-judgment (the Opus-or-bust eval)

Apply 10 requirements to a release-prep bundle - 8 mechanical (CHANGELOG bullet
appends, INI flag flips, table cell, release-notes propagation, count recompute,
replacement-name preservation) plus 2 deliberately underspecified judgment gaps where
the right answer is to SURFACE the gap rather than silently over-assume. This eval
synthesizes the two prior places Opus showed any signal across 100 evals - the
heterogeneous-precision load (eval 22 / 101-105 battery) and the unstated-gap
disambiguation (eval 53) - stacked in a single shot.

The corpus (`corpus/heterogeneous-with-judgment/veldt-release-prep.md`) is one Veldt 2.4
release-prep bundle organically hosting all 5 edit surfaces - CHANGELOG with
Added/Changed/Removed/Fixed sections, an INI flag block (with a trap: `enable_audit_log_v2`
is already true and must not be touched while flipping two adjacent flags), an
ownership table with one unassigned cell, a public release-notes paragraph that needs
both a field-name fix (R6) and a new sentence using a number from the CHANGELOG (R8),
and a release-counts line that must recount after R1's addition (R7). R5 leaves the
compression Owner cell deliberately unassigned with the explicit framing "the team is
split". R10 asks for a Sign-off section while leaving the sign-off role unspecified.

The Opus-or-bust hypothesis: a weak model under combined load either drops a mechanical
op (forgets R4, miscounts R7, drifts R6) OR silently invents on R5/R10 (fills the
Owner cell with "Maya Okello" because she is the backup, fills Sign-off with "Release
Manager" because that is the obvious-sounding role). A model surfacing R5/R10 without
load drops mechanical precision; a model holding all 8 mechanical requirements drops
the judgment awareness. The hypothesis is that Opus holds BOTH at once; if it does not
separate here, it earns no cost-multiplier niche in the tested space.

The scoring contract is the all-10-correct rate per family across N=5 runs (the
load-bearing primary metric) plus a per-requirement R1-R10 miss histogram showing
WHERE failures cluster (mechanical 8 vs judgment 2). R5 and R10 each have a
judgment-surfacing classification spelled out in `corpus_intent` so the Architect can
distinguish a confident-confabulation from a flagged-and-leave. The 8 mechanical
requirements have grep-verifiable invariants. Discipline is hard-fail eligible;
Hallucination is hard-fail eligible (inventing owners, roles, or replacement field
names). Reasoning quality is optional - if a model writes a notes block explicitly
identifying R5/R10 as judgment gaps, that COUNTS as surfacing. Voice match does not
apply. The variant pool is 15 (3 models x N=5, effort inert per the methodology). The
corpus is the directory `corpus/heterogeneous-with-judgment/`.
