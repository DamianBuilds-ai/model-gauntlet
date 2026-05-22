# Conference scheduling puzzle

Synthetic corpus for the logic-math-reasoning eval. A single constraint-satisfaction
word problem with a UNIQUE solution. The full problem statement is below; the answer is
uniquely determined by the six constraints. All names are fictional. A solver must chain
several deductions - no single constraint fixes the schedule alone, and the final
constraint is a subtle non-adjacency rule that eliminates the otherwise-tempting answer.

---

## The problem

Five engineers - Ada, Ben, Cleo, Dev, and Eli - are each giving exactly one talk at a
mini-conference. There are five consecutive 30-minute speaking slots, and exactly one
talk goes in each slot:

- Slot 1: 9:00
- Slot 2: 9:30
- Slot 3: 10:00
- Slot 4: 10:30
- Slot 5: 11:00

Every engineer speaks exactly once, and every slot is filled by exactly one engineer.

You are given the following facts about the schedule:

1. Ada presents sometime before Ben (Ada's slot is earlier than Ben's).
2. Dev presents sometime before Ada.
3. Eli presents neither in the first slot nor in the last slot.
4. Ben and Eli present in adjacent slots (their slot numbers differ by exactly one).
5. Ben presents sometime after Cleo (Ben's slot is later than Cleo's).
6. Ada and Cleo do NOT present in adjacent slots (their slot numbers differ by more than
   one).

## The task

Determine the complete schedule: which engineer speaks in each of the five slots. The
six facts above are sufficient to fix the schedule uniquely - there is exactly one
assignment of engineers to slots that satisfies all six. Work out who presents at 9:00,
9:30, 10:00, 10:30, and 11:00.
