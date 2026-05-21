# Higher-N rerun corpus - verbatim-capture

Synthetic meeting transcript for a fictional "Acme" team. The verbatim-capture task
asks the model to extract specific statements WORD-FOR-WORD (no paraphrasing) and
attribute each to the speaker. Tests retrieval discipline: the failure mode is
"helpfully" rewording a quote.

---

Mara: I think we should freeze the schema before the migration, not during it.
Changing columns mid-migration is how we corrupted the staging data last time.

Devin: Agreed on the freeze. My only worry is the reporting team has a deadline on
Friday and the freeze blocks their new column.

Priya: Then let us land the reporting column first, today, and start the freeze
tomorrow morning. That gives them the column and protects the migration.

Mara: Works for me. To be explicit: freeze starts tomorrow 9am, no schema changes
until the migration is verified complete.

Sol: I will post the freeze window in the team channel so nobody is surprised. And I
will add a CI check that rejects schema-changing migrations during the freeze.

Devin: One more thing - can we agree the rollback plan is to restore from the
pre-migration snapshot, not to hand-edit rows? Hand-editing is what bit us before.

Mara: Yes. Rollback equals restore-from-snapshot. No hand-editing. Write that down.
