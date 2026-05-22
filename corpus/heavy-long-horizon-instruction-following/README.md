# Corpus - heavy-long-horizon-instruction-following (the 30-scattered-instructions probe)

A long instruction brief plus a large set of source material. The model must
produce a SINGLE consolidated release-notes document for a fictional product
("Cardinal Platform") that obeys THIRTY explicit sub-instructions. The
instructions are scattered: some sit in the numbered task list, several are
buried mid-paragraph in the prose brief, a few live inside the source files
themselves (a style guide and a maintainer note), and three are deliberately
counter-default (they override what a model would naturally do).

This is the heavy, scaled-up analog of ordinary instruction-following: at three
or four instructions every model complies, but at thirty scattered across a long
context the cheaper models start to DROP the buried ones (recall failure on
instructions) while still obeying the obvious top-of-list ones.

All content is synthetic. Fictional company: "Cardinal Platform" by "Northwind
Software". No real people are named.

## The task

Read `brief.md` (the instruction brief), `style-guide.md` (the house style, which
itself contains binding instructions), `maintainer-note.md` (a note that contains
one binding instruction), and the four raw changelog source files under `raw/`.
Produce ONE consolidated `RELEASE-NOTES-v9.0.md` document for the v9.0 release
that follows every instruction.

## Files

- `README.md` - this file.
- `brief.md` - the primary instruction brief (most of the 30 instructions live
  here, several buried mid-paragraph).
- `style-guide.md` - the Cardinal house style guide. Contains binding formatting
  instructions (these COUNT toward the 30).
- `maintainer-note.md` - a short note from the release maintainer. Contains one
  binding instruction (it COUNTS toward the 30) and a lot of non-binding context.
- `raw/team-frontend.md` - raw frontend-team changelog entries (long).
- `raw/team-backend.md` - raw backend-team changelog entries (long).
- `raw/team-platform.md` - raw platform-team changelog entries (long).
- `raw/team-security.md` - raw security-team changelog entries (long, includes
  embargoed items the brief tells you to handle specially).

## Why this discriminates

Thirty explicit instructions over a long context. A model under load tends to
obey the first handful and the visually-salient ones (the numbered list, the
big headings) and silently drop the buried ones: the mid-paragraph "sort within
each section by ticket number ascending" rule, the style-guide "never use the
word simply" rule, the maintainer-note "credit the on-call engineer by initials
only" rule, and the three counter-default overrides (do NOT alphabetise; keep
the security section LAST not first; render dates as ISO not the friendly format
the sources use). The scored discriminator is the COUNT of the thirty
instructions genuinely satisfied in the output document - verified by reading the
output against the answer key, not the model's self-report - with a confidently
-wrong claim (asserting an instruction was followed when the document violates it)
penalised hardest.

The exhaustive instruction key with the location of each instruction and how to
verify it is in the spec's `notes` field (the answer key).
