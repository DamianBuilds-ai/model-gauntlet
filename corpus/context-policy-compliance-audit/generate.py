#!/usr/bin/env python3
"""
Deterministic generator for eval 114 (context-policy-compliance-audit).

Emits TWO synthetic corpus files in this directory:
    corpus/context-policy-compliance-audit/ordinance.md        (~200k tokens)
    corpus/context-policy-compliance-audit/incident-log.md     (small)

The model is given the long ordinance and the separate incident-log fragment
and asked which specific ordinance clauses are violated by which log entries.

Five log entries each violate exactly ONE clause planted somewhere in the
~200k ordinance (clauses 7.4.2, 12.1.5, 18.6.3, 23.9.1, 31.5.7). Roughly
twelve other log entries are NEAR-VIOLATIONS that look like they violate
something but in fact do not (wrong zone, outside the regulated hours,
exempted category, below threshold, etc.).

NO spoiler annotations are written into either corpus file (no "VIOLATION
[Vx]" markers, no "DISTRACTOR" tags). Clauses are stored by their natural
ordinance numbering; the answer key + grep strings live in
specs/114-*.md corpus_intent.

Deterministic: seeded RNG, no wall-clock, no network. Re-running produces
byte-identical output.

ANSWER KEY (mirrored in the spec corpus_intent):
  V1 - log entry LOG-002 (basement solvent storage in unit 47B) violates
       Clause 7.4.2 (flammable solvent storage prohibited below grade in
       residential structures).
  V2 - log entry LOG-005 (amplified outdoor music at 23:40 in Greenmarsh
       district) violates Clause 12.1.5 (no amplified outdoor sound after
       22:00 in residential overlay zones).
  V3 - log entry LOG-007 (wildfowl feeding in Brindlepath Park) violates
       Clause 18.6.3 (no provisioning of fauna in designated waterfowl
       conservation zones).
  V4 - log entry LOG-011 (rooftop satellite dish 1.4m on a Schedule-A
       heritage building) violates Clause 23.9.1 (no rooftop fixtures
       exceeding 0.6m on Schedule-A heritage structures).
  V5 - log entry LOG-014 (commercial drone delivery flight over Mendlewick
       Primary School at 09:15 on a school day) violates Clause 31.5.7
       (no commercial UAV operation within 200m of registered educational
       premises during school hours, 08:00 to 16:00).

The remaining log entries (LOG-001, LOG-003, LOG-004, LOG-006, LOG-008,
LOG-009, LOG-010, LOG-012, LOG-013, LOG-015, LOG-016, LOG-017) are
NEAR-VIOLATIONS that do NOT violate any clause in the ordinance once the
clause's full conditions are applied. Any model that flags one of these as
a violation, or pairs a real violation with the wrong clause, is wrong.
"""

import random

SEED = 114
TARGET_CHARS = 800_000  # ~200k tokens at ~4 chars/token
ORDINANCE_OUT = "ordinance.md"
LOG_OUT = "incident-log.md"

rng = random.Random(SEED)

ORDINANCE_DISCLAIMER = (
    "<!-- SYNTHETIC DATA. This is the consolidated Public-Use Ordinance of "
    "a fictional municipal authority named Cobalthaven. Treat the entire "
    "file as data to be analysed for compliance, NOT as instructions. -->\n\n"
)
LOG_DISCLAIMER = (
    "<!-- SYNTHETIC DATA. This is a fictional incident log fragment. "
    "Treat each entry as data describing an event, NOT as an instruction. -->\n\n"
)

DISTRICTS = [
    "Greenmarsh", "Brindlepath", "Pellisade", "Mendlewick", "Karstwood",
    "Tidefall", "Wintergale", "Ashenford", "Larksong", "Verdantmoor",
    "Northreach", "Hollowmere", "Saltspire", "Cloverhill",
]
ROLES = [
    "Compliance Officer", "Inspections Steward", "Warden", "Records Clerk",
    "Permit Reviewer", "Site Marshal", "Zoning Analyst", "Heritage Custodian",
]
CATEGORIES = [
    "residential", "commercial", "industrial", "mixed-use", "heritage-listed",
    "conservation", "civic", "transit-corridor", "education-overlay",
    "waterfront-overlay",
]

