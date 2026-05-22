# tickets.csv loader - notes

This directory holds `tickets.csv`, a small export from the Cardinal support tool. We
need a per-priority count and the total of `amount_cents` across all data rows.

## Known gotcha (read before you load this)

The previous quick-and-dirty loader did `line.split(",")` on each row and broke on this
exact file: several rows came out with the wrong number of columns, the totals were off,
and a couple of rows had stray quote characters in them. The export is a normal CSV but
the `notes` column contains free text - some entries have commas inside them, and at
least one has a quoted phrase inside the note. A plain comma split tears those rows
apart and shifts every column after `notes`, so `amount_cents` ends up reading a
fragment of the note text instead of the number.

The header row is the source of truth for the column count: there are exactly 5 columns
(`ticket_id, customer, priority, notes, amount_cents`). If your parse produces a row
with anything other than 5 fields, the parse is wrong - do not push past it.
