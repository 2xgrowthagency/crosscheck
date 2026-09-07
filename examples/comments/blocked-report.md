# Crosscheck QA report

RESULT: BLOCKED

MODE: deliverable

DECISION_MEANING: The target is not cleared. The named owner must perform the exact unblock action before fresh verification.

SCOPE: {"base": "synthetic-demo-v1", "configuration_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "environment": "local-synthetic", "kind": "interaction", "locator": "http://127.0.0.1:8765/demo.html", "revision": "a24292d9a877c25306908776204ec3e89d31a872a4414257e67fb04bfed0bea4"}

INTENT: Verify that the synthetic two-step demo shows its final state and preserves the ordered interaction.

INDEPENDENCE: {"attestation": "SIMULATED session admission for contract tests only. Media was captured by the implementation worker; this is not independent QA.", "ephemeral": true, "finished_at": "2026-09-07T06:01:50.892836+00:00", "inherited_context": false, "producer_id": "synthetic-producer", "started_at": "2026-09-07T06:01:48.816618+00:00", "target_write_owned": false, "target_written": false, "verifier_id": "synthetic-verifier"}

TARGET_FINGERPRINT: 895da7408044a3c67b2228409971c7626fb31152a0b3dd6ddce53f6ad29a1162

EVIDENCE_SNAPSHOT: 91e1a1c27ce7bf24ed97890d417f0e9f0163177ef82f1199aef1369b58604149

CRITERIA_MATRIX: [{"description": "Two clicks reach Step 2 of 2 in order, with current layout proof.", "id": "demo", "profile": "interaction", "required": true, "sequence": true, "viewports": [{"height": 640, "width": 960}], "visual": true}]

CRITERION_TOTALS: {"advisory": {"blocked": 0, "failed": 0, "passed": 0, "total": 0}, "required": {"blocked": 1, "failed": 0, "passed": 0, "total": 1}}

FINDINGS: [{"action": "Verification owner: provide a synthetic interaction surface or safe trace.", "artifact_ids": [], "code": "inconclusive-check", "criterion_id": "demo", "disposition": "ask-owner", "impact": "Verification cannot safely clear this target.", "observation": "No safe ordered trace was available.", "owner": "demo producer", "severity": "error"}]

INDEPENDENT_CHECKS: [{"action": "Verification owner: provide a synthetic interaction surface or safe trace.", "artifact_ids": [], "criterion_id": "demo", "id": "two-clicks", "observation": "No safe ordered trace was available.", "owner": "demo producer", "status": "blocked"}]

EVIDENCE: [{"artifacts": [], "check": "two-clicks"}]

ARTIFACTS: [{"captured_at": "2026-09-07T06:01:50.892836+00:00", "id": "screen", "kind": "screenshot", "media": {"revision": "a24292d9a877c25306908776204ec3e89d31a872a4414257e67fb04bfed0bea4", "sequence_proven": false, "url": "http://127.0.0.1:8765/demo.html", "viewport": {"height": 640, "width": 960}}, "origin": "verifier", "path": "artifacts/current.png", "review": {"reviewer": "fixture-author-reviewed-synthetic-media", "sha256": "873546cfe7f5183627138ef59d92bb97d438fb3a6ca9ff3e17d116c4db3a21be", "status": "approved"}, "session_id": "synthetic-verifier", "sha256": "873546cfe7f5183627138ef59d92bb97d438fb3a6ca9ff3e17d116c4db3a21be", "sharing": "safe-to-share", "size": 21817, "target_sha256": "895da7408044a3c67b2228409971c7626fb31152a0b3dd6ddce53f6ad29a1162", "tool": {"name": "Playwright", "version": "1.58.0"}}, {"captured_at": "2026-09-07T06:01:50.892836+00:00", "id": "sequence", "kind": "trace", "media": {"revision": "a24292d9a877c25306908776204ec3e89d31a872a4414257e67fb04bfed0bea4", "sequence_proven": true, "url": "http://127.0.0.1:8765/demo.html", "viewport": {"height": 640, "width": 960}}, "origin": "verifier", "path": "artifacts/interaction-trace.json", "review": {"reviewer": "fixture-author-reviewed-synthetic-media", "sha256": "04018f070fb9da32c6af14232896a3d0596ca0c64b56fb1008c97cd3744abac7", "status": "approved"}, "session_id": "synthetic-verifier", "sha256": "04018f070fb9da32c6af14232896a3d0596ca0c64b56fb1008c97cd3744abac7", "sharing": "safe-to-share", "size": 728, "target_sha256": "895da7408044a3c67b2228409971c7626fb31152a0b3dd6ddce53f6ad29a1162", "tool": {"name": "Playwright", "version": "1.58.0"}}]

SKIPPED_OR_INCONCLUSIVE: [{"action": "Verification owner: provide a synthetic interaction surface or safe trace.", "artifact_ids": [], "criterion_id": "demo", "id": "two-clicks", "observation": "No safe ordered trace was available.", "owner": "demo producer", "status": "blocked"}]

RISK: ["Synthetic contract example; does not certify the Crosscheck process or model interpretation."]

RISKS: ["Synthetic contract example; does not certify the Crosscheck process or model interpretation."]

INVALIDATION_TRIGGERS: Any target, base, environment, configuration, evidence, criteria or tool/session change; expiry.

PUBLICATION: [{"comment_locator": null, "destination_id": "pr", "reason": null, "status": "not-authorized"}, {"comment_locator": null, "destination_id": "issue", "reason": null, "status": "not-authorized"}, {"comment_locator": null, "destination_id": "worker", "reason": null, "status": "not-authorized"}]

RECOMMENDATION: The target is not cleared. The named owner must perform the exact unblock action before fresh verification.
