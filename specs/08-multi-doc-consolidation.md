---
task_category: multi-doc-consolidation
prompt_under_test: |
  You are a Consolidator. You are given several separate documents about one
  project/topic (scattered notes, specs, status updates, meeting summaries).
  Consolidate them into ONE structured plan a team lead could act on: group into
  themes, trace cross-document dependency chains, produce a prioritized open-risks /
  next-actions list that cites the source docs, and distinguish decided / in-progress
  / blocked items. Reconcile any conflicts between documents EXPLICITLY. Do not invent
  facts. Output envelope required (schemaVersion, tier, status, tool_budget_used). No
  em dashes. No emojis.
variant_pool: 9
corpus: corpus/multi-doc-consolidation/
notes: |
  MULTI-FILE DIMENSION PROBE. Spec 01 is the single-file extreme (40 threads in one
  file). THIS spec tests the MULTI-FILE dimension at the 5 to 15 doc range: 15
  separate documents about ONE fictional product launch ("Northwind Pulse"), each
  doc a different shape (project charter, three panel PRDs, raw customer research,
  data-pipeline notes, a risk register, two weekly status updates, a meeting summary,
  design/UX notes, billing-integration notes, security-review notes, GTM notes, and
  an open-questions parking lot). The docs cross-reference each other by name and the
  dependency chains are spread ACROSS docs, not contained in any one.

  Variant pool is 9, not 12. The methodology now treats reasoning effort as INERT
  (effort no longer materially separates variants), so this is a clean MODEL
  comparison: 3 models x N=3 - Haiku x3, Sonnet x3, Opus x3. Aggregate the 3 passes
  per model (mean weighted total); flag any model whose 3 passes diverge by more than
  0.5 as a consistency finding.

  Three deliberate CROSS-DOC CONFLICTS are planted - a good Consolidator must catch
  and reconcile each EXPLICITLY (name both source docs, do not silently pick one):
    1. Launch date - June 12 (charter, doc 01) vs June 19 (meeting summary doc 09,
       carried into status doc 13 and GTM doc 14). The later meeting supersedes;
       the strong answer says so AND names the stale charter.
    2. Billing-adapter owner - Priya (PRD doc 04, risk register doc 07) vs Marcus's
       team (billing-integration notes doc 11). Unreconciled in the source.
    3. Auth method - SSO (data-pipeline notes doc 06) vs email magic-link (design
       notes doc 10). This conflict is load-bearing: it blocks the security review
       from starting (doc 12), so flattening it loses a launch-blocking dependency.

  Dependency chains to trace: the aggregation service (doc 06) is a shared upstream
  blocking BOTH the Seat Usage panel (doc 02) and the API Volume panel (doc 03); the
  API Volume panel additionally needs the unassigned endpoint-tagging work (RISK-2,
  docs 03/07/08/13); the Billing panel (doc 04) depends on the Zentro adapter (doc 11)
  AND a hard security gate (RISK-1, doc 12).

  Score emphasis: Completeness (all 15 docs' key points retained, none dropped) x
  Reasoning quality (dependency chains traced, all three conflicts reconciled rather
  than flattened) x structure (themed, not 15 flat summaries). Source transparency
  matters (next-actions must cite the doc numbers). Voice match does not apply.

  THRESHOLD GOAL: compare the practical winner here against the practical winner of
  spec 01 (single-file 40-thread). Spec 01 stresses raw item count in ONE file; this
  stresses cross-DOC reconciliation across many files. Together they locate the
  doc-count threshold where the top-tier model pulls ahead on multi-doc consolidation.
---

# Spec 08 - multi-doc-consolidation (the 5-to-15-doc multi-file probe)

The multi-file companion to spec 01. Where spec 01 is one file with 40 threads, this
is 15 SEPARATE documents about one fictional product launch ("Northwind Pulse") under
`corpus/multi-doc-consolidation/`. The documents are varied in shape (charter, PRDs,
raw customer notes, status updates, a meeting summary, risk register, security and
billing notes, GTM notes, and a parking lot) and they cross-reference each other.

The eval runs the standard `/eval-pit` four-phase flow against the frozen
`rubric/rubric.md`. Applicable dimensions: Reasoning quality (heavily - tracing the
cross-document dependency chains AND reconciling the three planted conflicts is the
core signal), Completeness (did it keep every doc's key points or silently drop some
of the 15), structure (themed consolidation vs 15 flat summaries), Source transparency
(citing the source docs in the next-actions list), Helpfulness, and Discipline. Voice
match does not apply.

The variant pool is 9 (3 models x N=3, effort treated as inert per the methodology -
see the notes field). The corpus is the directory `corpus/multi-doc-consolidation/`.
