# QA Result Publication

Use this closeout only after the independent verdict and local report are complete, and only when the task explicitly authorizes the exact destination.

## Safety rules

- Verify the repository, pull request, issue, or task belongs to the QA packet.
- For a pull request, verify the tested commit matches the current PR head or an explicitly declared immutable target.
- Never publish secrets, cookies, private logs, customer data, absolute local paths, or raw screenshots.
- Result publication does not authorize code changes, reviews, approvals, merges, labels, issue closure, artifact uploads, or messages to additional destinations.
- A publication failure never changes the QA verdict.

## Idempotent marker

Read existing comments before writing and reuse this marker:

```html
<!-- independent-qa-result:PACKET_ID:TARGET_ID -->
```

Update or skip a matching comment instead of duplicating it. If editing is unavailable and the verdict changed, state that the new comment supersedes the prior result.

## Comment template

```markdown
<!-- independent-qa-result:PACKET_ID:TARGET_ID -->
## Independent QA: PASS|FAIL|BLOCKED

- Target tested: `IMMUTABLE_TARGET`
- Packet: `PACKET_ID`
- Criteria: SHORT_PASS_FAIL_SUMMARY
- Material findings: NONE_OR_BOUNDED_FINDINGS
- Residual risks / unsupported checks: NONE_OR_DETAILS
- Recommendation: REVIEW_OR_REWORK_OR_UNBLOCK_ACTION
- Full report: APPROVED_EXTERNAL_LINK_OR_LOCAL_REPORT_RETAINED

This comment reports independent verification only; it does not approve or merge the change.
```

Record the resulting destination URL in `PUBLICATION`. When writing is unavailable, return the verified target and prepared body instead of guessing or silently skipping the closeout.
