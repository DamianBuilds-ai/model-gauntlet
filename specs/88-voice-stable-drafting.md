---
task_category: voice-stable-drafting
prompt_under_test: |
  Draft a short announcement post for the fictional workshop Marlowe Forge. Two files
  are provided in the directory corpus/voice-stable-drafting/:

    - VOICE.md - the brand voice guide. Its rules are HARD rules.
    - topic-seed.md - the topic and the facts to convey.

  Write the post so that:
    - It follows EVERY rule in VOICE.md - both the banned constructs and the required
      style.
    - It states the content facts accurately (tool name, ship date, pricing, offline
      behaviour) exactly as VOICE.md specifies. Do NOT alter or "round" any fact.
    - It is roughly 120-180 words.

  Output ONLY the post text (no preamble, no explanation of your choices). Then append
  the required output envelope (schemaVersion, tier, status, tool_budget_used) as
  separate lines after the post. No em dashes (use spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/voice-stable-drafting/
corpus_intent: |
  Two fictional files: a brand voice guide (VOICE.md) with explicit HARD rules, and a
  topic seed (topic-seed.md) for an announcement post. The eval tests VOICE ADHERENCE
  UNDER TEMPTATION plus FACT ACCURACY - an announcement naturally tempts the exact
  constructs the voice guide bans (exclamation marks, hype superlatives, rhetorical
  questions, a CTA sign-off), and the facts have specific correct forms a careless
  draft will round or restate wrongly. All codenames fictional (Marlowe Forge,
  Benchplane).

  THE VOICE RULES THAT MUST HOLD (banned constructs - any single violation is a voice
  failure):
    V1. NO em dashes anywhere (only spaced hyphens).
    V2. NO exclamation marks (zero).
    V3. NO emojis.
    V4. NO rhetorical questions (no "?" used to address the reader).
    V5. NO the word "leverage".
    V6. NO the word "synergy".
    V7. NO hype superlatives: "revolutionary", "game-changing", "world-class",
        "cutting-edge", "best-in-class".
  Required style (must be present):
    V8. Opens with a concrete observation, not a claim.
    V9. First person plural ("we" / "our").
    V10. Ends with a single plain takeaway sentence, NOT a call-to-action sign-off.
    V11. Brand written exactly as "Marlowe Forge" (not stylized uppercase).

  THE CONTENT FACTS THAT MUST BE ACCURATE (any wrong fact is a content failure):
    F1. Tool name spelled exactly "Benchplane".
    F2. Ship date stated as 2026-03-09.
    F3. Pricing: free for the first 90 days, then a flat 12 dollars a month. NOT "free
        forever", NOT a percentage, NOT a different number, NOT free indefinitely.
    F4. Works fully offline - no account, no cloud needed. Do NOT claim it requires the
        cloud or an account to run.

  ANSWER KEY (for the scoring Architect). A passing draft satisfies ALL of V1-V11 AND
  ALL of F1-F4, is roughly 120-180 words, and reads as a Marlowe Forge announcement.
  The opening line should be a concrete observation (per the seed: the team losing time
  switching between three tools to plan one day) rather than a hype claim.

  THE FAILURE MODES TO DETECT (an announcement TEMPTS these - weaker models slip):
    - An exclamation mark (V2) - the single most common announcement-voice slip.
    - A hype superlative like "revolutionary" or "game-changing" (V7).
    - A rhetorical question opener like "Tired of switching between tools?" (V4).
    - A call-to-action sign-off like "Try it today" / "Get started now" (V10).
    - An em dash (V1).
    - A FACT error: "free forever" or a wrong price or wrong ship date (F3/F2), or
      claiming it needs the cloud/an account (F4), or misspelling Benchplane (F1).
    - Stylizing the brand as "MARLOWE FORGE" (V11).

  GREP-VERIFIABLE INVARIANTS (for the Architect):
    - The character `!` appears ZERO times in the post body.
    - No em dash character appears (only spaced hyphens).
    - The words `leverage`, `synergy`, `revolutionary`, `game-changing`, `world-class`,
      `cutting-edge`, `best-in-class` each appear ZERO times.
    - No `?` is used to pose a rhetorical question to the reader (a `?` count of 0 is the
      simplest pass; any `?` must be inspected and is almost certainly a V4 violation).
    - `Benchplane` is spelled exactly that way and appears at least once.
    - `2026-03-09` appears (the ship date) OR the date is stated in the same exact form.
    - `90 days` AND `12 dollars` (or "$12" / "12 a month") both appear; `free forever`
      appears ZERO times.
    - `offline` appears; no claim that it needs the cloud / an account to run.
    - `Marlowe Forge` appears exactly cased (no `MARLOWE FORGE`).
    - Word count is roughly 120-180 (a soft check; gross overrun/underrun is a format
      miss).
    - First-person plural ("we" / "our") is present.

  Scoring guidance:
    - Correctness (hard-fail eligible) = ALL voice rules held AND all facts accurate.
      Even one banned construct (an exclamation mark, a hype superlative, a rhetorical
      question, an em dash) is a voice failure; one wrong fact is a content failure.
      Either drops Correctness sharply.
    - Completeness = all four facts conveyed, opener is a concrete observation, plain
      takeaway close.
    - Hallucination (hard-fail eligible) = inventing a fact not in the seed (a feature,
      a different price, a fake testimonial) or restating a fact wrongly (free forever).
    - Discipline = the load-bearing discriminator here - holds EVERY voice rule under
      the announcement format's natural pull toward hype and CTAs.
    - Format adherence = post only (no meta commentary), envelope outside, ~120-180
      words, spaced hyphens.
    - Voice match APPLIES and is heavily weighted - this eval is explicitly about voice
      stability.
    - Reasoning quality = SKIP-eligible (output is the post, not reasoning).
notes: |
  Chat C domain-realistic eval (personal-ops / markdown-KB), the voice-stable-drafting
  task type. Unlike most gauntlet evals Voice match APPLIES and is heavily weighted. The
  scored discriminator is whether the model holds EVERY explicit voice rule (banned
  constructs V1-V7, required style V8-V11) under an announcement format that naturally
  tempts the banned constructs (exclamation marks, hype superlatives, rhetorical-question
  openers, CTA sign-offs, em dashes), while stating all four content facts accurately
  (name spelling, ship date, the exact 90-days-then-12-dollars pricing, offline
  behaviour). The corpus is a fictional VOICE.md with explicit rules plus a topic seed;
  the seed deliberately supplies a concrete observation hook (team losing time across
  three tools) so the required-observation opener is achievable from the material.
  Standard four-phase /eval-pit flow against the frozen rubric/rubric.md. Correctness and
  Hallucination are hard-fail eligible; the answer key (voice rules that must hold + the
  four content facts) plus grep-verifiable invariants are embedded in corpus_intent.
  Variant pool 9 (3 models x N=3, effort inert). Corpus is the directory
  corpus/voice-stable-drafting/. All codenames fictional - no real domain names.
---

# Spec 88 - voice-stable-drafting

Draft a short Marlowe Forge announcement post from a voice guide (VOICE.md) and a topic
seed (topic-seed.md). The corpus is those two fictional files.

The eval tests voice stability under temptation plus fact accuracy. The voice guide sets
hard rules - no em dashes, no exclamation marks, no emojis, no rhetorical questions, no
"leverage" / "synergy", no hype superlatives, plus required style (concrete-observation
opener, first person plural, plain takeaway close, exact brand casing). An announcement
is precisely the format that pulls a model toward the banned constructs: the exclamation
mark, the "revolutionary new tool" superlative, the "Tired of juggling tools?" rhetorical
opener, the "Try it today" call-to-action sign-off. The load-bearing discriminator is
holding every rule anyway.

Alongside voice, the four content facts have specific correct forms - the tool is the
"Benchplane", it shipped 2026-03-09, it is free for the first 90 days then a flat 12
dollars a month (not "free forever"), and it runs fully offline with no account or cloud.
A draft that rounds the pricing, claims free-forever, or says it needs the cloud fails on
content even if the voice is clean.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. Voice match
applies and is heavily weighted; Correctness and Hallucination are hard-fail eligible.
The answer key (the voice rules that must hold plus the four content facts) and
grep-verifiable invariants live in `corpus_intent` for the scoring Architect. The variant
pool is 9 (3 models x N=3, effort inert per the methodology). The corpus is the directory
`corpus/voice-stable-drafting/`.
