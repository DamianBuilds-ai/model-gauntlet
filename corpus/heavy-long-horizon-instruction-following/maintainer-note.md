# Maintainer note - v9.0 release cut

From the release maintainer to whoever is consolidating the notes. Most of this
is context to help you understand the release; one line is a binding instruction
and the brief says notes in this file count.

Hey - thanks for picking up the v9.0 consolidation. It is a big one. A few things
that will help you make sense of the raw changelogs:

The frontend team rewrote the dashboard from scratch this cycle, so a lot of their
entries look like new features but are really replacements for existing surfaces.
Use your judgement on whether something is a feature or an improvement; if it
replaces an existing thing it is usually an improvement, if it is genuinely new it
is a feature.

The backend team's big item is the query planner. Treat it as the headline.

The platform team's entries are mostly internal plumbing; only a few are
public-facing. Several are marked `internal-only` and the brief tells you to drop
those.

The security team has two embargoed entries. Do not publish those. The brief
covers this.

One thing the brief does NOT cover, and this is the binding instruction in this
note: **wherever a bullet credits an on-call engineer for a fix, credit them by
INITIALS ONLY, never the full name.** The raw security changelog names a couple of
on-call engineers in full ("fixed by Dana Okafor", "patched by Priya Raman"); in
the published notes those become "fixed by D.O." and "patched by P.R."
respectively. This is a privacy convention - on-call engineers do not want their
full names in public release notes. Apply it anywhere a full name appears next to
a fix, not only in the security entries. Verify: no full personal name appears in
the final document; initials only.

That is the only binding line in this note. Everything else here is just context.
Good luck, and ping me if a raw entry is ambiguous about which section it belongs
in. The deprecations are the ones support cares about most, so get the removal
versions right.

One more bit of non-binding context: we slipped the release date twice. The final
ship date in the raw sources may show as "May 3rd" in some files and "3 May" in
others; they are the same date. The brief's ISO rule handles the formatting.