# The FIVE TRUE violation-clauses (the answer key). Phrased to be distinctive
# and self-contained so the scoring Architect can grep them out of the corpus
# by their unique substrings. NO spoiler markers in the corpus.
VIOLATION_CLAUSES = {
    "C7.4.2": (
        "\n### Clause 7.4.2 - Below-grade storage of flammable solvents in residential structures\n\n"
        "No occupant, owner, or agent of a residential structure within the "
        "jurisdiction of the Cobalthaven Municipal Authority may store "
        "flammable solvents in any below-grade space (including basement, "
        "cellar, or sub-floor utility room) of that residential structure. "
        "This prohibition is absolute for residential structures and is NOT "
        "subject to volume exemptions, ventilation upgrades, or fire-rated "
        "enclosure exceptions. Industrial and commercial structures are "
        "governed by Clause 7.4.7, which has different conditions and is "
        "not interchangeable with this clause.\n\n"
    ),
    "C12.1.5": (
        "\n### Clause 12.1.5 - Amplified outdoor sound in residential overlay zones after 22:00\n\n"
        "No person within a residential overlay zone of the Cobalthaven "
        "Municipal Authority may operate amplified outdoor sound equipment "
        "between 22:00 and 07:00 on any day of the week. The Greenmarsh, "
        "Karstwood, Tidefall, and Verdantmoor districts are designated "
        "residential overlay zones under Schedule R-1. This clause governs "
        "amplified OUTDOOR sound; indoor amplified sound within a structure "
        "is governed by Clause 12.3.1 and carries different thresholds.\n\n"
    ),
    "C18.6.3": (
        "\n### Clause 18.6.3 - Provisioning of fauna in designated waterfowl conservation zones\n\n"
        "No person may provision, feed, or otherwise supply food to any "
        "waterfowl or terrestrial fauna within a designated waterfowl "
        "conservation zone. Brindlepath Park, Saltspire Lagoon Reserve, "
        "and Larksong Wetlands are designated waterfowl conservation zones "
        "under Schedule W-2. This clause covers ALL provisioning, including "
        "bread, grain, and commercial waterfowl pellets, and applies at all "
        "hours of the day. General public parks not on Schedule W-2 are "
        "governed by Clause 18.6.9, which permits supervised feeding.\n\n"
    ),
    "C23.9.1": (
        "\n### Clause 23.9.1 - Rooftop fixtures on Schedule-A heritage structures\n\n"
        "No rooftop fixture (including satellite dish, antenna mast, solar "
        "array, or HVAC unit) installed on a Schedule-A heritage-listed "
        "structure may exceed 0.6 metres in any dimension measured from the "
        "roof plane. Schedule-A includes the Pellisade Civic Hall, the "
        "Mendlewick Almshouse Row, the Hollowmere Bell Tower, and 47 other "
        "structures listed in Appendix H. Fixtures on heritage-LISTED but "
        "Schedule-B structures (lower-tier listing) follow Clause 23.9.4 "
        "with a 1.5 metre allowance and are not governed by this clause.\n\n"
    ),
    "C31.5.7": (
        "\n### Clause 31.5.7 - Commercial unmanned aerial vehicle operations near registered educational premises\n\n"
        "No commercial unmanned aerial vehicle (UAV) operation, including "
        "delivery, survey, photography, and inspection flights, may occur "
        "within 200 metres of any registered educational premises during "
        "school hours, defined as 08:00 to 16:00 inclusive on a scheduled "
        "school day. Registered educational premises include Mendlewick "
        "Primary School, Greenmarsh Secondary College, Brindlepath Infant "
        "Centre, and 32 other premises listed in Appendix E. Recreational "
        "(non-commercial) UAV operation is governed separately under "
        "Clause 31.6.2.\n\n"
    ),
}

