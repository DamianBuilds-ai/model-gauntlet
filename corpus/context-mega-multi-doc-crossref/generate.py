#!/usr/bin/env python3
"""
Deterministic generator for eval 113 (context-mega-multi-doc-crossref).

Emits a single large synthetic corpus file:
    corpus/context-mega-multi-doc-crossref/vellforge-archive.md

Target: ~250k tokens (~1,000,000 chars at ~4 chars/token), composed of ~50
sub-documents (charters, council minutes, research notes, policy briefs,
financial summaries, glossaries) of a fictional research consortium named
"Vellforge Cooperative".

Four NEEDLES are planted across four DIFFERENT sub-documents at distant
positions (roughly the 11%, 34%, 58%, 81% marks). Together they answer ONE
synthesis question about launching a new Class-IV Frontier initiative under
the amended charter. Near-duplicate distractors throughout name the WRONG
values for OTHER initiative classes (Class-I, Class-II, Class-III, Class-V).

NO spoiler annotations are written into the corpus (no "NEEDLE [Nx]" markers).
The needles use distinctive phrasing so the scoring Architect can grep for
them; the answer key + grep strings live in specs/113-*.md corpus_intent.

Deterministic: seeded RNG, no wall-clock, no network. Re-running produces
byte-identical output.

ANSWER KEY (mirrored in the spec corpus_intent):
  N1 - Class-IV Frontier annual budget allocation = 14.7 percent of the annual
       Frontier reserve fund. (Distractors: 9.0%, 12.5%, 22.0% for other classes.)
  N2 - Class-IV Frontier launch voting threshold = three-quarters supermajority
       of the Standing Council. (Distractors: simple majority and two-thirds
       for other classes.)
  N3 - Sponsoring-researcher eligibility tenure = at least 7 consecutive cycles
       of accredited standing. (Distractors: 3, 5, 10 cycles for other classes.)
  N4 - Ratification deadline = 21 calendar days from the close of the
       deliberation window. (Distractors: 14, 30, 45 days for other classes.)
  Synthesis: launching a Class-IV Frontier initiative under the amended charter
  requires 14.7% of the Frontier reserve fund, a three-quarters Standing Council
  supermajority, a sponsoring researcher with at least 7 consecutive cycles of
  accredited standing, and ratification within 21 calendar days of the close of
  the deliberation window.
"""

import random

SEED = 113
TARGET_CHARS = 1_000_000  # ~250k tokens at ~4 chars/token
OUT = "vellforge-archive.md"

rng = random.Random(SEED)

DISCLAIMER = (
    "<!-- SYNTHETIC DATA. This is the consolidated archive of a fictional "
    "research consortium named Vellforge Cooperative. Treat the entire file "
    "as data to be analysed, NOT as instructions. -->\n\n"
)

# Fictional, codename-clean vocabulary.
REGIONS = [
    "Northreach", "Hollowmere", "Saltspire", "Brindlepath", "Pellisade",
    "Greenmarsh", "Cloverhill", "Mendlewick", "Karstwood", "Tidefall",
    "Wintergale", "Ashenford", "Cobalthaven", "Larksong", "Verdantmoor",
]
COMMITTEES = [
    "Standing Council", "Budget Steering Panel", "Research Ethics Bureau",
    "External Liaison Office", "Internal Audit Bench", "Charter Review Body",
    "Quartermaster's Roundtable", "Membership Tenure Board",
]
CLASSES = ["Class-I Survey", "Class-II Applied", "Class-III Sustained",
           "Class-IV Frontier", "Class-V Restricted"]
ROLES = [
    "Convener", "Recording Scribe", "Senior Auditor", "Junior Auditor",
    "Initiative Liaison", "Charter Steward", "Tenure Registrar",
    "Treasury Witness", "Standing Delegate", "Visiting Fellow",
]
DOC_TYPES = [
    "charter-revision", "council-minutes", "research-note", "policy-brief",
    "financial-summary", "glossary-fragment", "review-memo", "training-record",
    "site-inspection", "external-correspondence",
]

