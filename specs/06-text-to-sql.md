---
task_category: text-to-SQL
prompt_under_test: |
  You are given a database schema at corpus/text-to-sql/schema.sql and four
  natural-language questions at corpus/text-to-sql/questions.md (Q1 easy through Q4
  hard). For EACH question, produce a single SQL query that answers it against the
  given schema.

  Requirements:
    1. Use ONLY tables and columns that exist in schema.sql. Do not invent columns.
    2. Get the joins and aggregations right - especially Q3 (distinct customers per
       category, excluding cancelled orders) and Q4 (first-ever order in the same
       month as account creation, where that first order was cancelled).
    3. Return one labelled SQL block per question (Q1..Q4). State any assumption you
       make about ambiguous wording.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 12
corpus: corpus/text-to-sql/
notes: |
  New task type. Tests schema-grounded SQL generation across a difficulty gradient.
  Watch for: invented columns (Hallucination hard-fail), wrong join cardinality
  producing inflated sums on Q2 (Correctness), missing the not-cancelled filter on
  Q3 (Correctness/Completeness), and botching the first-order-per-customer window/
  subquery logic on Q4 (Reasoning quality). The corpus path is the DIRECTORY (schema
  plus questions); preflight validates the directory exists. Voice match does not apply.
---

# Spec 06 - text-to-SQL

Generate SQL for the four synthetic questions in `corpus/text-to-sql/questions.md`
against `corpus/text-to-sql/schema.sql`. Standard four-phase flow against the frozen
rubric. Correctness and Hallucination (no invented columns) are hard-fail eligible.
Reasoning quality is the differentiator on Q3 and Q4. Voice match does not apply. The
corpus is the directory `corpus/text-to-sql/`.
