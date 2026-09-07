# Result publication

Publish only after the verdict, report, receipt, and evidence manifest are complete and the target still matches.

Use a stable marker keyed by packet and target. Read existing comments; update or skip the matching result instead of duplicating it. Publish to each explicitly associated PR and issue, and notify the original worker thread according to the packet policy.

A public summary contains:

```markdown
<!-- crosscheck-result:PACKET_ID:TARGET_ID -->
## Crosscheck: PASS|FAIL|BLOCKED

**What this was for:** one plain-language sentence.
**What I checked:** short ordinary-language summary.
**Result:** practical meaning, including what this does not authorize.
**What happens next:** review, bounded rework, or exact unblock action and owner.
**Evidence:** approved link, or “full evidence retained in the task artifacts.”
```

Do not publish secrets, cookies, customer/client data, raw logs, absolute local paths, or unreviewed media.

The worker notification is informational and must not trigger self-directed rework. It states the verdict, practical meaning, bounded findings/blocker, safe report link, and next lane. Root/orchestrator decides whether to requeue.

Track delivery workflow separately from the runtime receipt. Labels such as not required, partial, skipped or blocked may explain workflow state in prose; never serialize them as runtime receipt publication statuses. Receipt schema 1.1 permits exactly `pending`, `not-authorized`, `published`, `failed`, and `stale`; use the installed schema and transport outcome for each destination. A publication failure never changes a conclusive QA verdict, but any required destination without verified delivery blocks workflow closeout.