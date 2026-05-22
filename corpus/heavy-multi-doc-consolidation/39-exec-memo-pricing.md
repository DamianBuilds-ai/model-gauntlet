# Helios Exec Memo - Pricing Direction

Author: VP Product (exec)
Status: proposal (LATER than the pricing plan doc 26)

## Recommendation

This memo recommends Helios adopt USAGE-BASED (consumption) pricing rather than per-seat
pricing. The argument: self-serve analytics customers have many occasional viewers (see
research doc 07, interview 3), and per-seat pricing suppresses adoption by charging for
every viewer. Usage-based pricing (billing on rows ingested or queries run) aligns cost with
value and removes the seat-count adoption barrier.

NOTE: the pricing plan (doc 26), written earlier, specifies PER-SEAT pricing. THIS exec memo,
written later, recommends USAGE-BASED. The pricing MODEL is therefore in conflict between doc
26 (per-seat) and this memo (usage-based) - risk register doc 12, RISK-12. The memo is later
and from an exec, but it is a RECOMMENDATION that has NOT yet been ratified into the plan, so
the conflict is genuinely UNRESOLVED, not silently superseded. A consolidator should surface
that the pricing model is contested (per-seat doc 26 vs usage-based exec memo doc 39), note
that the exec memo is the later proposal, and flag that until ratified the model is undecided.

## Downstream impact

If usage-based wins, the billing adapter (doc 22) must report metered consumption, the
billing surface (doc 04) usage meter becomes the billing basis (not just informational), the
GTM pricing page (doc 30) changes, and the analytics billing dimension (doc 27) changes. The
memo acknowledges this rework and asks for a decision before the billing adapter is finalized.
