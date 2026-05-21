# Requirements Checklist - Weighted

Synthetic corpus doc 16 of 16. Riverbend's own weighted requirements. Useful as a
scoring frame, but a Researcher should still state their OWN decision criteria up
front rather than just deferring to these weights.

## Weighted requirements (Riverbend's stated priorities)

| Requirement | Weight | Why |
|-------------|--------|-----|
| Low operational burden (small team) | High | Only 3 data engineers (doc 01) |
| EU data residency / compliance | High | Handles EU customer data (doc 01, doc 09) |
| Interactive dashboard latency at scale | High | ~50 concurrent users by year 3 (doc 14) |
| Predictable / bounded three-year cost | Medium | Finance prefers forecastable spend (doc 13) |
| Lowest raw license cost | Low | Matters less once people cost is included (doc 07) |
| Maximum control over the stack | Low | Not a stated business priority |

## How the options map (for the Researcher to verify, not copy)

- The two HIGH weights that most separate the field are operational burden and EU
  compliance.
- Low ops burden favours the managed options (Lumen, Beacon) over self-managed Strato.
- EU compliance currently rules Beacon's BI layer OUT (doc 09).
- Latency-at-scale favours Lumen and Strato over Beacon (doc 06, doc 14).

## Caution

These weights are Riverbend's own framing. A strong recommendation states its decision
criteria explicitly (which may adopt or adjust these weights) and justifies the single
pick against the EVIDENCE in the dossier - not merely by asserting the checklist. The
checklist is an input, not the answer.
