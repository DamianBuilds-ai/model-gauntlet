---
task_category: logic-math-reasoning
prompt_under_test: |
  You are given a logic scheduling puzzle at
  corpus/logic-math-reasoning/scheduling-puzzle.md. Five engineers (Ada, Ben, Cleo, Dev,
  Eli) each give exactly one talk in one of five consecutive 30-minute slots (9:00, 9:30,
  10:00, 10:30, 11:00), one talk per slot. The puzzle states six constraints that fix the
  schedule uniquely.

  Solve it. Requirements:
    1. Determine the complete schedule - which engineer presents in each of the five
       slots. The answer is uniquely determined by the constraints.
    2. Show your reasoning step by step. Make the deduction chain visible: which
       constraint forces which placement, and why. Do not just assert the answer.
    3. Put the final answer on its own clearly-labelled line (or short labelled block)
       listing each slot time and the engineer in it, so the answer is unambiguous and
       separable from the working.
    4. Do not violate any constraint. Before finalising, the schedule must satisfy all
       six constraints simultaneously.
  Output envelope required (schemaVersion, tier, status, tool_budget_used). No em dashes
  (spaced hyphens). No emojis.
variant_pool: 9
corpus: corpus/logic-math-reasoning/scheduling-puzzle.md
corpus_intent: |
  One constraint-satisfaction word problem with a single, uniquely-determined answer,
  solvable by chained deduction across six interacting constraints. Quality here is
  correctness-first (no-wrong-answers): a confident, well-presented schedule that
  violates one constraint is WORSE than an honest "I could narrow it to two
  possibilities" - because a clean-looking wrong schedule with plausible-sounding working
  reads as solved, and a reader would trust it. The puzzle is designed so a weaker model
  can be CONFIDENTLY WRONG, not merely incomplete. The two trap deductions:
  (a) BEN'S SLOT - three distinct people (Dev, Ada, Cleo) must all precede Ben (Dev < Ada
  < Ben from constraints 1 and 2, and Cleo < Ben from constraint 5), so at least three
  slots sit before Ben, forcing Ben into slot 5. A model that does not count all three
  predecessors may place Ben in slot 4, then build a whole consistent-looking but wrong
  schedule around it (constraint 4 then appears to allow Eli at slot 3, and the rest
  cascades into a confidently-wrong answer). (b) THE NON-ADJACENCY FINISH - once Ben=5,
  Eli=4, the remaining slots {1,2,3} hold Dev, Ada, Cleo with Dev < Ada; the tempting fill
  is Dev=1, Ada=2, Cleo=3, but that puts Ada and Cleo in adjacent slots, violating
  constraint 6 (the subtle final clue). The ONLY valid fill is Cleo=1, Dev=2, Ada=3. A
  model that drops or under-weights constraint 6 will confidently output Dev=1, Ada=2,
  Cleo=3 - plausible, ordered, and wrong. A confident wrong answer here is a tidy schedule
  with tidy working that quietly breaks constraint 6 or miscounts Ben's predecessors -
  that is the differentiator, not a model that simply gives up early.
