---
task_category: leaf-extraction
prompt_under_test: |
  You are given one bloated trunk reference doc, corpus/leaf-extraction/HOLLOWMERE.md,
  for a fictional domain "Hollowmere". The trunk has grown too large. Your job is to
  extract ONE coherent, self-contained section into a new leaf doc and wire the trunk
  to point at it.

  Do this in two parts:

  PART 1 - Identify and extract the leaf.
    - Choose the SINGLE most self-contained, coherent section that can stand alone as
      its own leaf doc (a section that does not depend on, and is not depended on by,
      the surrounding pipeline material).
    - Produce the new leaf file content. Name it `HOLLOWMERE-RENDER-CACHE.md` IF (and
      only if) the render-cache material is what you extract. Give the leaf a top-level
      `# HOLLOWMERE-RENDER-CACHE.md - ...` heading and include the FULL content of the
      extracted section verbatim (all of its sub-sections), nothing from other sections.

  PART 2 - Update the trunk.
    - Show the updated HOLLOWMERE.md with the extracted section REMOVED from its body
      AND a back-reference pointer ADDED under the "## Leaves" list so future sessions
      can discover the new leaf. The pointer line must name the new leaf file.
    - Leave every other section of the trunk byte-identical.

  Output TWO fenced code blocks, clearly labelled:
    1. "=== NEW LEAF: HOLLOWMERE-RENDER-CACHE.md ===" then the leaf content.
    2. "=== UPDATED TRUNK: HOLLOWMERE.md ===" then the trunk with the section removed
       and the pointer added.
  Then the output envelope (schemaVersion, tier, status, tool_budget_used) on separate
  lines OUTSIDE the code blocks. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/leaf-extraction/
