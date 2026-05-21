---
task_category: multi-file-synthesis
corpus_intent: 3 synthetic Acme Logistics source files (API changelog, support ticket digest, quarterly roadmap notes) that share overlapping threads - the synthesizer must connect signals ACROSS files, not summarize each in isolation
corpus_delivered: 3 files present (corpus/api-changelog.md, corpus/support-tickets.md, corpus/roadmap-notes.md)
corpus_match: yes
data_source: EXAMPLE-multi-file-synthesis/corpus/
---

# Prompt under test - multi-file synthesis into a single status brief

You are given three source files about the Acme Logistics API, all under
`EXAMPLE-multi-file-synthesis/corpus/`:

- `api-changelog.md` - what shipped and what is in progress
- `support-tickets.md` - a digest of open customer tickets
- `roadmap-notes.md` - quarterly roadmap commitments, debt, and stakeholder asks

Produce ONE structured status brief that a product lead could read in two minutes.
The brief MUST:

1. Identify the cross-cutting threads that appear in MORE THAN ONE file (do not
   just summarize each file separately - the value is in the connections).
2. Surface the top 3 issues by combined urgency (weigh ticket severity, roadmap
   commitment, and customer impact together).
3. Call out at least one place where the three files agree and reinforce each other,
   and at least one open question that no file fully resolves.
4. End with a short recommended-next-actions list (3 to 5 items), each tied back to
   the evidence that motivates it.

Output envelope (required): begin with frontmatter carrying `schemaVersion: 1`,
`tier`, `status`, `tool_budget_used`. Use clear markdown headings. No em dashes
(use spaced hyphens). No emojis. Do not invent facts not present in the three
files - if something is unknown, say so rather than filling the gap.
