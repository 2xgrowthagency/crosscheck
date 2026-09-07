# Human intent from source issue 1

Source: https://github.com/2xgrowthagency/crosscheck/issues/1

> Audit it for improvements now that we’re on Astra; make it more robust depending on the type of task or decision being QA’d; improve completion evidence such as screenshots and videos; and rebrand it to Final Boss. It should run after the assignment and/or No Mistakes, use an ephemeral independent agent with fresh context, remain read-only, publish a plain-language PASS/FAIL report to the worker thread and GitHub, and remain an open-source project maintained under 2x.

Implementation boundary for this draft: deterministic runtime/schema/validator,
behavior cases, packaging, migration and integration documentation. Reusable skill
source must come from the existing Skill Workshop proposal and is not edited here.
The fresh independent QA and release decisions belong to the separate owner.

## Approved naming direction

The original quote above is preserved verbatim. The later naming decision
supersedes its working name:

> sure let's use cross check. rename the proejct, repo, and topic. then pick this up from where we got sidetracked with naming

The canonical product/package/CLI name is Crosscheck. The repository rename is
complete; installed legacy marketplace and skill identities remain compatible.
The existing branch and local execution path remain unchanged for continuity.
Managed instruction content stays in the existing Crosscheck Workshop proposal.
This implementation may prepare and test packaging in isolation, but may not
apply or activate that proposal, install live skills, merge, tag, release or deploy.
