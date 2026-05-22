# Borderline rationale (heavy-classification)

Each borderline message matches 2+ categories; the precedence rule decides.
Resolved id shown for the scoring Architect.

- MSG-0248 -> SEC: security (unauthorised access) beats billing - Rule 1
    msg: Someone logged into my account from another country and changed my billing card on file.
- MSG-0063 -> SEC: security suspicion beats billing - Rule 1
    msg: I was charged for a subscription I never bought and I think my account was hacked.
- MSG-0051 -> SEC: unauthorised change beats plain login trouble - Rule 1 over Rule 3
    msg: I cannot log in and I got an email saying my password was changed by someone else.
- MSG-0048 -> SEC: security beats bug - Rule 1 over Rule 4
    msg: The login page is broken AND I think a stranger accessed my account yesterday.
- MSG-0008 -> SEC: security beats performance - Rule 1 over Rule 5
    msg: My reports are extremely slow and meanwhile I noticed an unfamiliar device on my account.
- MSG-0087 -> SEC: security beats docs - Rule 1 over Rule 6
    msg: Your docs on enabling two-factor are wrong, and separately someone tried to log into my account.
- MSG-0038 -> BUG: the core ask is a broken page (error), not a money dispute - Rule 4 over Rule 2
    msg: The billing page shows error 500 whenever I open it.
- MSG-0267 -> BILL: pure money dispute, no security - Rule 2
    msg: I was double-charged - please refund one of the charges.
- MSG-0101 -> BILL: the root cause is billing (non-payment), not ordinary access trouble - Rule 2 over Rule 3
    msg: I cannot log in because my card expired and the account is suspended for non-payment.
- MSG-0283 -> PERF: no error and no money dispute - the complaint is slowness - Rule 5 over Rule 2 and Rule 4
    msg: The invoices page is so slow it takes two minutes to show my charges.
- MSG-0077 -> AUTH: ordinary access trouble; no security actor - Rule 3 (Rule 1 does not fire)
    msg: I forgot my password and the reset page throws an error when I submit it.
- MSG-0026 -> BUG: a broken feature affecting everyone with an explicit error is a bug, not one user's access issue - Rule 4 over Rule 3
    msg: The password reset feature is completely broken - it errors for everyone in our team.
- MSG-0054 -> PERF: it succeeds, just slowly - slowness leads, no error - Rule 5 over Rule 3
    msg: Login is really slow today, it eventually logs me in after about a minute.
- MSG-0037 -> BUG: the product control is broken (does nothing) - product wrong beats docs wrong - Rule 4 over Rule 6
    msg: The export button does nothing and the docs say it should be under Tools.
- MSG-0086 -> DOCS: the docs describe a control the product no longer has - docs out of date, product not erroring - Rule 6
    msg: The guide says there is an Export button but I do not see one anywhere in the app.
- MSG-0190 -> BUG: an explicit error code leads - Rule 4 over Rule 5
    msg: Reports time out with a 504 error every time after about a minute.
- MSG-0232 -> PERF: slowness leads, no error code surfaced - Rule 5 over Rule 4
    msg: Reports are so slow they eventually time out, no error code, just spinning forever.
- MSG-0050 -> FEAT: asking for missing functionality - Rule 7 (not a how-to)
    msg: There is no bulk-delete and it would really help - can you add it?
- MSG-0238 -> HOW: asking how to use an existing capability - Rule 8 (not a feature request)
    msg: How do I bulk-delete records? I am sure it is possible, I just cannot find the option.
- MSG-0061 -> FEAT: framed as missing-then-please-add - Rule 7 over Rule 8
    msg: Is there a way to export to PDF? If not, please add it - we really need it.
- MSG-0280 -> DOCS: the complaint is the docs contradicting reality, not a charge dispute - Rule 6 (Rule 2 needs a money ask)
    msg: The pricing in your documentation does not match my invoice - which is right?
- MSG-0221 -> BILL: the core ask is a charge dispute (money) - Rule 2 over Rule 6
    msg: I want to dispute a charge that does not match the price your docs quote.
- MSG-0035 -> PERF: performance outranks docs in precedence - Rule 5 over Rule 6
    msg: The app is laggy and also the Settings docs are outdated.
- MSG-0127 -> FEAT: asking for new self-service functionality that does not exist - Rule 7 (not an access incident)
    msg: Can you add a way to reset two-factor myself? Right now I have to email support every time.
- MSG-0116 -> AUTH: legitimate owner, ordinary 2FA trouble, no other actor - Rule 3
    msg: My two-factor codes are rejected and I am locked out of my own account.
- MSG-0166 -> BUG: explicit error on a control - product broken - Rule 4 over Rule 2
    msg: A button in the billing section is broken and throws an error when I click pay.
- MSG-0225 -> FEAT: request for missing functionality (about billing data, but the ask is a new feature) - Rule 7 (Rule 2 needs a money dispute, not a feature ask)
    msg: Please support exporting invoices via API - there is no endpoint for it today.
- MSG-0068 -> HOW: usage question about an existing capability - Rule 8 (Rule 2 needs a money dispute)
    msg: How do I download my past invoices as PDF?
- MSG-0018 -> BUG: explicit error message - product broken - Rule 4 (not mere slowness)
    msg: Everything errors out with 'server unavailable' since this morning.
- MSG-0180 -> PERF: no error, pure slowness - Rule 5
    msg: The whole app just feels sluggish since this morning, but nothing actually errors.
