---
task_category: cross-language-migration
prompt_under_test: |
  You are given a Python module at corpus/cross-language-migration/source.py - a
  small inventory-reservation helper. Port it to idiomatic Go.

  Requirements:
    1. Preserve ALL behaviour: the available() calculation, the non-negative on_hand
       validation, the positive-qty validation on reserve, the not-enough-available
       and unknown-sku failure cases on reserve, and the clamp-at-zero behaviour on
       release.
    2. Use idiomatic Go: a struct with methods, errors returned (not exceptions),
       a map-backed store, and a constructor function. Do not transliterate Python
       line-by-line - write what a Go engineer would write.
    3. Note any place where Go semantics force a deliberate decision that differs
       from the Python (for example, how you represent the "unknown sku returns None"
       case that Python expressed with Optional).
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis. Do not add features the source does not have.
variant_pool: 9
corpus: corpus/cross-language-migration/source.py
notes: |
  New task type. Tests porting fidelity plus idiomatic-target judgment. Watch for:
  silently dropping a validation (Completeness/Correctness), non-idiomatic
  transliteration like panicking instead of returning errors (Reasoning/Discipline),
  and whether the variant flags the Optional-to-(value, ok) decision (Source
  transparency / Reasoning). Correctness is hard-fail eligible - a port that changes
  the reserve failure semantics is wrong, not just stylistically off.
---

# Spec 04 - cross-language-migration (Python to Go)

Port the synthetic Python inventory helper at
`corpus/cross-language-migration/source.py` to idiomatic Go. Standard four-phase
flow against the frozen rubric. This is a code-correctness task, so Correctness and
Hallucination (inventing standard-library calls that do not exist) are the
load-bearing dimensions; Reasoning quality covers the idiomatic-translation
judgment. Voice match does not apply.
