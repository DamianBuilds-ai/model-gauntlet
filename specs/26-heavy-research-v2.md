---
task_category: heavy-research
prompt_under_test: |
  You are a Researcher. Given the source documents under
  corpus/heavy-research-v2/, do deep synthesis and deliver a decision-grade
  recommendation. Your output MUST contain ALL of the following, explicitly:

    1. A RANKED recommendation of the options (1st, 2nd, and any disqualified),
       not just a single pick.
    2. EXPLICIT WEIGHTING MATH. The corpus contains a weighted requirements
       instrument. Apply it: state the hard gate first, then for every option that
       passes the gate show the per-dimension weight, the per-dimension score, and
       the arithmetic that produces each option's weighted total. Show the sum, not
       just the final number.
    3. A NAMED DISQUALIFIER. State which option is disqualified, by which specific
       hard requirement, and cite the source. A disqualified option is ranked last
       and excluded from the weighted comparison; do not let a high feature score
       rescue it.
    4. A STATED CONFIDENCE per major claim (e.g. high / medium / low), with one
       phrase on what drives that confidence (which source, how reliable).
    5. SOURCE HANDLING: cite which source backs each load-bearing claim; explicitly
       NAME any source you discount and say why (stale, single-voice, conflicted,
       contradicted by a more reliable source). Reconcile conflicting sources into
       one coherent recommendation rather than averaging or silently picking a side.

  Do not invent facts not present in the sources. Output envelope required
  (schemaVersion, tier, status, tool_budget_used). No em dashes (spaced hyphens). No
  emojis.
