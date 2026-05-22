# Blueprints - Agent Formation Catalog

Named formations users can invoke conversationally instead of typing out full agent dispatch specs. Saves typing + protects main session context + standardizes patterns.

> **How to invoke:** Say the codename in chat (e.g., "spray 5 on the queue files" or "lock"). A main-session hook detects the keyword and reads this catalog, then executes the formation per spec.

---

## Slot grammar

```
<codename> [on <topic>] [-N <count override>] [--model <model> --effort <effort>]
```

Examples:

- `spray-5 on diary themes` - run spray-5 formation with topic
- `recon-3 across queue, handoff, and decisions` - run recon-3 with multi-target topic
- `lock` - dispatch single Architect-on-Max over existing in-session work
- `distill-6 on the builder fleet outputs` - compress 6 file paths to chat
- `eval-4-pit on theme synthesis` - prompt-eval framework run with 4 variants

---

## Recognition mechanism

Hook keyword detection (lazy-load). Regex example: `\b(recon|spray|lock|distill|forge|eval)-?(\d+|\w+)?\b` (word-boundary, codename-shape). Plus standalone `\block\b`.

When a blueprint codename is detected, main session reads this file, finds matching entry, executes formation.

Optional namespace prefix `bp:` to disambiguate from future workflow / command names: `bp:forge-1` (resolves explicitly to this catalog).

---

## Starter catalog (7 blueprints)

### recon-3

- **Formation:** 3 Haiku Scouts parallel, 1 file each
- **Tally:** none (raw scout returns to chat)
- **When to use:** Unknown territory mapping; need to see what's in 3 specific files fast
- **When NOT:** Synthesis needed (use spray-5 instead)
- **Per-agent budget:** HARD_MAX 4, SOFT_BUDGET 2
- **Cost class:** $ (cheap)

### spray-5

- **Formation:** 3 Haiku Scouts + 2 Sonnet Analysts (parallel)
- **Tally:** Sonnet medium synthesis (5-line BLUF)
- **When to use:** Research with synthesis across 3+ sources; cost-conscious
- **When NOT:** Deep judgment calls (use spray-10 or ad-hoc Architect)
- **Per-agent budget:** Scouts 4/2, Analysts 8/5
- **Cost class:** $$ (medium)

### spray-10

- **Formation:** 3 Haiku Scouts + 4 Sonnet Analysts + 2 Opus Architects medium + 1 Sonnet Builder (parallel)
- **Tally:** Architect-on-Max (Opus high effort)
- **When to use:** Full design fleet for major architectural decisions
- **When NOT:** Single-question lookups (overkill)
- **Per-agent budget:** Per-tier defaults; Architect tally 6/3
- **Cost class:** $$$ (heavy)

### lock

- **Formation:** 1 Architect-on-Max (Opus high effort) reads in-session context + prior agent outputs
- **Tally:** self (this IS the tally)
- **When to use:** Final decision call over existing work; "tally up what you think is best"
- **When NOT:** Fresh research (use spray-N)
- **Per-agent budget:** HARD_MAX 6, SOFT_BUDGET 3
- **Cost class:** $$ (one big call)

### distill-N

- **Formation:** 1 Haiku Scout (Distiller variant) reads N existing markdown file paths
- **Tally:** none (compression only, no decision)
- **When to use:** Compress N agent-outputs files to chat-safe summary (~30 lines); chat hygiene after fleet returns
- **When NOT:** Synthesis or decision needed (Distiller does NOT decide; it summarizes)
- **Per-agent budget:** HARD_MAX 3, SOFT_BUDGET 2; output cap 30 lines
- **Critical rule:** Distiller MUST include one-line attribution per source file. If a claim cannot be attributed, flag with `[unattributed]`
- **Cost class:** $ (cheap)

### forge-1

- **Formation:** 1 Drafter (Sonnet medium, voice-stable)
- **Tally:** none
- **When to use:** Single voice-stable output (cover letter, recruiter reply, follow-up email)
- **When NOT:** Voice-CRITICAL one-shots (stay in main session or use a dedicated Drafter Plus formation)
- **Per-agent budget:** HARD_MAX 6, SOFT_BUDGET 4
- **Cost class:** $$ (one Sonnet call)