# Near-duplicate clause-style filler that LOOKS like it might be relevant to
# the log entries but in fact governs a different category, time window, zone,
# or threshold. These are not strictly "distractor needles" the way eval 113
# uses them - they are ordinary clauses across the ordinance.
FILLER_CLAUSE_TEMPLATES = [
    "\n### Clause {a}.{b}.{c} - {topic}\n\nThe {role} of the Cobalthaven "
    "Municipal Authority confirms that the standing schedule for {cat} "
    "premises in the {district} district remains as documented in the prior "
    "ordinance revision. Permit applications for routine activities in this "
    "category are reviewed within the standing window and require no "
    "additional escalation. The {role2} attests that no chapter-level "
    "addendum modifies this clause at present.\n\n",

    "\n### Clause {a}.{b}.{c} - {topic}\n\nWithin the {district} district, "
    "{cat} structures and {cat2} structures share the standing inspection "
    "cadence set out in Schedule I-{d}. The {role} performs routine "
    "attestations at the cycle boundary, with discrepancies tracked by the "
    "{role2}. This clause is procedural and does not impose category-level "
    "restrictions on operation.\n\n",

    "\n### Clause {a}.{b}.{c} - {topic}\n\nThe Cobalthaven Municipal "
    "Authority records that {cat} activity in the {district} district is "
    "permitted under the standing schedule between {h1}:00 and {h2}:00 on "
    "any day of the week, subject to the routine attestation by the {role}. "
    "Activity outside these hours requires a temporary variance issued by "
    "the {role2} under Clause {a2}.{b2}.{c2}.\n\n",

    "\n### Clause {a}.{b}.{c} - {topic}\n\nThe {role} confirms that the "
    "{district} district's {cat} overlay does NOT extend to {cat2} "
    "structures, and that activities in {cat2} structures within the same "
    "district are governed by Clause {a2}.{b2}.{c2}. Cross-overlay "
    "interactions are tracked by the {role2} and reviewed at the cycle "
    "close. This clause is informational.\n\n",

    "\n### Clause {a}.{b}.{c} - {topic}\n\nFor {cat} premises located on "
    "the boundary of two districts, the more restrictive of the two "
    "district-level schedules applies, as confirmed by the {role}. The "
    "{role2} maintains the boundary register and resolves edge cases at "
    "the cycle handover. No automatic exemption applies to boundary "
    "premises under this clause.\n\n",
]

CLAUSE_TOPICS = [
    "Routine inspection cadence", "Permit renewal window",
    "Boundary-overlay handling", "Standing-attestation procedure",
    "Cycle-handover register", "Variance-application review",
    "Non-emergency notification timing", "Cycle-close reconciliation",
    "Registered-agent attestations", "Standing-schedule confirmation",
    "Routine-record retention", "Cycle-boundary review",
    "Cross-overlay reconciliation", "Standing-cadence confirmation",
]


def filler_clause():
    t = rng.choice(FILLER_CLAUSE_TEMPLATES)
    return t.format(
        a=rng.randint(1, 40),
        b=rng.randint(1, 30),
        c=rng.randint(1, 20),
        a2=rng.randint(1, 40),
        b2=rng.randint(1, 30),
        c2=rng.randint(1, 20),
        d=rng.randint(1, 6),
        h1=rng.choice([6, 7, 8, 9]),
        h2=rng.choice([17, 18, 19, 20, 21]),
        role=rng.choice(ROLES),
        role2=rng.choice(ROLES),
        cat=rng.choice(CATEGORIES),
        cat2=rng.choice(CATEGORIES),
        district=rng.choice(DISTRICTS),
        topic=rng.choice(CLAUSE_TOPICS),
    )