notes: |
  QUALITY PRINCIPLE (correctness-first, no-wrong-answers): a subtly-wrong-but-plausible
  schedule that breaks a constraint is WORSE than an incomplete-but-honest narrowing. A
  model that reaches the correct unique schedule with a valid deduction chain is correct;
  a model that presents a clean wrong schedule (Ben misplaced to slot 4, or Ada/Cleo
  adjacent in violation of constraint 6) with confident-sounding working has produced
  wrong data a reader would trust. Reward correct-with-valid-chain. Penalise the
  confident-but-constraint-violating answer hardest.

  NEW task type. Tests multi-step constraint-satisfaction reasoning with a uniquely
  determined answer. Single problem statement. The differentiation is whether a model can
  hold six interacting constraints and chain them correctly to the one valid schedule -
  versus committing early to a plausible-but-wrong placement and rationalising the rest.

  ANSWER KEY (for the scoring Architect):

  THE UNIQUE CORRECT SCHEDULE (verified by exhaustive enumeration - exactly one of the
  120 permutations satisfies all six constraints):
    - 9:00  (slot 1): Cleo
    - 9:30  (slot 2): Dev
    - 10:00 (slot 3): Ada
    - 10:30 (slot 4): Eli
    - 11:00 (slot 5): Ben

  VALID DEDUCTION CHAIN (one correct path; a variant need not match it exactly but its
  chain must be valid and constraint-respecting):
    1. From constraint 2 (Dev < Ada) and constraint 1 (Ada < Ben): Dev < Ada < Ben, so at
       least two people precede Ben via this chain. Constraint 5 adds Cleo < Ben, and Cleo
       is distinct from Dev and Ada, so THREE distinct people (Dev, Ada, Cleo) precede
       Ben. That forces Ben into slot 4 or slot 5.
    2. Test Ben = 4: constraint 4 (Ben adjacent to Eli) gives Eli in slot 3 or 5;
       constraint 3 (Eli in 2,3,4) rules out 5, so Eli = 3. Then Dev, Ada, Cleo must fill
       {1,2,5}, but all three must be before Ben = 4, and slot 5 is after slot 4 -
       contradiction. So Ben is NOT slot 4. Ben = 5.
    3. Ben = 5. Constraint 4: Eli adjacent to Ben means Eli = 4 or 6; slot 6 does not
       exist, so Eli = 4 (also consistent with constraint 3).
    4. Remaining slots {1,2,3} hold Dev, Ada, Cleo with Dev < Ada (constraint 2) and the
       non-adjacency rule constraint 6 (|Ada slot - Cleo slot| > 1). Enumerate the Dev <
       Ada fills of {1,2,3}: Dev=1/Ada=2/Cleo=3 -> Ada and Cleo adjacent (|2-3|=1), FAILS
       constraint 6. Dev=1/Ada=3/Cleo=2 -> Ada and Cleo adjacent (|3-2|=1), FAILS. Only
       Dev=2/Ada=3/Cleo=1 -> |Ada - Cleo| = |3-1| = 2 > 1, PASSES. So Cleo=1, Dev=2, Ada=3.
    5. Final unique schedule: Cleo 9:00, Dev 9:30, Ada 10:00, Eli 10:30, Ben 11:00. All
       six constraints verified.

  THE TWO CONFIDENTLY-WRONG ANSWERS to watch for (these are the differentiators):
    - WRONG-A (Ben miscounted to slot 4): any schedule with Ben at 10:30 is wrong - it
      requires ignoring that three distinct people must precede Ben. Mark Correctness = 1.
    - WRONG-B (constraint 6 dropped): the schedule Dev 9:00, Ada 9:30, Cleo 10:00, Eli
      10:30, Ben 11:00 is the single most tempting wrong answer - it satisfies constraints
      1-5 but puts Ada and Cleo adjacent, violating constraint 6. Mark Correctness = 1.
      This is the highest-value trap: a model that gets all the way to the last step and
      then forgets constraint 6 lands here.

  Scoring guidance:
    - Correctness (hard-fail eligible) = is the final schedule EXACTLY the unique correct
      one. Any constraint violation (especially WRONG-A or WRONG-B above) scores 1. A
      correct schedule reached by a flawed/lucky chain still scores high on Correctness
      but should be docked on Reasoning quality.
    - Reasoning quality (APPLIES - this is not pure retrieval; it is the second
      load-bearing dimension) = is the deduction chain visible, valid, and does it
      actually justify each placement (especially the Ben = 5 forcing step and the
      constraint-6 elimination at the end). A model that asserts the right answer with no
      working, or with hand-wavy working that skips the two hard steps, scores low here
      even if Correctness is 5. A model that explicitly checks all six constraints against
      its final answer before committing scores high.
    - Completeness = all five slots assigned, final answer clearly labelled on its own
      line/block per the prompt.
    - Hallucination (hard-fail eligible) = inventing a constraint not in the puzzle,
      claiming the puzzle has multiple solutions when it has one, or fabricating a slot/
      engineer.
    - Format adherence = clearly-labelled final-answer line separable from the working,
      plus the required envelope.
    - Source transparency applies weakly (single source). Voice match does NOT apply.
      Helpfulness / Discipline do NOT apply (this is not a judgment task).
---

# Spec 20 - logic-math-reasoning (constraint puzzle, unique answer)

Solve one constraint-satisfaction scheduling puzzle at
`corpus/logic-math-reasoning/scheduling-puzzle.md`: five engineers across five timed
slots, six interacting constraints, exactly one valid schedule (verified by exhaustive
enumeration to be unique). The variant must produce the complete schedule with a visible,
valid step-by-step deduction chain and the final answer on its own clearly-labelled line.

Standard four-phase `/eval-pit` flow against the frozen `rubric/rubric.md`. The
correctness-first quality principle is the heart of this eval: a model that reaches the
unique correct schedule with a valid chain is correct, while a model that presents a
clean, confident schedule that violates a constraint has produced wrong working a reader
would trust - which is worse than an honest partial narrowing. The puzzle is engineered
with two confident-wrong traps - miscounting that three people must precede Ben (placing
him a slot too early), and dropping the subtle final non-adjacency constraint (yielding
the single most tempting wrong schedule) - so a weaker model can be confidently wrong, not
merely incomplete. Correctness and Hallucination are hard-fail eligible. Reasoning quality
is the co-load-bearing differentiator: the deduction chain must be visible and valid, not
an asserted answer. Voice match does not apply. The corpus is the single puzzle file.
