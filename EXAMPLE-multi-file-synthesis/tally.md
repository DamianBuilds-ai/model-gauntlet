# Tally - EXAMPLE-multi-file-synthesis

Pass 2/3: the sealed key in `variants/key.md` is now opened, weighted totals are
attributed to models, the within-family tiebreaker and cross-family cost-override
table from `rubric/rubric.md` are applied, and the two winners are reported.

---

## Headline

Quality winner: Sonnet 4.6 medium (weighted total 5.0/5.0)
Practical winner: Haiku 4.5 low (cost-override fired - 0.38 gap at 7x cost ratio, rubric section 5: cheaper wins in the 0.3-0.5 band at >= 3x)

---

## Reveal - labels to models

| Label | Model + effort | Weighted total | Gate | Outcome |
|-------|----------------|----------------|------|---------|
| D | Sonnet 4.6 medium | 5.00 | PASS | QUALITY WINNER |
| A | Haiku 4.5 low | 4.62 | PASS | PRACTICAL WINNER (cost-override) |
| F | Sonnet 4.6 low | 4.41 | PASS | - |
| E | Opus 4.7 high | 4.35 | PASS | - |
| B | Sonnet 4.6 low | (2.39) | gate PASS, Hallucination=1 | HARD FAIL - eliminated |
| C | Sonnet 4.6 high | (n/a) | gate FAIL | eliminated |

## Tiebreaker + cost-override trace

1. **Within-family tiebreaker (rubric section 4).** The only same-family pair within
   0.3 weighted total would be the two Sonnet-low entries (B, F). B is hard-fail
   eliminated (Hallucination=1), so no live intra-family tie exists. D (Sonnet medium,
   5.00) and F (Sonnet low, 4.41) are 0.59 apart - outside the 0.3 band - so no
   tiebreaker applies between them either. Nothing to resolve here.
2. **Cross-family cost-override (rubric section 5).** Quality winner D (Sonnet medium,
   ~7x illustrative cost) versus the cheapest passing variant A (Haiku low, 1x). Gap =
   5.00 - 4.62 = 0.38, which lands in the 0.3-0.5 band. Cost ratio 7x is >= 3x. The
   table says cheaper wins. Practical winner = A (Haiku 4.5 low).

## Per-dimension highlights

- **Correctness / Hallucination.** All four ranked variants are factually clean. The
  separation is NOT about getting facts wrong (except B) - it is about how much of the
  cross-file connection each one surfaces and how disciplined the output stays.
- **Reasoning quality (the core ask).** D is the only variant that explicitly reasons
  about COMBINED urgency (active customer impact x whether the fix path is decided),
  which is exactly what "top 3 by combined urgency" demanded. A does this implicitly;
  F and E less so.
- **Completeness.** A and D surface all three cross-file threads (webhooks, throughput,
  docs-lag). F drops the `carrier_reference` docs-lag thread (-> Completeness 3).
- **Scope discipline.** E is accurate but inflated past the "two-minute read" ask; the
  verbosity is its only real cost.

## Scoreboard row (append to the cross-eval Scoreboard)

| Task category | N variants | Quality winner | Practical winner | Cost-override fired? | Notes |
|---------------|-----------|----------------|------------------|----------------------|-------|
| multi-file-synthesis | 6 (reduced-N example) | Sonnet 4.6 medium (5.00) | Haiku 4.5 low (4.62) | yes (0.38 gap, 7x) | Sonnet medium flawless on structure; Haiku low wins practical on a clean tight synthesis. Opus high over-elaborated. |

## Surprises

1. **Opus high did NOT top the board.** It was fully correct and best-sourced but its
   verbosity cost it Scope discipline and Discipline, landing it 4th of the four ranked.
   Consistent with the broader pattern that effort tax shows up as over-elaboration.
2. **Haiku low beat two more expensive Sonnet/Opus variants on quality, not just cost.**
   At 4.62 it outscored both Sonnet low (4.41) and Opus high (4.35) outright, then took
   the practical win via the cost-override on top. For tight bounded synthesis the floor
   is lower than a route-by-vibes guess would put it.
3. **The two eliminations land for opposite reasons.** B is fluent but fabricates (the
   trap a careless human reviewer falls for); C is honest but ignored the envelope
   contract. Sealed scoring plus the binary gate catch both classes.

---

## Paste-back return block

Copy this into the origin chat to update the routing map:

```
EVAL COMPLETE: multi-file-synthesis (EXAMPLE, reduced-N=6)

Quality winner:   Sonnet 4.6 medium  (5.00/5.0, flawless cross-file synthesis)
Practical winner: Haiku 4.5 low      (4.62/5.0, cost-override: 0.38 gap @ 7x -> cheaper wins)

Eliminated:
  - Sonnet 4.6 low (B): Hallucination hard-fail (fabricated SOC 2 / hotfix / pricing)
  - Sonnet 4.6 high (C): instruction-following gate FAIL (missing output envelope)

Routing implication: for bounded multi-file synthesis where the inputs are present
and the ask is "connect the threads + prioritize", Haiku low is the practical route.
Reserve a higher tier only when the synthesis requires deeper judgment than this
corpus demanded. Opus high showed effort-tax verbosity with no quality buy here.

Caveat: reduced-N=6 EXAMPLE with illustrative cost multipliers. Re-run at the full
9-variant model-only pool with live pricing before locking this into the routing map.
```

---

## Note on this folder

This `EXAMPLE-multi-file-synthesis/` folder is a STATIC TEACHING REFERENCE showing
the exact end-to-end shape of one eval (corpus -> prompt -> variants -> sealed key
-> scores -> tally). It is NOT part of Stan's live run path. Live runs are driven by
`specs/NN-slug.md` definitions, produce transient results in `outbox/`, and ship via
`scripts/send-eval.sh` to a `run/<timestamp>` branch. See `commands/eval-run.md`.