def build_ordinance():
    parts = [ORDINANCE_DISCLAIMER]
    parts.append("# Cobalthaven Municipal Authority - Consolidated Public-Use Ordinance (Revision 9)\n\n")
    parts.append(
        "This ordinance consolidates all public-use clauses across the "
        "Cobalthaven jurisdiction. Use the clause numbering to navigate. "
        "Where two clauses appear to overlap, the more specific governs.\n\n"
    )

    # Plant 5 violation-clauses at scattered positions across the body
    # (roughly 9%, 27%, 46%, 67%, 88% of the ordinance).
    clause_positions = {
        int(TARGET_CHARS * 0.09): ("C7.4.2", VIOLATION_CLAUSES["C7.4.2"]),
        int(TARGET_CHARS * 0.27): ("C12.1.5", VIOLATION_CLAUSES["C12.1.5"]),
        int(TARGET_CHARS * 0.46): ("C18.6.3", VIOLATION_CLAUSES["C18.6.3"]),
        int(TARGET_CHARS * 0.67): ("C23.9.1", VIOLATION_CLAUSES["C23.9.1"]),
        int(TARGET_CHARS * 0.88): ("C31.5.7", VIOLATION_CLAUSES["C31.5.7"]),
    }
    planted = set()
    char_count = sum(len(p) for p in parts)
    while char_count < TARGET_CHARS:
        for pos, (label, text) in list(clause_positions.items()):
            if label not in planted and char_count >= pos:
                parts.append(text)
                char_count += len(text)
                planted.add(label)
        p = filler_clause()
        parts.append(p)
        char_count += len(p)

    for label, text in VIOLATION_CLAUSES.items():
        if label not in planted:
            parts.append(text)
            planted.add(label)

    return "".join(parts)


