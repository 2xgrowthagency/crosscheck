---
name: "crosscheck"
description: "Independently verify completed work, decisions, or QA processes with fresh evidence and a read-only PASS/FAIL gate."
---

# Crosscheck

Run after the builder finishes the assignment and its normal tests/review/No Mistakes gate. Crosscheck verifies an exact completed target; it never repairs it or grants approval.

## Admission

Require a fresh ephemeral verifier that neither built nor materially changed the target and does not inherit the builder conversation as trusted context. Record actual producer/verifier execution identities and target-write separation. Builder summaries, screenshots and logs are leads, not proof.

The controller supplies original intent, protected required/advisory criteria, immutable target locators, permitted read surfaces and publication authority. If identity, independence, safe isolation, binding or required evidence cannot be established, return BLOCKED. A name or model change is not independence.

Keep the target read-only. Only local QA artifacts and explicitly authorized result comments/worker notices may be written. Never repair, merge, close, deploy, mutate accounts/settings, access secrets or expand authority.

## Choose scope

Select deliverable, decision or process mode and the applicable [task profiles](references/task-profiles.md). Combine profiles when necessary. Classify risk from reversibility, blast radius, privacy/security, money, production impact and ambiguity. Use the strongest suitable available reasoning model; the 2x Codex adapter defaults to Astra medium and escalates high-risk, cross-system, consequential-decision or ambiguous process checks to Astra high. Model choice never proves quality.

Before reading producer conclusions, record the original intent/exclusions, what PASS permits, target/base/environment/config fingerprint, associated issue/PR/worker, freshness window, sharing policy, risk and criterion-to-check map. Classify required versus advisory before testing. Inspect safe available context before asking for information already on disk.

## Execute

1. Bind the exact commit/content hash and relevant deployment, account, environment, configuration or process/corpus version. For code, confirm local and remote/PR head and base.
2. Run the smallest independent check set covering every required criterion and named safety invariant. Exercise behavior and semantic output; instruction keywords and producer logs are not behavior proof.
3. Seek proportionate counterevidence and realistic failure cases. Reproduce prior regressions when safe.
4. Capture current evidence using [evidence bundle](references/evidence-bundle.md). Require named viewport screenshots for visual claims and ordered interaction evidence when sequence matters; pair server-side effects with persisted-state proof. Preserve raw evidence locally and review exact derivative bytes before sharing.
5. Recheck target before verdict and publication. Any target, base, deployment, content, evidence or material configuration change invalidates the result.
6. Return one verdict and publish according to [result publication](references/result-publication.md). Runtime-backed runs also read [runtime integration](references/runtime-integration.md); never invent receipts or present synthetic fixtures as real QA.

## Gate and findings

- PASS: every required criterion passed with fresh durable proof. Only PASS clears the exact target.
- FAIL: a required criterion is violated or contradicted by observed evidence.
- BLOCKED: required intent, independence, authorization, capability, evidence or freshness is unavailable. It is a non-pass, never a caveat.

Decision PASS means ready for the named human decision, not approved or authorized. Process verdict applies only to the bound version and evaluated corpus. Advisory observations may remain only if classified before checking and do not undermine required conclusions.

Each finding identifies severity, criterion, observation, evidence, impact, owner and bounded next action: rework, ask-owner or no-op. Crosscheck never performs rework; the controller routes it.

## Outputs and delivery

Retain qa-report.md, evidence-manifest.json, crosscheck-receipt.json and contract-required media/raw evidence. The report preserves RESULT, MODE, DECISION_MEANING, INTENT, SCOPE, RISK, INDEPENDENCE, TARGET_FINGERPRINT, EVIDENCE_SNAPSHOT, CRITERIA_MATRIX, FINDINGS, INDEPENDENT_CHECKS, EVIDENCE, ARTIFACTS, SKIPPED_OR_INCONCLUSIVE, RISKS, INVALIDATION_TRIGGERS, PUBLICATION and RECOMMENDATION.

The receipt binds schema/version, verdict, target, verifier execution, completed time, criteria totals, manifest hash, final report hash, invalidation/expiry and publication state. Consumers fail closed on missing/invalid receipts, non-PASS, changed target or stale evidence. A delivery failure does not overwrite a conclusive product verdict but blocks closeout when delivery is required.

Re-read active communication/taste guidance at publication; never copy private local rules into this public skill. Start the summary with PASS, FAIL or BLOCKED, then explain in ordinary language what the work was for, what was independently checked, what the result means, who acts next and whether a person needs to do anything. Keep hashes, paths, commands and exhaustive matrices in the local report. Publish only approved safe links/derivatives and verify all required issue, PR and original worker destinations.
