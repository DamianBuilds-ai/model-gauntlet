---
task_category: patch-application
prompt_under_test: |
  You are given two files under corpus/patch-application/ for a fictional service
  (platform "Northwind", company "Globex"):

    - inventory.py    - a small Python module of inventory helpers (the target).
    - change.patch    - a unified diff (git format) describing the change to make.

  Apply the unified diff in change.patch to inventory.py EXACTLY, as `patch` or
  `git apply` would. The diff is the complete and authoritative change spec. Apply
  every hunk it contains, at the locations it names, and make NO other change. Do NOT
  add edits the diff does not contain, do NOT reformat or reorder anything outside the
  diff's hunks, and do NOT "improve" the surrounding code.

  The diff contains four hunks:
    - TAX_RATE changes from 0.10 to 0.15.
    - order_total gains a `discount=0` parameter and a `subtotal -= discount` line.
    - a new function total_units is inserted before restock_needed.
    - restock_needed's comparison changes from `<` to `<=`.

  Lines that are NOT touched by any hunk (the module docstring body, line_total,
  order_subtotal, and format_currency) must remain BYTE-IDENTICAL to the original.

  Output the COMPLETE patched content of inventory.py, from its first line to its last
  line, as a single fenced code block, with every hunk applied and nothing else
  altered. After the code block, append the required output envelope (schemaVersion,
  tier, status, tool_budget_used) on separate lines OUTSIDE the code block. No em dashes
  (spaced hyphens). No emojis. Do not add commentary inside the file content.
