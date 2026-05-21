# Sealed identity key - EXAMPLE-multi-file-synthesis

SEALED until Pass 2 of scoring. In a real eval the Architect does NOT open this
file until after every per-variant dimensional score is written in `scores.md`.
This reveal is what turns sealed scores into a model-attributed tally. In this
EXAMPLE folder the key is shown so a reader can see the full shape end to end.

This is a REDUCED-N example pool of 6 variants (A through F). The production
default is the full 12-variant pool (Haiku low/medium/high, Sonnet
low/medium/high/max, Opus low/medium/high/xhigh/max). Six is used here so the
reference stays legible.

| Label | Model | Effort | Relative cost (illustrative, vs Haiku low = 1x) |
|-------|-------|--------|--------------------------------------------------|
| A | Haiku 4.5 | low | 1x |
| B | Sonnet 4.6 | low | 5x |
| C | Sonnet 4.6 | high | 9x |
| D | Sonnet 4.6 | medium | 7x |
| E | Opus 4.7 | high | 30x |
| F | Sonnet 4.6 | low | 5x |

Notes on cost figures: the multipliers above are ILLUSTRATIVE placeholders for the
EXAMPLE only, chosen to make the cost-override mechanic legible. Real evals pull
current per-model input/output token pricing into the cost ratio. Do not treat
these multipliers as live pricing.

Pool composition note (intentional, for teaching value):
- Two Sonnet-low entries (B and F) demonstrate the within-family tiebreaker.
- B is a planted hallucination case (fabricates a SOC 2 audit, a v3.2.1 hotfix, and
  GraphQL pricing - none in the corpus) to show a Hallucination hard-fail.
- C is a planted instruction-following gate FAIL (omits the required output
  envelope frontmatter) to show that the binary gate eliminates otherwise-decent work.
