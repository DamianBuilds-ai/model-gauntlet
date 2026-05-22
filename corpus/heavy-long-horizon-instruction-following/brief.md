# Release-notes consolidation brief - Cardinal Platform v9.0

You are the release editor for Cardinal Platform, a fictional developer platform
shipped by Northwind Software. Four teams (frontend, backend, platform, security)
have each filed a raw changelog under `raw/`. Your job is to consolidate them into
a single, polished, public-facing `RELEASE-NOTES-v9.0.md` for the v9.0 release.

This brief is long on purpose. Read all of it before you start writing, because
several requirements are stated in the running prose rather than the numbered
list, and a handful of requirements live in `style-guide.md` and
`maintainer-note.md` rather than here. Treat every requirement as binding whether
it sits in a numbered item or in a sentence.

## Background context (read, but this section contains no instructions)

Cardinal Platform has shipped quarterly for three years. v9.0 is the largest
release of the year. It bundles a new query planner, a redesigned dashboard, a
move to a new authentication provider, and the deprecation of two long-standing
APIs. The four raw changelogs are written in each team's own style and are
inconsistent: some use friendly dates ("May 3rd"), some use ticket prefixes, some
bury breaking changes inside feature bullets. Marketing wants a clean, scannable
document. Support wants every breaking change and every deprecation called out so
they can prep customers. Security wants their section handled carefully because
two of their entries are still under embargo until the patch ships.

The previous release (v8.4) notes are not provided and you should not invent or
reference them.

## The numbered requirements

1. Produce exactly ONE output document and put it at `RELEASE-NOTES-v9.0.md`. Do
   not produce per-team files.

2. Begin the document with a single H1 heading reading exactly
   `# Cardinal Platform v9.0` and nothing else on that line.

3. Immediately under the H1, write a 2 to 3 sentence summary paragraph of the
   release. Do not use a bulleted list for the summary; it must be prose.

4. Organise the body into exactly these five H2 sections, in this order:
   `## Highlights`, `## New features`, `## Improvements`, `## Breaking changes`,
   `## Deprecations`. Do not add, rename, merge, or reorder these five sections.

5. Every entry in `## New features`, `## Improvements`, `## Breaking changes`, and
   `## Deprecations` is a single bullet beginning with `- `. The `## Highlights`
   section is the exception: it is a numbered list (`1.`, `2.`, `3.`) of exactly
   the THREE most significant items of the release, chosen by you.

6. Each feature, improvement, breaking-change, and deprecation bullet must end
   with the originating ticket id in parentheses, e.g. `(FE-1203)`. The ticket id
   is taken verbatim from the raw source. A bullet with no ticket id in the raw
   source is dropped (see requirement 19 about untriaged entries).

7. Do NOT alphabetise the bullets. (Counter-default note: a tidy editor instinct
   is to sort alphabetically; do not. The required sort is stated in the prose
   below, requirement-by-prose.)

8. The `## Deprecations` section must explicitly state, for each deprecated API,
   the version in which it will be REMOVED, taken from the raw source. A
   deprecation bullet that omits the removal version is incomplete.

9. Render EVERY date in the document in ISO 8601 format (`YYYY-MM-DD`). The raw
   sources use friendly formats ("May 3rd", "3 May", "05/03"); convert them all.
   The release year is 2026 for any date whose year is not stated. (Counter-
   default note: do not preserve the friendly source format even though it reads
   nicely; ISO is mandatory for this document.)

10. Use British spelling throughout (organise, behaviour, colour, prioritise,
    licence as a noun). The raw sources mix American and British; normalise to
    British.

11. The `## Security` material is special. Do NOT create a `## Security` H2
    section. Instead, fold the NON-embargoed security entries into
    `## Improvements` and `## Breaking changes` as appropriate, each tagged with a
    leading `[security]` token before the bullet text, e.g.
    `- [security] Rotated signing keys ... (SEC-22)`. The two EMBARGOED security
    entries (the raw source marks them `EMBARGO: do not publish`) must be OMITTED
    entirely from the public notes.

12. After the five sections, add a final H2 `## Upgrade notes` containing a short
    prose paragraph (not bullets) describing the single most disruptive upgrade
    step, which is the authentication-provider migration. Keep it under 80 words.

13. Do NOT include any entry whose raw text contains the marker `WIP` or
    `internal-only`; those are not for the public notes.

14. Where a raw bullet describes BOTH a feature and a breaking change in one
    sentence, SPLIT it into two bullets: one in `## New features` and one in
    `## Breaking changes`, each carrying the same ticket id. (This is the
    one-to-many split rule; do not leave a breaking change buried inside a
    feature bullet.)

15. The total document must be no longer than 130 lines (the consolidated notes
    are meant to be scannable; if you exceed 130 lines you have included too much).

16. Do not use the em dash anywhere in the output; use spaced hyphens. Do not use
    emojis.

17. End the document with a single horizontal rule (`---`) followed by exactly one
    line: `Generated for the v9.0 release. Questions: release-team internal channel.`
    Nothing after that line.

18. Each entry must appear EXACTLY ONCE in the whole document, except for the
    deliberate feature-or-breaking split in requirement 14 (where one ticket
    legitimately appears in two sections). No other duplication across sections.

19. Untriaged entries (those with no ticket id) are listed separately: collect
    them under a SHORT comment block at the very TOP of the file, ABOVE the H1,
    using HTML comment syntax `<!-- untriaged: ... -->`, one per line, so they are
    invisible in the rendered page but preserved for the editor. Do not silently
    discard them and do not show them in the visible body.

Several more requirements are stated in the prose paragraphs that follow, and a
few live in the style guide and the maintainer note. Find them all.

## Requirements stated in prose (these are binding too)

Within each of the four bulleted sections, sort the bullets by ticket NUMBER
ascending, treating the numeric part only (so FE-9 comes before FE-1203 only if
9 < 1203; here it does, so FE-9 first). The team prefix is ignored for sort
purposes; only the integer after the hyphen drives the order. This is the sort
rule referenced by requirement 7, and it is the one editors most often get wrong
because it is stated here in prose and not in the numbered list.

The summary paragraph required by requirement 3 must NAME the new query planner
explicitly by its product name, which the raw backend changelog calls the
"Cardinal Query Planner". Do not abbreviate it to CQP in the summary; the full
name must appear at least once.

Any entry that the raw source marks with `(beta)` keeps the `(beta)` token
immediately before its ticket id, e.g. `- New streaming export (beta) (BE-77)`.
Do not drop the beta marker and do not move it elsewhere in the bullet.

The phrase used to introduce the breaking-changes section matters to support: do
NOT soften it. The first line under `## Breaking changes` must be a single prose
sentence reading exactly `These changes require action before upgrading.` before
any bullets. No other section gets an intro sentence.

Finally on ordering: although the natural instinct is to lead a release-notes
document with security, for THIS document the `## Breaking changes` and
`## Deprecations` sections come AFTER `## Improvements` (per requirement 4 they
are positions four and five), and there is NO standalone security section at all
(per requirement 11). Keep that order exactly; do not promote security to the top.

## A final word

Accuracy beats completeness-theatre. If you cannot place an entry confidently, it
is better to put it in the closest correct section than to invent a new section
or duplicate it. Do not claim in any closing note that you followed an instruction
you did not follow; this document is read by support engineers who will act on it,
so a confidently-wrong "all dates converted" when one friendly date slipped
through is worse than the slip itself. There is no separate self-report section
required; just produce the document correctly.