variant_pool: 9
corpus: corpus/patch-application/
corpus_intent: |
  Two files under corpus/patch-application/ (inventory.py - a 32-line Python module of
  inventory helpers; change.patch - a git-format unified diff with four hunks). The eval
  asks for a verbatim application of the unified diff to the target file: apply every
  hunk at the location it names, change nothing else, and leave every untouched line
  byte-identical. There is exactly one correct end-state - the file `git apply` would
  produce.

  THE SETTER TEST, PATCH FORM (Haiku-lightweight-apply vs Sonnet-Builder). A "Setter" is
  a cheap write/apply agent (Haiku) that, after a Scout retrieves, applies a
  fully-specified change itself - as opposed to the Builder (Sonnet, execution plus
  verification). Spec 49 tested a fully-specified apply in one file from a prose change
  spec; spec 50 spread it across several files; this spec gives the change as a UNIFIED
  DIFF, which is the most mechanical apply of all - the diff already encodes the exact
  before / after and the exact line locations. The hypothesis: applying a clean unified
  diff is the strongest case for the Setter, so Haiku should match Sonnet. The failure
  mode to detect is whether Haiku, instead of applying the diff verbatim, "interprets"
  it - applying a hunk at the wrong line, inventing a change the diff does not contain,
  re-deriving the code from the hunk descriptions instead of transcribing it, dropping a
  hunk, or reformatting untouched lines - where Sonnet applies all four hunks exactly and
  leaves the rest byte-identical.

  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a patched file that LOOKS done
  but mis-applied a hunk or drifted an untouched line is WORSE than one that honestly
  applies three of four hunks and flags the fourth. The highest-signal traps are all
  mis-apply or over-reach errors: (a) re-deriving the function bodies from memory rather
  than transcribing the original untouched lines verbatim (a confidently-wrong
  reconstruction - e.g. format_currency, which the diff never touches, comes back
  subtly rewritten); (b) applying the `discount` change to order_total but also changing
  the unrelated `tax` line or order_subtotal; (c) inserting total_units in the wrong
  place (the diff puts it AFTER order_total and BEFORE restock_needed) or with the wrong
  blank-line spacing; (d) flipping `<` to `<` instead of `<=`, or also changing
  line_total's body; (e) carrying the literal `+` / `-` / context-space diff markers into
  the output file. A model that produces exactly the file `git apply` would produce is
  correct; a model that re-imagines untouched code, or mis-locates a hunk, is confidently
  wrong. Over-reach and mis-apply are the heaviest penalties here.

  ANSWER KEY (for the scoring Architect - the exact end-state after applying all four
  hunks). Verify by comparing the model's output line-by-line against the original
  inventory.py and the four hunks in change.patch.

    1. The module docstring (lines 1-3) is UNCHANGED, byte-identical.

    2. TAX_RATE = 0.15 (was 0.10 - hunk 1). Appears once; `TAX_RATE = 0.10` appears
       zero times.

    3. line_total(quantity, unit_price) is UNCHANGED: `return quantity * unit_price`.

    4. order_subtotal(lines) is UNCHANGED (its three-line body - total = 0, the for loop
       over qty, price, the return total - is byte-identical).

    5. order_total now reads exactly (hunk 2):
         def order_total(lines, discount=0):
             subtotal = order_subtotal(lines)
             subtotal -= discount
             tax = subtotal * TAX_RATE
             return subtotal + tax
       The signature gained `discount=0`; a new `subtotal -= discount` line sits between
       the subtotal assignment and the tax line. The tax and return lines are otherwise
       unchanged.

    6. A NEW function total_units sits AFTER order_total and BEFORE restock_needed (hunk
       3), reading exactly:
         def total_units(lines):
             return sum(qty for qty, _ in lines)
       with one blank line of separation on each side, matching the file's existing
       two-blank-line spacing between top-level defs.

    7. restock_needed now reads `return on_hand <= threshold` (was `on_hand < threshold`
       - hunk 4). The signature `def restock_needed(on_hand, threshold):` is unchanged.

    8. format_currency(cents) is UNCHANGED, byte-identical (the diff never touches it):
         dollars = cents / 100
         return "$" + str(dollars)

    9. No diff markers (`+`, `-`, leading context spaces from the hunk, `@@ ... @@`
       headers, `diff --git`, `index`, `---`, `+++`) appear anywhere in the output file.

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - `TAX_RATE = 0.15` appears once; `TAX_RATE = 0.10` appears zero times.
    - `def order_total(lines, discount=0):` appears once; the old
      `def order_total(lines):` appears zero times.
    - `subtotal -= discount` appears exactly once.
    - `def total_units(lines):` appears exactly once and its `return sum(qty for qty, _
      in lines)` body appears exactly once; total_units sits between order_total and
      restock_needed.
    - `return on_hand <= threshold` appears once; `return on_hand < threshold` appears
      zero times.
    - `format_currency`, `line_total`, and `order_subtotal` bodies are unchanged
      (`return quantity * unit_price` appears once; `dollars = cents / 100` appears once;
      `return "$" + str(dollars)` appears once).
    - The output is valid Python (no stray `+` / `-` / `@@` diff markers, no leading
      context spaces, correct indentation), and there are exactly six top-level defs:
      line_total, order_subtotal, order_total, total_units, restock_needed,
      format_currency.

  Scoring guidance:
    - Correctness (hard-fail eligible) = all four hunks applied exactly at their named
      locations AND every untouched line byte-identical. Mis-locating a hunk, dropping a
      hunk, re-deriving untouched code, changing an unrelated line, or leaving diff
      markers in the file is Correctness=1 (a confidently-wrong patch that a downstream
      commit would trust).
    - Completeness = all four hunks present (TAX_RATE, order_total signature + line,
      total_units insert, restock_needed comparison).
    - Hallucination (hard-fail eligible) = inventing a change the diff does not contain,
      re-imagining an untouched function body, adding a fifth edit, or claiming "patch
      applied cleanly, nothing else changed" when an untouched line in fact drifted.
    - Format adherence = the complete patched file as one fenced code block, envelope
      outside it, valid Python, no diff markers leaked in.
    - Discipline = transcribed the untouched lines verbatim and applied ONLY the four
      hunks. This is the load-bearing Setter discriminator: a diff is applied, not
      interpreted or reconstructed.
    - Reasoning quality = SKIP-eligible (this is a near-pure apply); if reasoning is
      shown, it should not invent scope or re-derive untouched lines.
    - Source transparency applies weakly (one target file, one diff).
    Voice match does NOT apply. The scored discriminators are exact verbatim application
    of the four hunks and ZERO drift on untouched lines.
