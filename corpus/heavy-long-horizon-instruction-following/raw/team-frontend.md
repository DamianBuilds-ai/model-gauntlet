# Frontend team - raw changelog for v9.0

These are the frontend team's raw entries, written in our own loose style. The
release editor will consolidate them. Dates are however whoever wrote the line
felt like writing them. Some of these are still works in progress and tagged WIP.

## Shipped this cycle

- FE-9: Rebuilt the dashboard shell from scratch. The new shell loads the side
  navigation, the top bar, and the content frame independently so a slow panel no
  longer blocks the whole page. This replaces the old monolithic dashboard mount.
  Landed May 3rd.

- FE-1203: New command palette. Press `cmd-k` to open a fuzzy command palette that
  can navigate to any page, run any saved query, and toggle theme. This is
  genuinely new, there was no palette before. Shipped 3 May.

- FE-880: Redesigned the settings page. The settings are now grouped into
  Account, Workspace, and Billing tabs instead of one long scroll. This replaces
  the old single-page settings. 05/03.

- FE-451: Dark theme is now the default for new workspaces and we removed the old
  high-contrast theme entirely. So this is two things really: dark theme by
  default (a feature for new users) AND the removal of the high-contrast theme
  (a breaking change for anyone who relied on it, since the `theme=high-contrast`
  URL parameter now 404s). Both under FE-451. Landed May 1st.

- FE-77: Added inline validation to all forms. Fields now validate on blur and
  show the error next to the field. Simply start typing and the error clears.
  Shipped April 28th.

- FE-1450: New keyboard-shortcuts help overlay. Press `?` anywhere to see the
  shortcuts. May 2nd.

- FE-203: Improved table rendering performance. Large tables (over 10,000 rows)
  now virtualise their rows and scroll smoothly. This is an improvement to the
  existing table, not a new component. 30 April.

- FE-1198: The dashboard now remembers your last-visited page and returns you
  there on next login. Improvement to existing navigation. May 2nd.

- FE-66: Accessibility pass on the whole app - every interactive element now has a
  visible focus ring and an aria-label. Improvement. April 29th.

## Still in progress (NOT shipping in v9.0)

- FE-1500: WIP - new charting library evaluation. Not shipping this cycle, still
  prototyping. Do not include.

- FE-1502: WIP - drag-and-drop dashboard layout. Behind a flag, not ready.

## Untriaged (no ticket assigned yet)

- Tweaked the loading spinner colour to match the new brand palette. No ticket
  filed yet, slipped in during the dashboard rebuild.

- Fixed a typo in the empty-state message on the saved-queries page. No ticket.

## Notes

The dashboard rebuild (FE-9) is the frontend headline but the backend query
planner is the release headline overall, per the maintainer. Our colour choices
moved to the new brand palette; we have been writing "color" in code and "colour"
in prose inconsistently, the editor will normalise. We use American spelling in
some of these bullets (color, behavior, prioritize) out of habit.
