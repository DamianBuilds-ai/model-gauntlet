# Internal Slack Thread - Engineering

Captured from the #infra channel. Context: ops asked engineering whether they could
help run a self-hosted support tool.

---

**ops_lead:** If we went with Quillstack (self-hosted), could infra own running it?
Upgrades, scaling before peak, backups, that kind of thing?

**eng_lead:** Honest answer: no, not reliably. We are already underwater on our own
roadmap. We could help you stand it up, but we cannot commit to owning patching and
peak-scaling on an ongoing basis. That has to be someone's actual job and right now it
is nobody's.

**eng_lead:** If you pick something self-hosted, budget for it to fall on you in ops,
or budget for a paid support contract, because it will not get sustained attention from
us.

**ops_lead:** That is what I was afraid of. Noted.

---

[Confirms Cardinal has NO capacity to operate a self-hosted platform. The operating
burden of Quillstack would land on the small ops team or require paid support - exactly
the cost the analysis in doc 07 captures.]
