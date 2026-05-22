---
task_category: structured-extraction
prompt_under_test: |
  You are given a single messy intake document at
  corpus/structured-extraction/vendor-intake-notes.md - a procurement coordinator's
  raw, human-written notes describing several vendor records. Some fields are stated
  plainly, some are buried mid-sentence, some are implied, and some are genuinely
  absent.

  Extract EVERY vendor record into a JSON array. Each object MUST use exactly this
  schema, with these keys in this order and no others:

    {
      "vendor_name": string,
      "contact_name": string | null,
      "contact_title": string | null,
      "category": string,
      "payment_terms_net_days": integer | null,
      "annual_spend": number | null,
      "currency": string | null,
      "abn": string | null,
      "status": "active" | "pending",
      "onboarded_date": string | null
    }

  Rules:
    1. Output ONLY a single valid JSON array - no prose before or after it, no
       markdown code fences around extra commentary. (A fenced ```json block is fine;
       commentary outside it is not.)
    2. Use null for any field the document does not state. Do NOT invent, guess, or
       infer a value that is not supported by the text. An empty string is NOT null -
       use null.
    3. payment_terms_net_days is an integer number of days only (e.g. net 30 -> 30).
       annual_spend is a plain number in the stated currency's major units (e.g. 240k
       -> 240000). abn is the digits with the spacing as written, or null.
    4. status is exactly "active" or "pending" - lowercase, no other values.
    5. Do not add records that are not in the document. Do not merge two records.
  After the JSON array, append the required output envelope (schemaVersion, tier,
  status, tool_budget_used) as separate lines OUTSIDE the JSON. No em dashes (spaced
  hyphens). No emojis.
variant_pool: 9
corpus: corpus/structured-extraction/
corpus_intent: 8 vendor records in one messy prose document
corpus_delivered: TBD
corpus_match: TBD
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a subtly-wrong-but-plausible
  extraction that distorts the record is WORSE than an incomplete-but-honest one. A
  model that writes null for a field it cannot find is behaving correctly; a model that
  confidently fills net_days=30 from the "30 days lead time" red herring, or carries the
  retracted EUR currency, or invents a contact name, has produced confidently-wrong data
  that a downstream system would trust. Reward the honest null. Penalise the plausible
  fabrication hardest. Hallucination is hard-fail eligible here.

  NEW task type. Tests strict-schema adherence, null discipline, and resistance to
  embedded traps. Single source doc, 8 records. The differentiation is whether a model
  can hold a rigid schema while the prose actively fights it.

  ANSWER KEY (for the scoring Architect - the 8 records as the corpus actually states
  them):
    1. Brightwater Logistics - contact Dana Okafor, title head of accounts, category
       logistics, net 30, spend 240000, AUD, abn "51 824 753 556", active, onboarded
       2026-04-03 (stated "3rd of April"; accept "April 3" / "3rd of April" / ISO).
    2. Per Diem Catering - contact Marco (surname genuinely not given, so "Marco" is
       correct; title null - he is "the owner", borderline, accept null or "owner"),
       category food, net 14, spend 38000, AUD, abn null (promised, never sent),
       pending.
    3. Northbridge Cloud - contact Priya Sundaram, title enterprise account lead,
       category IT/software (accept "software" or "IT"), net 45, spend 1100000, USD,
       abn null (EIN given, explicitly "leave ABN blank"), active, onboarded
       2026-02-12. TRAP: must NOT put the EIN in abn.
    4. TBD Consulting - contact Tom Reilly, title null (he is the principal, no title
       given; accept null), category consulting, net 30 (floated, accept 30 or null
       since "nothing signed" - 30 is stated so 30 is defensible, null is also
       defensible; do NOT mark wrong either way), spend null, AUD, abn null, pending.
    5. Greenfield Maintenance - contact Sarah Lin, title null, category maintenance,
       net 60 (TRAP: the "30" is lead time, NOT terms; net_days=30 here is
       confidently-wrong), spend 85000, AUD, abn "88 102 938 217", active, onboarded
       2026-03-20.
    6. Atlas Stationery - contact null (genuinely not recorded), title null, category
       office supplies, net 30, spend 6000, AUD, abn "24 600 411 905", active,
       onboarded null (active "for ages", no date given - onboarded_date must be null,
       not invented).
    7. Cardinal Translation Services - contact Yuki Tanaka, title localisation
       manager, category translation, net 30, spend 70000 (the 70k figure stands;
       only the CURRENCY changed), currency AUD (TRAP: the EUR was retracted - "ignore
       the EUR mention"; currency=EUR is confidently-wrong), abn "33 555 010 200",
       pending.
    8. Coastal Print Co - contact Elena Voss (TRAP: the unnamed sales contact is a
       distractor; the relationship owner Elena Voss is the correct contact_name),
       title ops manager, category printing, net 21, spend 52000, AUD, abn
       "19 778 634 122", active, onboarded 2026-02-28.

  Scoring guidance: Correctness = field-level accuracy across all 8 records (the four
  traps - record 3 EIN-as-ABN, record 5 lead-time-as-terms, record 7 retracted EUR,
  record 8 wrong contact - are where a weaker model will be confidently wrong).
  Hallucination (hard-fail) = inventing a value where the text says null (e.g. a
  contact name for Atlas, a spend for TBD Consulting, an onboarded date for Atlas).
  Format adherence = exact schema, key order, types (integer days, numeric spend,
  lowercase status), and a clean JSON array. Completeness = all 8 records present.
  Discipline = honoured "null for missing, do not invent". Source transparency applies
  weakly (the doc is the only source). Voice match does NOT apply.
---

# Spec 13 - structured-extraction (strict schema vs messy prose)

Extract eight vendor records from one deliberately messy intake document at
`corpus/structured-extraction/vendor-intake-notes.md` into a strict, fixed JSON schema
defined in the prompt. The document states some fields plainly, buries others
mid-sentence, implies a few, and leaves several genuinely absent - and it plants four
traps where a plausible-looking value is actually wrong (an EIN that is not an ABN, a
lead-time "30" that is not the payment term, a retracted EUR currency, and a distractor
contact who is not the relationship owner).

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a model that writes
`null` for what it cannot find is correct, while a model that confidently fills a trap
value has produced wrong data a downstream system would trust - which is worse than an
honest omission. Correctness and Hallucination are hard-fail eligible. Format adherence
(exact schema, key order, JSON validity, lowercase enum status) and Discipline (null
over invention) are the load-bearing differentiators. Voice match does not apply. The
corpus is the directory `corpus/structured-extraction/`.
