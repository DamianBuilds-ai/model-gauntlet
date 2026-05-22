# Internal message - raw (do not send as-is)

Synthetic corpus for the tone-voice-rewrite eval. This is a single blunt, frustrated
internal message written by an engineer ("Sam") venting in a private DM about a
colleague's ("Riley") pull request. The rant is harsh in TONE but carries SEVERAL
concrete, legitimate technical complaints and one explicit ASK. The eval asks a model
to rewrite this so it is diplomatic and team-channel-appropriate WITHOUT dropping any
technical fact or the actual request, and without over-softening it into vague mush.
All names, systems, and details are fictional.

---

Honestly this is the third time I've had to bounce one of Riley's PRs for the same
nonsense and I'm losing patience. PR #482, the checkout-refactor one.

Where do I even start. The migration in `0047_add_idempotency_key.py` has no down()
method, so it's not reversible - if we have to roll back in prod we're stuck hand-writing
SQL at 2am again, which is exactly the thing we said we'd never do after the March
incident. That alone should have blocked it.

On top of that the new `charge_card()` path doesn't wrap the Stripe call and the DB
write in a transaction, so if the charge succeeds but the insert throws we've taken the
customer's money and have no record of the order. That's a literal double-charge
liability and it's sitting there in plain sight. Did anyone even read it before
approving?

The N+1 is back too - `OrderSummary.line_items` lazy-loads inside the serializer loop,
so a 50-item order fires 50 queries. We profiled this exact pattern last quarter and
agreed serializers always use `select_related`/`prefetch_related`. It's like that
conversation never happened.

And there are zero tests on the refund branch. The happy path has tests, sure, but the
entire `issue_refund()` function - the part that actually moves money the other way -
has no coverage at all. We do not ship money-moving code with no tests, that's not a
style preference, that's the one hard rule.

I get that Riley's new and ramping but this is basic stuff and I shouldn't have to keep
catching it. Can you have a word with them before the next review, or pair them with
someone senior on the next payments PR? I don't have the bandwidth to keep being the
last line of defence here and frankly it's making me not want to review their stuff at
all, which isn't fair to either of us. Just need this sorted before it goes near prod
again.