### eval-N-pit

- **Formation:** N model variants running the same prompt in parallel with sealed identity labels. Default N=9 - the model-only pool (Haiku x3, Sonnet x3, Opus x3, labels A through I). Effort is not a current dispatch dimension (the Agent tool pins `model:` only).
- **Tally:** Architect-on-Max with 9-dimension rubric + binary instruction-following gate per `METHOD.md`
- **When to use:** Prompt-eval framework run; pit tiers / specialists / effort against each other on the same task
- **When NOT:** Tier choice already obvious (skip the eval)
- **Per-agent budget:** Per variant: HARD_MAX 5, SOFT_BUDGET 3; Architect tally: HARD_MAX 6, SOFT_BUDGET 4
- **Standard variant count:** 9 (model-only default - Haiku x3, Sonnet x3, Opus x3) or 3-6 (reduced N when targeting a specific question, e.g., "is Sonnet enough?")
- **Reference:** `METHOD.md` for full variant pool spec; `commands/eval-pit.md` for the slash form
- **Cost class:** $$$ (multi-variant)

---

## Cap and lifecycle

- **Active blueprints capped at 12** to keep mental model scannable. Starter catalog ships with 7.
- **Quarterly audit:** codenames invoked 0 times in 90 days -> DEPRECATED. After 180 days -> archived.
- **Adding a new blueprint:** propose via your project's queue / decision log; Architect ratifies + adds row.
- **Codename collision check:** before adding, grep your project's `commands/` directory and any workflow names. If collision, use `bp:` namespace prefix.

---

## Available tiers (7 canonical)

Blueprints can compose any of these tiers:

1. **Scout** (Haiku) - retrieval, quick factual research, state lookups
2. **Analyst** (Sonnet low/med) - research, pattern finding, multi-source comparisons
3. **Builder** (Sonnet low/med) - mechanical execution with verification
4. **Scribe** (Sonnet med) - voice-stable structured writing
5. **Engineer** (Opus low) - execution with local judgment calls (Decisions Made log)
6. **Researcher** (Opus low) - deep external research + best-of-N picks
7. **Architect** (Opus med/high) - design, deep research, ADR-level work

Plus 5 specialists supplementing: Janitor, Verifier, Pruner, Router, Drafter.

Future blueprints may compose Researcher (for deep-research formations) or Scribe (for voice-stable batch drafting). Starter 7 blueprints intentionally use existing Scout / Analyst / Builder / Architect / Drafter only - extend as patterns emerge.

---

## Changelog

- **v1.0** (2026-05-19): Starter catalog locked. 7 blueprints (recon-3, spray-5, spray-10, lock, distill-N, forge-1, eval-N-pit).
- **v1.1** (2026-05-19): Slot grammar formalized, recognition mechanism via hook regex documented.
- **v1.4 update** (2026-05-19): `eval-N-pit` default variant count changed from 6 to 12 (full effort spectrum). Per no-gaps comparison ask - sweep entire tier / effort matrix unless a specific question warrants a reduced-N run.
- **v1.5 update** (2026-05-22): `eval-N-pit` default moved to a 9-variant model-only pool (Haiku x3, Sonnet x3, Opus x3, labels A through I). Effort was dropped as a dispatch dimension because the Agent tool pins `model:` only. Effort is not a current dispatch dimension (may be revisited).

---

## Related docs

- [README.md](README.md) - framework overview
- [METHOD.md](METHOD.md) - prompt-eval methodology (`eval-N-pit` blueprint sources its rubric here; same as `/eval-pit` slash command)
- [commands/eval-pit.md](commands/eval-pit.md) - `/eval-pit` slash command (slash form of `eval-N-pit` blueprint)
- [EVIDENCE.md](EVIDENCE.md) - N=10 cross-eval findings (informs blueprint tier choices)