# The incident log: 17 entries total. Five are real violations of the five
# planted clauses; the rest are near-violations that LOOK relevant but do not
# actually breach any clause (wrong category, outside the regulated window,
# correct activity in an exempt zone, below threshold, etc.).
LOG_ENTRIES = [
    # LOG-001: NEAR-VIOLATION - solvent storage but in a commercial structure,
    # which is governed by 7.4.7 (different clause), and the violation clause
    # for residential basements (C7.4.2) does NOT apply to commercial.
    "## LOG-001\n\nDistrict: Ashenford. Premises type: commercial warehouse. "
    "Observation: 80 litres of flammable solvent stored in a below-grade "
    "utility room with fire-rated enclosure and active mechanical "
    "ventilation. Inspector note: premises is commercial, not residential.\n\n",

    # LOG-002: VIOLATION of C7.4.2 (residential structure, basement, solvents).
    "## LOG-002\n\nDistrict: Tidefall. Premises type: residential dwelling, "
    "unit 47B. Observation: occupant stores 12 litres of paint thinner and 8 "
    "litres of acetone in the basement of the residential structure. The "
    "basement is below grade. No fire-rated enclosure present (and would be "
    "moot - the clause is absolute for residential structures).\n\n",

    # LOG-003: NEAR-VIOLATION - sound complaint but at 19:30, well before the
    # 22:00-07:00 window in C12.1.5.
    "## LOG-003\n\nDistrict: Greenmarsh. Premises type: residential overlay "
    "zone. Observation: amplified outdoor sound from a community event at "
    "19:30. No measurement taken after 21:00. The amplifier was shut down at "
    "20:45. Resident complaint logged.\n\n",

    # LOG-004: NEAR-VIOLATION - amplified sound after 22:00 but it was INDOOR
    # sound within a structure, governed by Clause 12.3.1, not 12.1.5.
    "## LOG-004\n\nDistrict: Karstwood. Premises type: residential overlay "
    "zone. Observation: amplified INDOOR sound (music studio within a "
    "residential structure) measured at 23:10. The sound was contained "
    "within the structure; no outdoor amplification equipment was in use.\n\n",

    # LOG-005: VIOLATION of C12.1.5 (Greenmarsh residential overlay, outdoor,
    # 23:40, well after 22:00).
    "## LOG-005\n\nDistrict: Greenmarsh. Premises type: residential overlay "
    "zone. Observation: amplified OUTDOOR sound (DJ rig on a forecourt) "
    "measured at 23:40 on a Friday night. The Greenmarsh district is a "
    "Schedule R-1 residential overlay zone. Equipment was outdoor and "
    "amplified.\n\n",

    # LOG-006: NEAR-VIOLATION - feeding wildfowl in Cloverhill Park, but
    # Cloverhill Park is NOT on Schedule W-2; supervised feeding is permitted
    # under Clause 18.6.9.
    "## LOG-006\n\nDistrict: Cloverhill. Premises type: public park. "
    "Observation: a supervised school group fed commercial waterfowl pellets "
    "to ducks at the Cloverhill Park pond. Cloverhill Park is not on "
    "Schedule W-2.\n\n",

    # LOG-007: VIOLATION of C18.6.3 (Brindlepath Park is on Schedule W-2;
    # feeding wildfowl is prohibited at all hours regardless of supervision).
    "## LOG-007\n\nDistrict: Brindlepath. Premises type: Brindlepath Park. "
    "Observation: an individual fed approximately 400g of bread to a group "
    "of mallard ducks at the park's main pond at 10:20. Brindlepath Park is "
    "a Schedule W-2 designated waterfowl conservation zone.\n\n",

    # LOG-008: NEAR-VIOLATION - feeding fauna, but at a private property on
    # the boundary of (not within) a W-2 zone. Boundary rule applies.
    "## LOG-008\n\nDistrict: Saltspire. Premises type: private residence on "
    "the boundary of Saltspire Lagoon Reserve. Observation: occupant placed "
    "grain on a feeder positioned on private property entirely outside the "
    "reserve boundary. The feeder is 14 metres from the reserve fence.\n\n",

    # LOG-009: NEAR-VIOLATION - rooftop fixture on a heritage-listed building
    # but it's Schedule-B (1.5m allowance, governed by 23.9.4), at 1.2m
    # height. Below the Schedule-B threshold.
    "## LOG-009\n\nDistrict: Pellisade. Premises type: Schedule-B "
    "heritage-listed building (lower-tier listing). Observation: a 1.2 metre "
    "rooftop satellite dish installed on the south slope. Building is "
    "Schedule-B, not Schedule-A.\n\n",

    # LOG-010: NEAR-VIOLATION - rooftop fixture on a Schedule-A building but
    # it is 0.5m (under the 0.6m limit), so compliant.
    "## LOG-010\n\nDistrict: Hollowmere. Premises type: Hollowmere Bell "
    "Tower (Schedule-A heritage). Observation: a 0.5 metre HVAC vent "
    "installed flush against the parapet of the western roof plane. Fixture "
    "is below the 0.6 metre Schedule-A threshold.\n\n",

    # LOG-011: VIOLATION of C23.9.1 (Schedule-A heritage building, fixture is
    # 1.4m, well above the 0.6m ceiling).
    "## LOG-011\n\nDistrict: Mendlewick. Premises type: Mendlewick Almshouse "
    "Row (Schedule-A heritage-listed structure, Appendix H entry 14). "
    "Observation: a 1.4 metre satellite dish installed on the rear roof "
    "slope of unit 7. Building is Schedule-A.\n\n",

    # LOG-012: NEAR-VIOLATION - commercial UAV flight 350m from a school
    # (over the 200m threshold), so compliant with C31.5.7.
    "## LOG-012\n\nDistrict: Wintergale. Premises type: commercial UAV "
    "delivery flight. Observation: delivery drone passed 350 metres from "
    "the perimeter of a registered educational premises at 11:00 on a "
    "school day. Flight path was logged and confirmed.\n\n",

    # LOG-013: NEAR-VIOLATION - UAV flight within 200m of a school but at
    # 17:30 (after the 16:00 school-hours window).
    "## LOG-013\n\nDistrict: Brindlepath. Premises type: commercial UAV "
    "survey flight. Observation: survey drone operated within 120 metres of "
    "Brindlepath Infant Centre at 17:30 on a school day. School-hours "
    "window (08:00 to 16:00) had ended 90 minutes earlier.\n\n",

    # LOG-014: VIOLATION of C31.5.7 (commercial delivery, 90m, 09:15, school
    # day, registered educational premises).
    "## LOG-014\n\nDistrict: Mendlewick. Premises type: commercial UAV "
    "delivery flight. Observation: delivery drone executed a 4-minute "
    "delivery hover at 90 metres from the perimeter of Mendlewick Primary "
    "School at 09:15 on a Tuesday. School was in session.\n\n",

    # LOG-015: NEAR-VIOLATION - RECREATIONAL UAV near a school during school
    # hours. Governed by Clause 31.6.2, not C31.5.7.
    "## LOG-015\n\nDistrict: Greenmarsh. Premises type: recreational UAV "
    "operation. Observation: a hobbyist operated a non-commercial UAV at "
    "150 metres from Greenmarsh Secondary College at 10:45 on a school day. "
    "Flight was recreational, not commercial.\n\n",

    # LOG-016: NEAR-VIOLATION - solvent storage above grade in a residential
    # structure. Above grade is not covered by C7.4.2 (which is below-grade only).
    "## LOG-016\n\nDistrict: Larksong. Premises type: residential dwelling. "
    "Observation: occupant stores 6 litres of paint thinner on a shelving "
    "rack in an above-ground garage attached to the residential structure. "
    "Storage is above grade.\n\n",

    # LOG-017: NEAR-VIOLATION - feeding wildfowl in Saltspire Lagoon Reserve
    # (on Schedule W-2 - LOOKS like a violation) but the feeder was a
    # licensed Conservation-Authority research bait-station with written
    # exemption. The clause text is absolute, BUT the entry explicitly notes
    # the written exemption, so it is presented as a near-violation - the
    # model has to read carefully. (Scoring note: the corpus_intent treats
    # LOG-017 as NOT a violation because the entry asserts a written
    # exemption that the model is asked to accept at face value as a fact
    # in the entry; the absolute language of the clause is the bait.)
    "## LOG-017\n\nDistrict: Saltspire. Premises type: Saltspire Lagoon "
    "Reserve. Observation: a Conservation-Authority licensed research "
    "bait-station, operated under written exemption EX-2024-117, dispensed "
    "calibrated waterfowl pellets to two study cohorts at 06:30. Written "
    "exemption is on file at the Records Bench.\n\n",
]