notes: |
  NEW task type and the third of the three Setter-vs-Builder probes (49-51). Spec 49
  tested a fully-specified deterministic apply in one file from a prose change spec; spec
  50 spread the same one-correct-answer determinism across several files plus a decoy;
  this spec gives the change as a git-format UNIFIED DIFF (four hunks) and asks for a
  verbatim application to a small Python module - the most mechanical apply of all, since
  the diff already encodes the exact before / after and the exact line locations. The
  question is whether applying a clean unified diff - the strongest case for the Setter -
  lets Haiku match Sonnet, or whether Haiku "interprets" the diff instead of transcribing
  it: mis-locating a hunk, re-deriving an untouched function body from memory, dropping a
  hunk, leaking diff markers into the file, or reformatting untouched lines, where Sonnet
  applies all four hunks exactly and leaves the rest byte-identical.

  The corpus (corpus/patch-application/) is two files: inventory.py (a 32-line Python
  module - TAX_RATE constant, line_total, order_subtotal, order_total, restock_needed,
  format_currency) and change.patch (a git-format unified diff with four hunks: TAX_RATE
  0.10 -> 0.15; order_total gains a discount=0 parameter and a subtotal -= discount line;
  a new total_units function inserted before restock_needed; restock_needed's comparison
  flipped from < to <=). The traps are all mis-apply or over-reach: re-imagining the
  untouched format_currency / line_total / order_subtotal bodies rather than transcribing
  them, inserting total_units in the wrong position, changing an unrelated line alongside
  a hunk, or carrying the literal +/-/context-space diff markers into the output. The
  correctness-first principle holds: a confidently-wrong patch (a mis-located hunk, a
  reconstructed untouched line, leaked diff markers) is worse than an honest partial that
  applies three hunks and flags the fourth. Correctness and Hallucination are hard-fail
  eligible; Discipline (a diff applied verbatim, not interpreted or reconstructed) is the
  load-bearing discriminator. The answer key gives the exact end-state plus
  grep-verifiable invariants. Voice match does not apply. Standard four-phase /eval-pit
  flow against the frozen rubric/rubric.md. The variant pool is 9 (3 models x N=3, effort
  inert per the methodology). The corpus is the directory corpus/patch-application/.
---

# Spec 51 - patch-application (the Setter test, patch form)

Apply a unified diff verbatim to its target file - every hunk at the location it names,
nothing else changed, every untouched line byte-identical - producing exactly the file
`git apply` would produce. This is the third of three Setter-vs-Builder probes (49
exact-single-file, 50 exact-multifile, 51 patch-application).

A "Setter" is Damian's term for a lightweight write/apply agent (Haiku) that, after a
Scout or Explorer retrieves, applies a fully-specified change itself - as opposed to the
Builder (Sonnet, execution plus verification). Spec 49 located whether the Setter is
safe on a fully-deterministic prose apply in one file; spec 50 spread it across several
files plus a decoy; this spec hands the change as a unified diff, which is the most
mechanical apply of all - the diff already encodes the exact before / after and the
exact line locations, so applying it is transcription, not inference. The hypothesis is
that this is the strongest case for the Setter and Haiku should match Sonnet; the
failure mode to detect is whether Haiku "interprets" the diff - applying a hunk at the
wrong line, re-deriving an untouched function body from memory, dropping a hunk, leaking
diff markers into the output, or reformatting untouched lines - where Sonnet applies all
four hunks exactly and leaves the rest byte-identical.

The corpus (`corpus/patch-application/`) is two files: `inventory.py` (a 32-line Python
module of inventory helpers) and `change.patch` (a git-format unified diff with four
hunks - TAX_RATE 0.10 to 0.15, an added `discount=0` parameter plus `subtotal -=
discount` line in order_total, a new `total_units` function inserted before
restock_needed, and restock_needed's comparison flipped from `<` to `<=`). Each hunk has
exactly one correct application. The traps are all mis-apply or over-reach:
re-imagining the untouched `format_currency` / `line_total` / `order_subtotal` bodies
rather than transcribing them, inserting `total_units` in the wrong position, changing
an unrelated line alongside a hunk, or carrying the literal `+` / `-` / context-space
diff markers into the output file.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a confidently-wrong patch
(a mis-located hunk, a reconstructed untouched line, leaked diff markers) is worse than
an honest partial that applies three hunks and flags the fourth. Correctness and
Hallucination are hard-fail eligible; Discipline - a diff applied verbatim, not
interpreted or reconstructed, with every untouched line byte-identical - is the
load-bearing discriminator, and the answer key provides the exact end-state plus
grep-verifiable invariants for the scoring Architect. Voice match does not apply. The
variant pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the
directory `corpus/patch-application/`.
