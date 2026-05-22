---
task_category: heavy-translation
prompt_under_test: |
  You are given a long technical document in English at
  corpus/heavy-translation/source-en.md - the developer reference for a fictional
  message-streaming platform called "Northwind Stream". Translate the ENTIRE document
  into Spanish.

  Requirements:
    1. Translate every section, heading, paragraph, and bullet into Spanish. Do not
       summarise, omit, or add content. The translated document has the same 10 numbered
       sections in the same order as the source.
    2. Preserve terminology CONSISTENCY across the whole document. Many technical terms
       (stream, record, partition, offset, producer, consumer, broker, leader, follower,
       commit, rebalance, in-sync replica set, and many more) recur in many sections.
       Whatever Spanish rendering you choose for a term, use that SAME rendering on every
       occurrence throughout all 10 sections. Do not render the same term two different
       ways in different sections.
    3. Leave every code block, command-line example, configuration key, field name, and
       identifier EXACTLY as written in the source - do NOT translate them. This includes
       the four fenced code blocks, every backticked token (e.g. acks=all,
       cleanup.policy=compact, group_id, auto_offset_reset, enable_idempotence), all
       stream and field names (orders, order_id, amount_cents, trace_id), hostnames, and
       numbers. Translating a code keyword, a config key, or a field name breaks the
       document.
    4. The product name "Northwind Stream" is a proper name - keep it as "Northwind
       Stream". The common noun "stream" elsewhere is translated normally.
    5. Do not invert the meaning of any technical statement. In particular keep the three
       delivery guarantees (at-most-once / at-least-once / exactly-once) and the three
       compatibility policies (backward / forward / full) correct - a swapped meaning is
       a serious error.
    6. Output ONLY the translated document (Markdown, same structure). Do not add
       translator notes or commentary inside the document body.

  After the translated document, append the required output envelope (schemaVersion,
  tier, status, tool_budget_used) as separate lines OUTSIDE the document body. No em
  dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/heavy-translation/
corpus_intent: one long English technical reference (~10 sections, ~2000+ words, 4 fenced code blocks, dozens of recurring technical terms) to be translated to Spanish preserving terminology consistency, code-block integrity, and structure; plus a terminology answer key under .provenance documenting accepted renderings + occurrence counts + structural invariants
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY TRANSLATION (consistency-and-fidelity-at-length). The corpus is a long technical
  document on purpose: the same technical vocabulary recurs across all 10 sections, so
  the model must hold its own term choices in working memory and apply them identically
  end to end. This is the eval-22 completeness-under-load mechanism applied to
  translation: under the volume of a long document, weaker models DRIFT - they render
  "partition" as one word early and a different word later, or quietly summarise a late
  section, or translate a code keyword they would have left alone in a short doc. A
  strong model locks each term once and reuses it, leaves every identifier verbatim, and
  translates all 10 sections without drift.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a translation that INVERTS a
  meaning (renders "at-least-once" as "at-most-once", or "backward compatibility" as
  "forward compatibility") or that TRANSLATES A CODE IDENTIFIER (turning acks=all or a
  field name into Spanish, breaking the document) has produced confidently-wrong
  developer documentation that a reader would trust and act on. That is WORSE than an
  honestly-imperfect-but-faithful rendering. Reward faithful, internally-consistent
  translation with intact code. Penalise meaning inversions and broken identifiers
  hardest. Correctness and Hallucination are hard-fail eligible.

  TARGET LANGUAGE: Spanish. Spanish is chosen because it is a widely verifiable technical
  translation target with a settled technical vocabulary, and because Spanish prose runs
  15-25% longer than English - so a model that produces output much SHORTER than the
  source has almost certainly summarised rather than translated (a useful Completeness
  tell).

  ANSWER KEY (for the scoring Architect): the canonical terminology map, accepted
  renderings per term, occurrence counts, and the structural invariants are in
  corpus/heavy-translation/.provenance/terminology-key.md. Translation admits more than
  one defensible rendering per term, so the key lists ACCEPTED renderings and the
  CONSISTENCY requirement (whichever rendering the model picks, it must use it on every
  occurrence). The Architect reads that key file and scores against it. Summary of the
  load-bearing checks:

    - CONSISTENCY (the primary discriminator): sample ~12 high-frequency terms (stream,
      record, partition, offset, producer, consumer, broker, leader, follower, commit,
      rebalance, in-sync replica set). For each, scan ALL occurrences in the translation
      and confirm the SAME Spanish rendering is used every time. One term rendered two
      different ways across sections is a consistency miss. Drift increases with document
      length, which is exactly what this heavy eval stresses.
    - IDENTIFIER INTEGRITY (Correctness): the four fenced code blocks (two nwstream-admin
      commands, one Producer example, one Consumer example) and every backticked token,
      config key, field name, hostname, and number are byte-identical to the source.
      Translating any of them is a Correctness miss because it breaks the document.
    - MEANING FIDELITY (Correctness, hard-fail eligible): no inverted technical claim.
      The three delivery guarantees and three compatibility policies must keep their
      correct meanings; a swap (at-least <-> at-most, backward <-> forward) is the worst
      case and is confidently-wrong.
    - STRUCTURE / COMPLETENESS: all 10 numbered sections present in order, nothing
      summarised away, nothing added, no translator notes inside the body. Count any
      missing or summarised section explicitly. Output noticeably shorter than the source
      is a Completeness red flag (Spanish should be longer, not shorter).

  Scoring guidance:
    - Correctness (hard-fail eligible, weight 3.0) = identifier integrity (no translated
      code/keys/fields) AND meaning fidelity (no inverted guarantee or compatibility
      policy). A single broken identifier or a single meaning inversion is a Correctness
      miss; an inversion on a delivery guarantee is the hard-fail case.
    - Completeness (weight 2.0) = all 10 sections, all bullets, all paragraphs present
      and actually translated (not summarised). Count dropped or summarised sections.
    - Reasoning quality (weight 2.5) = evidence the model TRACKED its own term choices
      and applied them uniformly (consistency is a working-memory task), and correctly
      separated translatable prose from non-translatable code rather than handling each
      ad hoc.
    - Hallucination (hard-fail eligible, weight 2.5) = inventing a term, a section, or a
      code line not in the source; fabricating a config key.
    - Format adherence (weight 1.5) = same Markdown structure, 10 numbered headings in
      order, code blocks fenced and intact, output envelope appended OUTSIDE the document
      body.
    - Source transparency applies weakly (single source document). Voice match does NOT
      apply in the drafting sense, but terminology consistency is the analogous
      load-bearing axis here.

  Suggested shorthand for the Architect: consistency_score = (high-frequency terms
  rendered consistently) / 12; identifier_integrity = code blocks + inline identifiers
  left verbatim (any single broken identifier drops Correctness); meaning_fidelity = no
  inverted delivery-guarantee or compatibility-policy statement. An exemplary 5 on
  Correctness keeps every identifier byte-identical, inverts no meaning, and locks every
  high-frequency term to a single rendering across all 10 sections. The score falls on
  any translated identifier, any inverted meaning, any term-rendering drift, or any
  summarised section.

  Run the full 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3; effort inert per
  the methodology). Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding - term-rendering
  drift on a long translation is exactly where per-run variance and forgetting-under-load
  show up.