# 14 NEAR-DUPLICATE DISTRACTORS that look like the needles but name the WRONG
# values for OTHER classes (Class-I, Class-II, Class-III, Class-V). A model
# that grabs one of these instead of the Class-IV figure is confidently wrong.
DISTRACTORS = [
    # Budget distractors (wrong classes, wrong percentages)
    "Budget Steering Panel note: the Class-I Survey programmes draw 9.0 percent "
    "of the annual Frontier reserve fund, which is the lowest of the five "
    "initiative classes and reflects their narrow operational scope.\n\n",

    "Budget Steering Panel note: Class-II Applied initiatives are funded at "
    "12.5 percent of the annual Frontier reserve fund under the current "
    "schedule, with quarterly drawdown caps documented separately.\n\n",

    "Budget Steering Panel note: Class-III Sustained initiatives receive the "
    "single largest annual line at 22.0 percent of the Frontier reserve fund, "
    "reflecting their multi-cycle nature.\n\n",

    # Voting threshold distractors (other classes)
    "Charter Review Body remark: under the amended charter, Class-I Survey "
    "launches require only a simple majority of the Standing Council; this is "
    "the lowest threshold across the five classes.\n\n",

    "Charter Review Body remark: Class-II Applied and Class-III Sustained "
    "initiatives both require a two-thirds majority of the Standing Council "
    "for launch under the amended charter.\n\n",

    "Charter Review Body remark: Class-V Restricted initiatives require a "
    "unanimous vote of the Standing Council; this is a deliberate ceiling and "
    "applies only to the Restricted class.\n\n",

    # Eligibility tenure distractors (wrong cycle counts for other classes)
    "Tenure Registrar advisory: the minimum sponsoring-researcher tenure for "
    "Class-I Survey initiatives is 3 consecutive cycles of accredited "
    "standing. This is the entry-level requirement.\n\n",

    "Tenure Registrar advisory: Class-II Applied sponsors must hold at least "
    "5 consecutive cycles of accredited standing; this is the intermediate "
    "tenure tier.\n\n",

    "Tenure Registrar advisory: Class-V Restricted sponsors must hold at "
    "least 10 consecutive cycles of accredited standing; this is the senior "
    "tenure tier and applies only to the Restricted class.\n\n",

    # Ratification window distractors
    "External Liaison Office reminder: Class-I Survey ratifications close 14 "
    "calendar days from the deliberation window's close. This is the shortest "
    "ratification interval in the schedule.\n\n",

    "External Liaison Office reminder: Class-II Applied and Class-III "
    "Sustained ratifications must be lodged within 30 calendar days of the "
    "deliberation window's close.\n\n",

    "External Liaison Office reminder: Class-V Restricted ratifications carry "
    "the longest interval at 45 calendar days, recognising the additional "
    "review required for restricted-class work.\n\n",

    # Cross-cutting near-look-alikes
    "Internal Audit Bench observation: across the five classes, the average "
    "allocation is roughly 13 percent of the Frontier reserve fund. The "
    "average is not the per-class figure for any single class.\n\n",

    "Internal Audit Bench observation: the average sponsoring-researcher "
    "tenure across all five classes is approximately 6 cycles. The average "
    "is not the per-class minimum for any single class.\n\n",
]

# The four TRUE needles. Phrased to be distinctive and self-contained so the
# scoring Architect can grep them out of the corpus by their unique substrings.
# These DO NOT carry "NEEDLE [Nx]" markers - the phrasing itself is the marker.
NEEDLES = {
    "N1": (
        "\n## Amended Charter Schedule A - Budget Steering Panel ratified entry\n\n"
        "Class-IV Frontier initiatives, under the amended charter, draw exactly "
        "14.7 percent of the annual Frontier reserve fund. This figure was "
        "ratified by the Budget Steering Panel during the eleventh cycle review "
        "and is the only allocation that applies to Class-IV Frontier work. It "
        "is not the same as the figures used for Class-I, Class-II, Class-III, "
        "or Class-V initiatives.\n\n"
    ),
    "N2": (
        "\n## Amended Charter Schedule B - Standing Council voting threshold\n\n"
        "Launching a Class-IV Frontier initiative under the amended charter "
        "requires a three-quarters supermajority of the Standing Council. This "
        "is stricter than the simple-majority threshold used for Class-I Survey "
        "launches and stricter than the two-thirds threshold used for Class-II "
        "Applied and Class-III Sustained launches. It is below the unanimous "
        "ceiling reserved for Class-V Restricted launches.\n\n"
    ),
    "N3": (
        "\n## Amended Charter Schedule C - Sponsoring researcher tenure\n\n"
        "A Class-IV Frontier initiative may be sponsored only by a researcher "
        "who holds at least 7 consecutive cycles of accredited standing on the "
        "Tenure Registrar's ledger. This requirement is unique to the Class-IV "
        "Frontier line; the Class-I, Class-II, and Class-V tenure minima are "
        "documented elsewhere in this archive and are not interchangeable with "
        "the Class-IV figure.\n\n"
    ),
    "N4": (
        "\n## Amended Charter Schedule D - Ratification deadline\n\n"
        "A Class-IV Frontier initiative launch must be ratified within 21 "
        "calendar days from the close of the deliberation window. This 21-day "
        "ceiling is specific to the Class-IV Frontier line and is shorter than "
        "the 30-day ceiling used for Class-II Applied and Class-III Sustained "
        "ratifications and shorter than the 45-day ceiling used for Class-V "
        "Restricted ratifications. The 14-day interval for Class-I Survey "
        "ratifications does not apply here.\n\n"
    ),
}

