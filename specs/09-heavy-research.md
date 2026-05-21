---
task_category: heavy-research
prompt_under_test: |
  You are a Researcher. Given the source documents, do deep synthesis: state your
  explicit decision criteria up front, recommend the single best option, justify with
  evidence cited from the sources, name the rejected alternatives and why, and flag
  any source you found unreliable or outdated and why you discounted it. Reconcile
  conflicting sources into one coherent, self-consistent recommendation. Output
  envelope required. No em dashes.
variant_pool: 9
corpus: corpus/heavy-research/
notes: |
  HEAVY MULTI-SOURCE RESEARCH PROBE. A deep synthesis task, heavier than a small-scale
  research eval. 16 separate synthetic source docs under corpus/heavy-research/ on ONE
  technical decision: a fictional logistics-SaaS company "Riverbend" choosing ONE of
  three analytics platforms (Lumen Cloud - managed warehouse; Strato DB - self-managed
  open-source columnar; Beacon Analytics - managed bundle with built-in BI) to
  standardise on for three years. The sources are varied (decision brief, three vendor
  one-pagers, two independent benchmark write-ups, a three-year cost analysis, an
  ops/postmortem note, a compliance memo, a community forum thread, an analyst note,
  two internal Slack-thread captures, a scaling projection, a support/SLA comparison,
  and a weighted requirements checklist).

  Variant pool is 9, not 12. Reasoning effort is treated as INERT under the current
  methodology, so this is a clean MODEL comparison: 3 models x N=3 - Haiku x3,
  Sonnet x3, Opus x3. Aggregate the 3 passes per model (mean weighted total); flag any
  model whose 3 passes diverge by more than 0.5 as a consistency finding.

  The tradeoffs are deliberately SPREAD so NO single doc has the whole picture:
    - Cost (three-year TCO incl. people cost): doc 07.
    - Latency: docs 05 and 06 (benchmarks) plus doc 14 (scaling projection).
    - Operational burden: docs 08 (postmortem) and 15 (support/SLA), reinforced by 07.
    - Scaling / concurrency: doc 14.
    - Compliance / EU residency: doc 09.
  A strong answer assembles these into one coherent picture rather than treating each
  doc in isolation.

  TWO SUBTLE TRAPS (no obvious metadata tell - the signal is buried in body text):
    1. Doc 05 (benchmark write-up A) is OUTDATED. It has NO date stamp. The only tells
       are in prose: it tested "Strato DB version 2.1", says "two major releases since"
       and that "Lumen introduced its high-performance tier after we published." Its
       headline 3x-4x Strato latency lead does NOT hold on current versions - doc 06
       (newer, 5 TB, current versions) shows the gap narrowed to ~1.3x with autoscaling
       favouring Lumen under concurrency. A strong Researcher CATCHES that doc 05 is
       stale and discounts its numbers, preferring doc 06.
    2. Doc 10 (community forum thread) is a LOW-RELIABILITY single-voice source -
       "free and fast, set it and forget it" enthusiasm with no team size, data volume,
       or incident history, directly contradicted by the costed postmortem (doc 08) and
       cost model (doc 07). A strong Researcher names it as weak evidence and does not
       let it override the costed analysis.

  There is no single "correct" pick mandated, but the evidence, read carefully, points
  to Lumen Cloud for Riverbend (small 3-engineer team makes ops burden decisive against
  self-managed Strato; Beacon is ruled out by the current EU BI-layer compliance gap in
  doc 09 AND its interactive-latency-at-concurrency weakness in docs 06/14). A weaker
  answer that fell for the stale benchmark would over-rate Strato on raw speed; one
  that trusted the forum thread would under-weight ops cost. The eval rewards the
  REASONING and SOURCE HANDLING, not merely the final letter.

  Score emphasis: Reasoning quality (synthesis depth, did it CATCH the stale benchmark
  trap and the weak forum source and reconcile the conflicting benchmarks), Source
  transparency (cited WHICH source backs each claim, named what it discounted and why),
  Completeness (covered the rejected alternatives and the spread tradeoffs). Voice match
  does not apply. This finds where the top-tier model's research depth - specifically
  trap-catching and multi-source reconciliation - justifies its cost over cheaper models.
---

# Spec 09 - heavy-research (deep multi-source synthesis with planted traps)

A heavy research-and-synthesis eval over 16 separate synthetic source documents under
`corpus/heavy-research/`, all bearing on ONE technical decision: which of three
analytics platforms a fictional company ("Riverbend") should standardise on for three
years. The tradeoffs (cost, latency, ops burden, scaling, compliance) are distributed
across the sources so that no single document contains the whole picture, and two
sources are deliberately unreliable (one outdated benchmark with the staleness hidden
in body text, one low-reliability forum thread).

The eval runs the standard `/eval-pit` four-phase flow against the frozen
`rubric/rubric.md`. Load-bearing dimensions: Reasoning quality (depth of synthesis,
catching the planted traps, reconciling the two conflicting benchmarks into one
coherent recommendation), Source transparency (citing which source backs each claim,
explicitly naming and justifying any discounted source), and Completeness (covering the
rejected alternatives and the spread-out tradeoffs). Hallucination is hard-fail eligible
if a variant invents platform facts not present in the sources. Voice match does not
apply.

The variant pool is 9 (3 models x N=3, effort treated as inert per the methodology -
see the notes field). The corpus is the directory `corpus/heavy-research/`.
