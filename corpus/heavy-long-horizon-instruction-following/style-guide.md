# Cardinal Platform - house style guide (release notes)

This is the Northwind Software house style for public release notes. Most of this
document is background you already know; a handful of rules are binding for the
v9.0 consolidation and the brief tells you to treat them as such. The binding
rules are marked **BINDING** in bold. Everything not marked BINDING is guidance
that does not count as a hard requirement for this exercise.

## Voice and tone

Cardinal release notes are written for working developers. They are direct,
concrete, and free of marketing adjectives. We describe what changed and what the
reader must do, not how excited we are about it.

**BINDING - never use the word "simply".** The word "simply" (and "just simply",
"simply use", etc.) is banned from Cardinal release notes because it implies the
reader should find something easy and is condescending when they do not. Rewrite
any source bullet that uses "simply" to remove the word without changing meaning.
Verify: the substring "simply" (case-insensitive) must not appear anywhere in the
final document.

**BINDING - no exclamation marks.** Release notes never use the exclamation mark.
If a raw source bullet ends in `!`, replace it with a full stop. Verify: the
character `!` does not appear in the final document.

## Headings and structure

We use sentence case for prose but the section H2s in this release are fixed by
the brief (Highlights, New features, Improvements, Breaking changes, Deprecations,
Upgrade notes). Follow the brief's casing for those exactly.

This is guidance, not binding: prefer short bullets over long ones; one idea per
bullet; lead with the verb.

## Links and code

**BINDING - inline code formatting for identifiers.** Every API name, function
name, configuration key, environment variable, and CLI flag mentioned in a bullet
must be wrapped in backticks (inline code). For example a bullet mentioning the
`auth.provider` config key or the `cardinal login` command must backtick them.
Verify: API/function/config/flag tokens appear inside backticks, not as bare
prose.

This is guidance, not binding: external links use reference-style markdown where
possible. (Not enforced for this exercise; the raw sources contain no external
links anyway.)

## Numbers and units

This whole subsection is guidance, not binding. Spell out numbers below ten in
prose; use numerals in bullets. Use SI units. Use a thin space as a thousands
separator in prose. None of this is enforced for the v9.0 consolidation.

## A note on completeness

The release notes must reflect the shipped release accurately. Do not list a
feature that was cut. The raw sources are the source of truth; if a team's raw
changelog does not mention something, it is not in this release.