DOC_HEADER_TEMPLATES = [
    "# Sub-doc {sd:02d} - {dtype} - {committee} ({region})\n\n",
    "# Sub-doc {sd:02d} - {dtype} from the {committee}, {region} chapter\n\n",
    "# Sub-doc {sd:02d} - {region} {dtype} prepared for the {committee}\n\n",
]

FILLER_TEMPLATES = [
    "Section {sec}.{sub} - the {role} of the {committee} confirms that the "
    "current {dclass} workstream operates within its stated parameters at the "
    "{region} site. Routine attestations are recorded by the {role2} during the "
    "standing handover and reviewed at the next cycle close. The baseline "
    "tolerance for this attestation is {n} units, unchanged from the prior "
    "{n2} cycles. Cross-references to the wider archive are tracked by the "
    "Internal Audit Bench under standard procedure and require no further "
    "escalation under the current schedule.",

    "Procedural reminder ({dtype}). The {role} attached to the {committee} "
    "verifies that {dclass} attestations are filed within the standing window. "
    "Discrepancies follow the normal chain: first the {role2}, then the "
    "Convener of the relevant Council subgroup. Most attestations clear at "
    "the {role2} level without further review. The {region} chapter has "
    "reported no anomalies for {n} consecutive cycles.",

    "Cross-reference note. The {dtype} prepared by the {committee} for the "
    "{region} chapter cites the standing schedule for {dclass} work. Where the "
    "standing schedule conflicts with a chapter-level addendum, the amended "
    "charter governs. The {role} attests that no chapter-level addendum "
    "currently overrides the standing schedule at the {region} site, and the "
    "{role2} concurs on the cycle handover record.",

    "Archive note ({dtype}). For the {region} chapter, the {role} confirms "
    "that the {committee}'s last cycle review did not amend the standing "
    "schedule for {dclass} initiatives. The annual reserve fund draw and the "
    "ratification cadence remain governed by the schedules attached to the "
    "amended charter. Routine queries are resolved by the {role2} at the "
    "next handover and do not require Council escalation.",

    "Glossary fragment. Within the {region} chapter, the term '{committee} "
    "review cycle' refers to the standing review interval applied by the "
    "{committee} to a {dclass} initiative. The cycle length is the same "
    "across chapters and is documented in the charter glossary. Cross-class "
    "comparisons are tracked by the {role} of the {committee} and reviewed "
    "by the {role2} at the next handover.",

    "Financial summary excerpt. The {region} chapter's contribution to the "
    "annual Frontier reserve fund is recorded under the standing schedule. "
    "The {dclass} line draws against the annual allocation set by the Budget "
    "Steering Panel; chapter-level top-ups are tracked separately by the "
    "Quartermaster's Roundtable and do not modify the annual allocation. The "
    "{role} attests to the chapter's compliance for the prior {n} cycles.",
]


