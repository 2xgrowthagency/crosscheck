"""Durable local report; legacy field names remain a supported output contract."""
import json


def report(manifest, receipt):
    mode = {"decision": "decision", "process": "process"}.get(manifest["target"]["kind"], "deliverable")
    fields = {
        "RESULT": receipt["verdict"], "MODE": mode, "DECISION_MEANING": receipt["meaning"],
        "SCOPE": manifest["target"], "INTENT": manifest["intent"],
        "INDEPENDENCE": manifest["session"], "TARGET_FINGERPRINT": receipt["target_sha256"],
        "EVIDENCE_SNAPSHOT": receipt["manifest_sha256"], "CRITERIA_MATRIX": manifest["criteria"],
        "FINDINGS": receipt["problems"], "INDEPENDENT_CHECKS": manifest["checks"],
        "EVIDENCE": [{"check": c["id"], "artifacts": c["artifact_ids"]} for c in manifest["checks"]],
        "ARTIFACTS": manifest["artifacts"],
        "SKIPPED_OR_INCONCLUSIVE": [c for c in manifest["checks"] if c["status"] == "blocked"],
        "RISKS": manifest["risks"],
        "INVALIDATION_TRIGGERS": "Any target, base, environment, configuration, evidence, criteria or tool/session change; expiry.",
        "PUBLICATION": receipt["publication"],
        "RECOMMENDATION": receipt["meaning"],
    }
    return "# Final Boss QA report\n\n" + "\n\n".join(
        f"{key}: {value if isinstance(value, str) else json.dumps(value, sort_keys=True)}" for key, value in fields.items()) + "\n"