variant_pool: 9
corpus: corpus/heavy-research-v2/
corpus_intent: 16 varied synthetic source docs on one vendor-selection decision (support platform for a small EU-bound logistics team) with a weighted requirements instrument, a hard compliance gate that disqualifies one option, and four planted unreliable sources (one stale benchmark, one single-voice forum thread, one conflicted analyst note, one inflated vendor uptime claim)
corpus_delivered: TBD
corpus_match: TBD
notes: |
  HEAVY MULTI-SOURCE RESEARCH PROBE v2 (the tightened redo of spec 09). Same family as
  09 (deep synthesis over many varied sources with planted traps and spread tradeoffs),
  but the PROMPT IS TIGHTER so judgment errors become visible and scorable rather than
  hiding behind a vague "recommend something" instruction. The four new prompt
  requirements - a ranked recommendation, explicit weighting MATH, a named disqualifier,
  and a confidence per claim - convert the soft "did it reason well" question into
  concrete pass/fail checks. A model that buries the weighting, skips the disqualifier,
  or asserts everything at flat confidence now visibly under-delivers. Re-running the
  09 family this way gives a second sample of the heavy-research category AND sharpens
  the discriminator.

  The corpus is a NEW scenario (a support-platform selection for a small EU-bound
  logistics team, "Cardinal Freight"), deliberately NOT the analytics scenario from 09,
  so a model cannot pattern-match the old answer. It keeps 09's two trap archetypes (a
  stale benchmark with the staleness hidden in body text; a low-reliability single-voice
  forum thread) and ADDS TWO more unreliable-source traps: an analyst note with a
  DISCLOSED conflict of interest (recommends the platform its own firm earns
  implementation revenue from), and an inflated VENDOR UPTIME CLAIM (99.99 percent
  self-reported) contradicted by an independent status-page audit (99.5 percent
  measured). Four traps total.

  Variant pool is 9, not 12. Reasoning effort is treated as INERT under the current
  methodology, so this is a clean MODEL comparison: 3 models x N=3 - Haiku x3,
  Sonnet x3, Opus x3. Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding.

  The tradeoffs are SPREAD so no single doc has the whole picture:
    - Cost (three-year fully-loaded TCO incl. people time): doc 07, reinforced 13.
    - Operating burden / no-platform-engineer fit: docs 08 (postmortem), 12 (eng
      Slack), 15 (support/SLA), reinforced by 07.
    - Peak-season scaling: docs 06 (current benchmark) and 14 (scaling projection),
      with doc 08 as the concrete failure case.
    - Reliability / uptime: doc 06 (independent measured) vs doc 03 (vendor claim).
    - Compliance / EU residency (the hard gate): doc 09, mapped in doc 16.
    - The weighting instrument itself: doc 16.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a confidently-wrong synthesis
  is worse than an incomplete one. A model that recommends the disqualified option
  because it scored well on features, or that quotes the stale 3x-4x throughput lead as
  current, or that repeats the 99.99 percent vendor uptime as fact, has produced a
  decision-grade output that MISLEADS - worse than an honest "I am less sure here."
  Flag any confidently-wrong claim for an extra penalty.

  ANSWER KEY (for the scoring Architect). The evidence, read carefully, points to a
  clear and VERIFIABLE answer.

  CORRECT RANKING:
    1st: Helmsdesk (managed all-in-one).
    2nd: Quillstack (self-hosted open source).
    Disqualified (ranked last): Beaconreach (managed AI bundle).

  THE NAMED DISQUALIFIER (must be stated):
    Beaconreach is disqualified by the HARD EU data-residency gate (doc 09, mapped in
    doc 16 Step 1). Its bundled AI assist + analytics layer processes EU customer
    contact data OUTSIDE the EU today (doc 04), the layer cannot be separated from the
    product (doc 04), and EU residency for it is roadmap-only. A roadmap promise does
    not satisfy a present legal obligation (doc 09). A strong answer names Beaconreach,
    names the EU-residency hard requirement, cites doc 09 (and/or 04/16), and ranks it
    last - it does NOT let Beaconreach's strong features or comparable cost rescue it.
    A model that ranks Beaconreach first or second on features has made a hard error.

  THE WEIGHTING MATH (doc 16 is the instrument; the arithmetic is fixed and checkable).
  Among gate-passers (Helmsdesk, Quillstack), weighted score = sum((weight/100)*score):
    Helmsdesk  = 0.30*5 + 0.25*5 + 0.20*5 + 0.15*4 + 0.10*3
               = 1.50 + 1.25 + 1.00 + 0.60 + 0.30 = 4.65 / 5.
    Quillstack = 0.30*2 + 0.25*1 + 0.20*2 + 0.15*2 + 0.10*5
               = 0.60 + 0.25 + 0.40 + 0.30 + 0.50 = 2.05 / 5.
    Beaconreach = DISQUALIFIED at the gate; no weighted score computed.
  Dimensions + weights (doc 16): operating burden 30, three-year cost 25, peak scaling
  20, reliability 15, throughput headroom 10. A strong answer reproduces this math (the
  exact totals 4.65 and 2.05, or a clearly-shown equivalent computation), shows the
  per-dimension contributions, and explains WHY Helmsdesk wins (it dominates the two
  heaviest dimensions - operating burden and cost - which decide it for a team with no
  platform engineer). Quillstack's ONLY strength (throughput, the lowest weight at 10)
  cannot overcome its losses on the heavy dimensions. A model that skips the math, or
  that just asserts a winner without the weighting, under-delivers on requirement 2.

  THE FOUR UNRELIABLE-SOURCE TRAPS (a strong answer NAMES each and discounts it):
    TRAP-1 (stale benchmark). Doc 05 (benchmark write-up A) is OUTDATED - no date
        stamp; the tells are in prose: it tested "Quillstack version 2.1", says "two
        major releases since" and that "Helmsdesk introduced its high-throughput
        Business tier connection pooling AFTER we published." Its headline 3x-4x
        Quillstack throughput lead does NOT hold on current versions; doc 06 (current
        versions, peak profile) shows the gap narrowed to ~1.3x with autoscaling
        favouring the managed option under concurrency. A strong Researcher CATCHES
        that doc 05 is stale and prefers doc 06. Quoting the 3x-4x as current is a
        confidently-wrong error.
    TRAP-2 (single-voice forum). Doc 10 (community forum thread) is a low-reliability
        single-voice source - "free and fast, set it and forget it" enthusiasm from one
        user (quillfan88), no team size, ticket volume, peak-load history, or incident
        record, directly contradicted by the costed postmortem (doc 08), the cost model
        (doc 07), and the engineering Slack (doc 12). A strong Researcher names it weak
        and does not let it override the costed analysis.
    TRAP-3 (conflicted analyst). Doc 11 (analyst note) recommends Quillstack BUT
        discloses in a footnote that the analyst firm earns implementation/hosting
        revenue from Quillstack deployments - a conflict of interest. A strong
        Researcher flags the conflict and discounts the Quillstack-favourable view as
        non-independent, especially where it conflicts with the independent costed
        sources (06/07/08). The analyst note also UNDER-states Beaconreach's residency
        gap ("confirm with vendor") - a strong answer notes the analyst missed the
        disqualifier that doc 09 treats as hard.
    TRAP-4 (inflated vendor uptime). Doc 03 (Quillstack one-pager) claims 99.99 percent
        uptime (vendor self-reported). Doc 06 (independent status-page audit) measures
        99.5 percent for Quillstack hosted deployments. A strong Researcher uses the
        INDEPENDENT measured figure, not the vendor marketing number, and notes the
        discrepancy. Repeating 99.99 percent as fact is a confidently-wrong error.

  SPREAD-TRADEOFF COVERAGE (a complete answer assembles these rather than treating each
  doc in isolation): cost decisive against Quillstack for a no-engineer team (07/13);
  operating burden decisive (08/12/15); peak scaling favours managed autoscaling
  (06/14, failure case 08); reliability uses independent uptime (06 over 03); throughput
  is Quillstack's only edge but lowest-weighted and partly stale (05 stale vs 06).

  Scoring guidance:
    - Correctness (hard-fail eligible): is the ranking right (Helmsdesk 1st,
      Quillstack 2nd, Beaconreach disqualified-last) and is the weighting math correct
      (the 4.65 / 2.05 totals or a clearly-shown equivalent)? A wrong ranking -
      especially ranking the disqualified Beaconreach above a gate-passer - or wrong
      arithmetic is a Correctness failure.
    - Reasoning quality (heavily weighted): depth of synthesis - did it CATCH all four
      traps (stale benchmark, single-voice forum, conflicted analyst, inflated uptime),
      reconcile the two benchmarks (05 vs 06), apply the hard gate before the weighting,
      and explain WHY the heaviest dimensions decide it? This is where the top-tier
      model is hypothesised to separate.
    - Source transparency: did it cite which source backs each load-bearing claim, and
      explicitly NAME and justify each discounted source (05 stale, 10 single-voice, 11
      conflicted, 03 inflated)? Naming fewer than all four traps is an incomplete
      source-handling result.
    - Completeness: ranked all three options, covered the spread tradeoffs, produced the
      weighting math, the named disqualifier, AND a confidence per major claim. Missing
      any of the four mandated output elements is an explicit completeness gap - note
      which element is missing.
    - Hallucination (hard-fail eligible): inventing platform facts, fabricating a source,
      or asserting a number not in the corpus (e.g. a made-up uptime or cost figure).
    - Helpfulness / Discipline (decision task): is the recommendation decision-grade and
      actionable, and did it stay disciplined - applying the gate, discounting weak
      sources, and NOT averaging the disqualified option back into contention?
    Voice match does NOT apply.

    Suggested scoring shorthand for the Architect: (a) ranking correct? (b) weighting
    math reproduced (4.65 vs 2.05, gate applied first)? (c) Beaconreach named as
    disqualified by the EU-residency hard gate? (d) all four traps named and discounted?
    (e) confidence stated per major claim? A model that hits all five with clean source
    citations is the exemplary 5 on Correctness, Reasoning, and Source transparency. The
    most damaging single failures are: ranking Beaconreach above a gate-passer, quoting
    the stale 3x-4x lead as current, or repeating the 99.99 percent vendor uptime as
    fact - each is confidently-wrong and penalised hardest.
