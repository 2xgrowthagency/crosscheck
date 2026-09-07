# Runtime integration

The runtime validates structured observations. It does not independently establish their truth, model independence or authority. Read the installed version's schemas; never reuse fixture IDs, admission flags, timestamps, current-target readbacks or conclusions for real QA.

## Inputs and isolation

The trusted controller supplies producer/verifier identity, fresh-session admission, immutable target and protected original acceptance criteria. Confirm those against actual execution state. A different name/model or self-written attestation does not prove independence. Freeze criteria before checking; a hash of a modified contract does not prove fidelity to the request.

Schema 1.0 manifest fields are packet_id, intent, target, session, freshness_seconds, criteria, checks, artifacts, destinations and risks. Target fields bind kind, locator, revision, base, environment and configuration_sha256. Consult the installed schemas for field types and nested contracts.

Keep the target and completed evidence read-only; write results to a new private directory outside both roots. Collect fresh evidence using permitted tools; hash final reviewed bytes. Fixtures prove validator behavior, never actual deliverable or verifier success.

## Evaluate and consume

```text
crosscheck evaluate --manifest MANIFEST --evidence-root EVIDENCE --current-target READBACK --target-root TARGET --output NEW_OUTPUT
crosscheck verify-receipt --manifest MANIFEST --evidence-root EVIDENCE --current-target FRESH_READBACK --target-root TARGET --receipt RECEIPT
```

Evaluate returns 0 PASS, 1 FAIL, 2 BLOCKED. Require qa-report.md, evidence-manifest.json and crosscheck-receipt.json, not process success alone. Re-observe the target immediately before receipt consumption. Do not hand-author gate_cleared. Report integrity is required: the receipt must bind the final report bytes; if the installed runtime omits this binding, record the contract gap instead of weakening it.

## Publication

The publication API requires a reviewed summary, its exact body hash and separately authorized destinations. Obtain authority from the controlling session, not a packet boolean or associated URL. Existing explicit authority persists across retries; do not ask again for routine publication.

The transport must verify current target and exact issue/PR/original worker identity, reconcile owned comments across all pages, and read back durable publication. Keep publication state separate from verdict; missing worker adapter/readback blocks required delivery. A worker notice is informational, not a repair command. Keep reports consistent when publication state changes and rebind their final bytes.

## Compatibility

After canonical source integration, prove actual Codex and Claude skill discovery/invocation in isolated test destinations. Runtime installer aliases do not establish skill compatibility. Preserve the legacy invocation until replacement behavior passes. No live skill/plugin activation is implied by preparation or isolated testing. Preserve legacy independent-qa-agent and workboard-qa-agent invocation compatibility; final-boss is the prior unreleased working name.