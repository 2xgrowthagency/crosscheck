# Final Boss QA report

RESULT: PASS

MODE: deliverable

DECISION_MEANING: Review of this tested workflow; no merge, closure, deployment or mutation authority.

SCOPE: {"base": "synthetic-demo-v1", "configuration_sha256": "0000000000000000000000000000000000000000000000000000000000000000", "environment": "local-synthetic", "kind": "interaction", "locator": "http://127.0.0.1:8765/demo.html", "revision": "7a3419f514da56d5982d5f486ab1c1519653992a446f9226c5bf9ad66e136226"}

INTENT: Verify that the synthetic two-step demo shows its final state and preserves the ordered interaction.

INDEPENDENCE: {"attestation": "SIMULATED session admission for contract tests only. Media was captured by the implementation worker; this is not independent QA.", "ephemeral": true, "finished_at": "2026-09-07T00:44:35.223712+00:00", "inherited_context": false, "producer_id": "synthetic-producer", "started_at": "2026-09-07T00:41:58+00:00", "target_write_owned": false, "target_written": false, "verifier_id": "synthetic-verifier"}

TARGET_FINGERPRINT: f1495fe485c979eeb2bd85961d6af410a1ca7255e2963227e1384931783b7386

EVIDENCE_SNAPSHOT: a6fe49b32f8d6b291ce190539799ed4543f3da96d1b581c971faf3c96bb7484d

CRITERIA_MATRIX: [{"description": "Two clicks reach Step 2 of 2 in order, with current layout proof.", "id": "demo", "profile": "interaction", "required": true, "sequence": true, "viewports": [{"height": 640, "width": 960}], "visual": true}]

CRITERION_TOTALS: {"advisory": {"blocked": 0, "failed": 0, "passed": 0, "total": 0}, "required": {"blocked": 0, "failed": 0, "passed": 1, "total": 1}}

FINDINGS: []

INDEPENDENT_CHECKS: [{"action": "Correct only the failed step and request fresh verification.", "artifact_ids": ["screen", "sequence"], "criterion_id": "demo", "id": "two-clicks", "observation": "Observed Step 0, then Step 1, then Step 2 with an isolated synthetic page.", "owner": "demo producer", "status": "pass"}]

EVIDENCE: [{"artifacts": ["screen", "sequence"], "check": "two-clicks"}]

ARTIFACTS: [{"captured_at": "2026-09-07T00:42:00.212083+00:00", "id": "screen", "kind": "screenshot", "media": {"revision": "7a3419f514da56d5982d5f486ab1c1519653992a446f9226c5bf9ad66e136226", "sequence_proven": false, "url": "http://127.0.0.1:8765/demo.html", "viewport": {"height": 640, "width": 960}}, "origin": "verifier", "path": "artifacts/current.png", "review": {"reviewer": "fixture-author-reviewed-synthetic-media", "sha256": "5da2e72363a11fa6c49cc0afca48be2091b486b6875313f45a7b35775d0aa2ca", "status": "approved"}, "session_id": "synthetic-verifier", "sha256": "5da2e72363a11fa6c49cc0afca48be2091b486b6875313f45a7b35775d0aa2ca", "sharing": "safe-to-share", "size": 21176, "target_sha256": "f1495fe485c979eeb2bd85961d6af410a1ca7255e2963227e1384931783b7386", "tool": {"name": "Playwright", "version": "1.58.0"}}, {"captured_at": "2026-09-07T00:42:00.212569+00:00", "id": "sequence", "kind": "trace", "media": {"revision": "7a3419f514da56d5982d5f486ab1c1519653992a446f9226c5bf9ad66e136226", "sequence_proven": true, "url": "http://127.0.0.1:8765/demo.html", "viewport": {"height": 640, "width": 960}}, "origin": "verifier", "path": "artifacts/interaction-trace.json", "review": {"reviewer": "fixture-author-reviewed-synthetic-media", "sha256": "30b9137106575550ef58c3fc1935010944df06d2e07a79dd4a3fc115ce26f523", "status": "approved"}, "session_id": "synthetic-verifier", "sha256": "30b9137106575550ef58c3fc1935010944df06d2e07a79dd4a3fc115ce26f523", "sharing": "safe-to-share", "size": 728, "target_sha256": "f1495fe485c979eeb2bd85961d6af410a1ca7255e2963227e1384931783b7386", "tool": {"name": "Playwright", "version": "1.58.0"}}]

SKIPPED_OR_INCONCLUSIVE: []

RISK: ["Synthetic contract example; does not certify the Final Boss process or model interpretation."]

RISKS: ["Synthetic contract example; does not certify the Final Boss process or model interpretation."]

INVALIDATION_TRIGGERS: Any target, base, environment, configuration, evidence, criteria or tool/session change; expiry.

PUBLICATION: [{"comment_locator": null, "destination_id": "pr", "reason": null, "status": "not-authorized"}, {"comment_locator": null, "destination_id": "issue", "reason": null, "status": "not-authorized"}, {"comment_locator": null, "destination_id": "worker", "reason": null, "status": "not-authorized"}]

RECOMMENDATION: Review of this tested workflow; no merge, closure, deployment or mutation authority.