---

# Spec 35 - heavy-translation (consistency and fidelity at length)

A heavy translation eval. The corpus is one long English technical document
(`corpus/heavy-translation/source-en.md`) - the developer reference for a fictional
message-streaming platform, "Northwind Stream", running to ten numbered sections, four
fenced code blocks, and dozens of recurring technical terms. The model must translate
the ENTIRE document into Spanish while (a) rendering each recurring technical term the
SAME way on every one of its occurrences across all ten sections, (b) leaving every code
block, command, configuration key, field name, and identifier byte-identical, and (c)
preserving the meaning of every technical claim - especially the three delivery
guarantees and the three compatibility policies, where a swapped meaning is a serious
error.

Translation is the eval-22 completeness-under-load mechanism in a new guise: the same
vocabulary recurs throughout a long document, so the model has to hold its own term
choices in working memory and apply them uniformly end to end. Under length, weaker
models drift - one rendering early, a different one later - or quietly summarise a late
section, or translate a code keyword they would have left alone in a short document. A
model that "improves" the doc by translating `acks=all` or a field name, or that inverts
"at-least-once" into "at-most-once", produces confidently-wrong developer documentation a
reader would act on, which is worse than an honestly imperfect but faithful rendering.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The answer
key is the canonical terminology map at
`corpus/heavy-translation/.provenance/terminology-key.md`, which lists accepted Spanish
renderings per term, occurrence counts, and the structural invariants (the four code
blocks, the inline identifiers, the ten-section structure). Because translation admits
more than one defensible rendering, the key scores CONSISTENCY (same rendering every
time) and FIDELITY (defensible rendering plus intact identifiers plus no inverted
meaning) rather than a single gold string. Correctness and Hallucination are hard-fail
eligible; Reasoning quality (term-tracking under length) and Completeness (all ten
sections actually translated, not summarised) are the load-bearing differentiators. Voice
match does not apply in the drafting sense; terminology consistency is its analogue here.
The variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is
the directory `corpus/heavy-translation/`.