corpus_intent: |
  One file (HOLLOWMERE.md, 171 lines): a bloated trunk for the fictional Hollowmere
  domain. It contains an Overview, Pipeline stages, a self-contained "## Render-cache
  subsystem" section (with 5 sub-sections: Cache keys, Eviction policy, Cache metrics,
  Cache warming, Cache failure modes), a Brightwater bus contract, Operational notes,
  and a Glossary. This mirrors a typical personal-ops leaf-extraction protocol (extract a leaf
  + add a trunk pointer) on the fictional Hollowmere domain (codename hygiene mandatory;
  no real domain names). The eval is a TWO-PART check: (1) clean extraction boundary -
  the right self-contained section is extracted whole, nothing from neighbouring
  sections bleeds in or is left behind; (2) the trunk back-reference - a pointer to the
  new leaf is added to the "## Leaves" list (the real-world failure mode is extracting
  the content but forgetting the pointer, so future sessions cannot discover the leaf).

  QUALITY PRINCIPLE (correctness-first): the load-bearing requirement is the trunk
  pointer. An extraction that pulls the right content into a leaf but DROPS the pointer
  (leaving the trunk with no discovery path) is a silent loss - worse than a model that
  flags uncertainty. Equally bad: extracting a section that is NOT self-contained, or
  bleeding adjacent pipeline content into the leaf.

  ANSWER KEY (exact expected end-state):

    THE CORRECT SECTION TO EXTRACT = "## Render-cache subsystem" (and ALL FIVE of its
    sub-sections: ### Cache keys, ### Eviction policy, ### Cache metrics, ### Cache
    warming, ### Cache failure modes). It is the only section in the trunk explicitly
    described as "a self-contained component ... It does not share state with the
    pipeline stages above; it sits beside them." The Pipeline stages, Brightwater bus
    contract, Operational notes, Overview, and Glossary are all interdependent
    domain-core material and are the WRONG choices to extract.

    NEW LEAF (HOLLOWMERE-RENDER-CACHE.md) MUST CONTAIN:
      - A top-level heading naming the leaf.
      - The full "Render-cache subsystem" prose intro.
      - ALL FIVE sub-sections verbatim: Cache keys (12 rules), Eviction policy (12 rules),
        Cache metrics (12 metrics), Cache warming (10 steps), Cache failure modes (10 modes).
      - NOTHING from the Pipeline stages, Brightwater bus, Operational notes, or Glossary.

    UPDATED TRUNK (HOLLOWMERE.md) MUST:
      - Have the entire "## Render-cache subsystem" section (heading through its last
        sub-section bullet) REMOVED from the body.
      - Have a NEW pointer line added under "## Leaves" naming the leaf, e.g.
        "- HOLLOWMERE-RENDER-CACHE.md - the render-cache subsystem reference".
      - Keep every OTHER section (Overview, Pipeline stages, Brightwater bus contract,
        Operational notes, Glossary) byte-identical.
      - The "## Brightwater bus contract" section now follows "## Pipeline stages"
        directly (the render-cache section that sat between them is gone).

  GREP-VERIFIABLE INVARIANTS (for the scoring Architect):
    - In the UPDATED TRUNK block: "## Render-cache subsystem" appears ZERO times in the
      body. "render_cache_hit_ratio" appears ZERO times. "Eviction rule" appears ZERO times.
    - In the UPDATED TRUNK block, under "## Leaves": a line naming "HOLLOWMERE-RENDER-CACHE.md"
      IS present. (This is the load-bearing pointer - its absence is the primary fail.)
    - In the UPDATED TRUNK block: "## Brightwater bus contract", "## Pipeline stages",
      "## Operational notes", and "## Glossary" all STILL appear (not extracted).
    - In the NEW LEAF block: "## Render-cache subsystem" or its content appears, AND all
      five sub-section markers appear: "Cache keys", "Eviction policy", "Cache metrics",
      "Cache warming", "Cache failure modes".
    - In the NEW LEAF block: "Brightwater bus contract" appears ZERO times, "Pipeline
      stages" appears ZERO times, "Glossary" appears ZERO times (no neighbour bleed).
    - "render_cache_hit_ratio" appears in the LEAF (it moved there, not deleted).

  Scoring guidance:
    - Correctness (hard-fail eligible) = the render-cache section is the extracted one,
      extracted whole, with the trunk pointer added. Extracting the wrong section, or
      omitting the pointer, is a confidently-wrong result.
    - Completeness = all five render-cache sub-sections present in the leaf; no content lost.
    - Hallucination (hard-fail eligible) = inventing content not in the trunk, or
      claiming a pointer was added when it was not.
    - Discipline = clean boundary (no neighbour bleed into the leaf; no extra trunk
      sections removed); other trunk sections byte-identical.
    - Format adherence = two labelled fenced blocks + envelope outside.
    - Voice match does NOT apply.
notes: |
  CHAT C domain-realistic personal-ops eval. Mirrors a typical personal-ops leaf-extraction
  protocol on the fictional Hollowmere domain (codename hygiene mandatory). TWO-PART
  check: (1) clean extraction boundary - the one genuinely self-contained section
  (Render-cache subsystem, the only one labelled "does not share state ... sits beside"
  the pipeline) is extracted whole, with no neighbour bleed and nothing left behind;
  (2) the trunk back-reference - a pointer to the new leaf is added to "## Leaves" so
  future sessions can discover it. The load-bearing failure is dropping the pointer
  (content moves, discovery path lost). A secondary trap is extracting an
  interdependent core section instead. Correctness and Hallucination are hard-fail
  eligible; Discipline covers the boundary cleanliness. The answer key gives the exact
  end-state and grep invariants. Standard four-phase /eval-pit flow against the frozen
  rubric/rubric.md. variant_pool 9 (3 models x N=3, effort inert). Corpus is the
  directory corpus/leaf-extraction/.
---

# Spec 83 - leaf-extraction

Given a bloated trunk reference doc (HOLLOWMERE.md), extract the single most
self-contained section into a new leaf and wire the trunk to point at it. This is a
two-part check that mirrors a typical personal-ops leaf-creation protocol on the neutral
fictional Hollowmere domain so no real codename leaks.

Part one is the extraction boundary: of all the trunk's sections, exactly one - the
Render-cache subsystem - is explicitly described as self-contained ("it does not share
state with the pipeline stages above; it sits beside them") and is the correct
extraction target. Its five sub-sections (cache keys, eviction policy, metrics,
warming, failure modes) move whole into the leaf, with no content from the
interdependent pipeline, bus-contract, operational, or glossary sections bleeding in.

Part two is the load-bearing requirement: a back-reference pointer to the new leaf must
be added under the trunk's "## Leaves" list. The real-world failure mode this eval
catches is a model that correctly extracts the content but forgets the pointer, leaving
the trunk with no way to discover the leaf - a silent loss. The correctness-first
principle holds: dropping the pointer, extracting the wrong (interdependent) section, or
bleeding neighbour content into the leaf are all confidently-wrong outcomes worse than
flagging uncertainty.

Correctness and Hallucination are hard-fail eligible; Discipline covers boundary
cleanliness and keeping the other trunk sections byte-identical. The answer key in
corpus_intent gives the exact expected end-state plus grep-verifiable invariants for the
scoring Architect. Voice match does not apply. Standard four-phase /eval-pit flow against
the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort inert per the
methodology). The corpus is the directory corpus/leaf-extraction/.
