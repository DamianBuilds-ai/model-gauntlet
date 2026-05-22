---
task_category: bug-fix-from-stacktrace
prompt_under_test: |
  You are given a buggy Python module at corpus/bug-fix-from-stacktrace/cart.py and
  the traceback it produces at corpus/bug-fix-from-stacktrace/traceback.txt. The
  module is a small shopping-cart discount engine. A test that adds items to two
  SEPARATE carts is failing.

  Produce:
    1. The ROOT CAUSE - the underlying defect, not the line the traceback points at.
       The crash site is a symptom; name the actual bug and explain why the symptom
       appears where it does.
    2. The MINIMAL correct fix - the smallest change that fixes the root cause without
       altering the module's intended behaviour or public API. Show the exact
       before/after lines (a unified diff or clearly-labelled snippet is fine).
    3. A ONE-LINE why: a single sentence stating why your fix addresses the root cause
       rather than masking the symptom.
  Do not rewrite the module, do not add features, do not "improve" unrelated code.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em
  dashes (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/bug-fix-from-stacktrace/
corpus_intent: |
  Two corpus files: a buggy module and its traceback. Quality is correctness-first and
  the whole eval is built so a weaker model can be CONFIDENTLY WRONG. The traceback
  points at a TypeError deep in the discount-application loop ("unsupported operand")
  - that is the SYMPTOM. The real root cause is a mutable default argument:
  Cart.__init__ uses `def __init__(self, items=[])` (a shared list created once at
  function-definition time), so every cart that does not pass items aliases the SAME
  underlying list. Items added to the first cart leak into the second cart, and the
  second cart ends up holding entries of an unexpected shape that blow up later in the
  discount math. The confidently-wrong fix is to patch the crash site - add a type
  guard or a try/except around the subtraction, or coerce the bad operand - which
  makes the traceback disappear while leaving the carts still sharing state (the
  discount totals stay silently wrong). A second plausible-but-wrong fix is to clear
  the list in __init__ (`items.clear()`), which mutates the shared default and merely
  moves the bug. The single correct minimal fix is the canonical
  `items=None` / `self.items = list(items) if items is not None else []` pattern. An
  incomplete-but-correct answer (names the mutable default, gives the None-guard fix,
  no extra polish) is far better than a confident symptom-patch that leaves carts
  aliased.
notes: |
  New task type. Root-cause debugging from a traceback where the crash site is a
  symptom and the defect is elsewhere. Differentiates on root-cause vs symptom (the
  central split - does the variant chase the TypeError line or find the shared mutable
  default in __init__), minimal-patch discipline (the None-guard one-liner vs a
  rewrite or a defensive try/except at the crash site), and reasoning quality (can it
  explain WHY items leak between carts and why the crash surfaces in the discount
  loop). Correctness is hard-fail eligible - a fix that silences the traceback but
  leaves the carts sharing state is a wrong answer, not a weaker one. Hallucination is
  hard-fail eligible - inventing a line, function, or import that is not in cart.py.
  Source transparency: cite the exact buggy line. Voice match does not apply. The
  corpus is the directory corpus/bug-fix-from-stacktrace/.
---

# Spec 11 - bug-fix-from-stacktrace

Find and fix the bug in `corpus/bug-fix-from-stacktrace/cart.py` given the traceback
at `corpus/bug-fix-from-stacktrace/traceback.txt`. Standard four-phase flow against
the frozen rubric. The defining split is root cause versus symptom: the traceback
points at a `TypeError` in the discount loop, but the real defect is a mutable default
argument in `Cart.__init__` that aliases one shared list across carts. Correctness is
hard-fail eligible - a patch that silences the traceback while leaving the carts
sharing state is wrong (the discount totals stay silently incorrect), so a confident
symptom-fix is worse than an incomplete-but-correct root-cause answer. Hallucination
(citing a line or API not in the file) is hard-fail eligible. Reasoning quality covers
the leak explanation; Scope discipline covers whether the variant resists rewriting
the module. Voice match does not apply. The corpus is the directory
`corpus/bug-fix-from-stacktrace/`.