---

# Spec 26 - heavy-research-v2 (the tightened deep-synthesis redo of spec 09)

The tightened redo of spec 09. Same heavy-research family - deep synthesis over many
varied sources with planted traps and tradeoffs spread so no single doc holds the whole
picture - but the prompt is sharpened so judgment errors are visible and scorable. The
model must deliver a RANKED recommendation, EXPLICIT WEIGHTING MATH applied from the
corpus's weighted requirements instrument, a NAMED DISQUALIFIER (which option fails
which hard requirement, with a citation), a STATED CONFIDENCE per major claim, and clean
source handling that names and discounts the unreliable sources.

The corpus (`corpus/heavy-research-v2/`) is a NEW scenario - a small EU-bound logistics
team ("Cardinal Freight") choosing one of three customer-support platforms (Helmsdesk
managed all-in-one, Quillstack self-hosted open source, Beaconreach managed AI bundle) -
deliberately not the analytics scenario from spec 09, so the old answer cannot be
pattern-matched. It keeps spec 09's two trap archetypes (a stale benchmark with the
staleness hidden in prose, a low-reliability single-voice forum thread) and adds two
more: an analyst note with a disclosed conflict of interest, and an inflated vendor
uptime claim contradicted by an independent status-page audit. The evidence points to a
verifiable answer: Helmsdesk first (weighted 4.65), Quillstack second (2.05), Beaconreach
disqualified last by the hard EU data-residency gate.

The eval runs the standard `/eval-pit` four-phase flow against the frozen
`rubric/rubric.md`. Load-bearing dimensions: Correctness (right ranking, right weighting
arithmetic), Reasoning quality (catching all four traps, reconciling the two benchmarks,
applying the gate before the weighting), Source transparency (citing each claim, naming
and justifying each discounted source), and Completeness (all four mandated output
elements present). Hallucination is hard-fail eligible if a variant invents platform
facts or numbers. Voice match does not apply. The variant pool is 9 (3 models x N=3,
effort treated as inert per the methodology). The corpus is the directory
`corpus/heavy-research-v2/`.