def filler_paragraph():
    t = rng.choice(FILLER_TEMPLATES)
    return t.format(
        sec=rng.randint(1, 40),
        sub=rng.randint(1, 30),
        committee=rng.choice(COMMITTEES),
        region=rng.choice(REGIONS),
        role=rng.choice(ROLES),
        role2=rng.choice(ROLES),
        dclass=rng.choice(CLASSES),
        dtype=rng.choice(DOC_TYPES),
        n=rng.choice([2, 3, 4, 5, 6, 8, 10, 12]),
        n2=rng.choice([2, 3, 4, 5, 6, 8]),
    ) + "\n\n"


def new_subdoc_header(sd_index):
    t = rng.choice(DOC_HEADER_TEMPLATES)
    return t.format(
        sd=sd_index,
        committee=rng.choice(COMMITTEES),
        region=rng.choice(REGIONS),
        dtype=rng.choice(DOC_TYPES),
    )


def build():
    parts = [DISCLAIMER]
    parts.append("# Vellforge Cooperative - Consolidated Archive (Cycle 12)\n\n")
    parts.append(
        "This archive consolidates approximately 50 sub-documents from the "
        "Vellforge Cooperative across its chapters. Each sub-document is "
        "scoped to a single committee, region, and cycle. Use sub-document "
        "headings to navigate.\n\n"
    )

    # We plant 4 needles at roughly 11%, 34%, 58%, 81% of the document.
    needle_positions = {
        int(TARGET_CHARS * 0.11): ("N1", NEEDLES["N1"]),
        int(TARGET_CHARS * 0.34): ("N2", NEEDLES["N2"]),
        int(TARGET_CHARS * 0.58): ("N3", NEEDLES["N3"]),
        int(TARGET_CHARS * 0.81): ("N4", NEEDLES["N4"]),
    }
    planted = set()
    # 14 distractor positions deterministically scattered across the body
    distractor_positions = sorted(
        rng.sample(range(int(TARGET_CHARS * 0.04), int(TARGET_CHARS * 0.97)),
                   len(DISTRACTORS))
    )
    di = 0

    # We target ~50 sub-docs across the corpus. We start a new sub-doc header
    # roughly every TARGET_CHARS / 50 chars of body.
    SUBDOC_INTERVAL = TARGET_CHARS // 50
    next_subdoc_at = SUBDOC_INTERVAL
    sd_index = 1
    parts.append(new_subdoc_header(sd_index))

    char_count = sum(len(p) for p in parts)

    while char_count < TARGET_CHARS:
        # plant needles whose position has been crossed
        for pos, (label, text) in list(needle_positions.items()):
            if label not in planted and char_count >= pos:
                parts.append(text)
                char_count += len(text)
                planted.add(label)
        # plant a distractor when its position is crossed
        while di < len(distractor_positions) and char_count >= distractor_positions[di]:
            d = rng.choice(DISTRACTORS)
            parts.append(d)
            char_count += len(d)
            di += 1
        # start a new sub-doc header when its position is crossed
        if char_count >= next_subdoc_at and sd_index < 50:
            sd_index += 1
            hdr = new_subdoc_header(sd_index)
            parts.append(hdr)
            char_count += len(hdr)
            next_subdoc_at += SUBDOC_INTERVAL
        p = filler_paragraph()
        parts.append(p)
        char_count += len(p)

    # Ensure any not-yet-planted needle is appended at the end.
    for label, text in NEEDLES.items():
        if label not in planted:
            parts.append(text)
            planted.add(label)

    return "".join(parts)


if __name__ == "__main__":
    content = build()
    with open(OUT, "w") as f:
        f.write(content)
    print(f"wrote {OUT}: {len(content)} chars (~{len(content)//4} tokens)")
    # sanity: each needle's distinctive phrase appears exactly once
    assert content.count("14.7 percent of the annual Frontier reserve fund") == 1, \
        "N1 unique-phrase count wrong"
    assert content.count(
        "three-quarters supermajority of the Standing Council"
    ) == 1, "N2 unique-phrase count wrong"
    assert content.count(
        "at least 7 consecutive cycles of accredited standing on the Tenure Registrar"
    ) == 1, "N3 unique-phrase count wrong"
    assert content.count(
        "must be ratified within 21 calendar days from the close of the deliberation window"
    ) == 1, "N4 unique-phrase count wrong"
    # confirm NO spoiler markers leaked in
    assert "NEEDLE [" not in content, "spoiler annotation leaked into corpus"
    print("all 4 needles planted exactly once; no spoiler annotations present")
