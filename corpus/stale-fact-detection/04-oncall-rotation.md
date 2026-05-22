# Cardinal Logistics - On-Call Rotation Runbook

This runbook covers how the on-call rotation works day to day: who is on, how
handoff happens, what the primary and secondary are responsible for, and the
mechanics of acknowledgement and escalation. It is the operational companion to the
incident runbook (which covers running an incident once one is declared).

## Rotation structure

Each rotation is one week long, running Monday 10:00 local to the following Monday
10:00 local. There is always a primary and a secondary on-call. The primary takes
first pages; the secondary is the escalation target and the backup if the primary
is unreachable. A third "manager on-call" exists for Sev-1 coordination but does
not take pages directly.

## Joining the rotation

New engineers shadow one full rotation before being added as a primary. During the
shadow week you receive pages in parallel (silenced) so you can practise triage
without owning the response. Platform adds you to the schedule once your lead signs
off.

## Daily expectations

While on primary, you keep your laptop and a charged phone within reach during
working hours and respond to pages at any hour. Routine work continues, but pages
take precedence. If you will be unreachable for a stretch (commute, appointment),
hand the pager to the secondary explicitly in the paging tool and tell them in the
channel.

## Acknowledgement and handoff

When a page fires, the paging tool notifies the primary first. The primary should
acknowledge as soon as they see it, even before they have diagnosed anything -
acknowledgement simply tells the system a human has taken ownership and stops the
escalation timer. If the primary does not acknowledge in time, the page rolls to
the secondary automatically. The primary has 15 minutes to acknowledge before the
page rolls to the secondary, so if you are stepping away even briefly during your
shift, hand off explicitly rather than risk a silent escalation. Once the secondary
picks up an escalated page, they own it until the primary explicitly takes it back
in the tool. Handoff at the end of a rotation happens at the Monday 10:00 boundary:
the outgoing primary briefs the incoming primary on any open incidents, watch
items, and flapping alerts before standing down.

## Secondary responsibilities

The secondary keeps the same reachability standard as the primary during the
rotation, because an escalation can arrive at any time. The secondary also reviews
the primary's open items at the daily sync so there is shared context if an
escalation lands.

## Escalation beyond the secondary

If neither primary nor secondary acknowledges, the page escalates to the manager
on-call, who will pull in whoever is needed. This is rare and is itself a signal
that the rotation is understaffed that week - raise it in the retro.

## Tooling

All of the above is enforced by the paging tool's escalation policy. The policy
mirrors the values in the config reference; if you think the tool's behaviour and
this runbook disagree, the config reference and the changelog are authoritative -
flag the discrepancy so the runbook gets corrected.