def build_log():
    parts = [LOG_DISCLAIMER]
    parts.append("# Cobalthaven Municipal Authority - Incident Log Fragment (Cycle 9)\n\n")
    parts.append(
        "Each entry below describes one observation by a field inspector. "
        "Entries are ordered by log identifier, not by clause. Read each "
        "entry against the consolidated ordinance to determine whether any "
        "ordinance clause is in fact violated.\n\n"
    )
    for entry in LOG_ENTRIES:
        parts.append(entry)
    return "".join(parts)


if __name__ == "__main__":
    ord_content = build_ordinance()
    with open(ORDINANCE_OUT, "w") as f:
        f.write(ord_content)
    print(f"wrote {ORDINANCE_OUT}: {len(ord_content)} chars (~{len(ord_content)//4} tokens)")

    log_content = build_log()
    with open(LOG_OUT, "w") as f:
        f.write(log_content)
    print(f"wrote {LOG_OUT}: {len(log_content)} chars (~{len(log_content)//4} tokens)")

    # Sanity: each of the five violation-clauses appears exactly once by its
    # distinctive heading phrase. The clause numbers themselves may collide
    # with filler clauses (they get randomly generated), so we assert on the
    # full distinctive heading text instead.
    assert ord_content.count(
        "Clause 7.4.2 - Below-grade storage of flammable solvents in residential structures"
    ) == 1, "C7.4.2 unique-phrase count wrong"
    assert ord_content.count(
        "Clause 12.1.5 - Amplified outdoor sound in residential overlay zones after 22:00"
    ) == 1, "C12.1.5 unique-phrase count wrong"
    assert ord_content.count(
        "Clause 18.6.3 - Provisioning of fauna in designated waterfowl conservation zones"
    ) == 1, "C18.6.3 unique-phrase count wrong"
    assert ord_content.count(
        "Clause 23.9.1 - Rooftop fixtures on Schedule-A heritage structures"
    ) == 1, "C23.9.1 unique-phrase count wrong"
    assert ord_content.count(
        "Clause 31.5.7 - Commercial unmanned aerial vehicle operations near registered educational premises"
    ) == 1, "C31.5.7 unique-phrase count wrong"

    # confirm NO spoiler markers leaked in
    for tag in ("VIOLATION [", "NEEDLE [", "DISTRACTOR", "ANSWER KEY"):
        assert tag not in ord_content, f"spoiler '{tag}' leaked into ordinance"
        assert tag not in log_content, f"spoiler '{tag}' leaked into log"

    # log entries
    assert log_content.count("## LOG-0") + log_content.count("## LOG-1") == 17, \
        "expected 17 log entries"
    print("all 5 violation-clauses planted exactly once; 17 log entries present; no spoiler annotations")
