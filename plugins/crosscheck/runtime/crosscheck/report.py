"""Durable local report; legacy field names remain a supported output contract."""
import copy
import hashlib
import json


def report(manifest, receipt):
    mode = {"decision": "decision", "process": "process"}.get(manifest["target"]["kind"], "deliverable")
    fields = {
        "RESULT": receipt["verdict"], "MODE": mode, "DECISION_MEANING": receipt["meaning"],
        "SCOPE": manifest["target"], "INTENT": manifest["intent"],
        "INDEPENDENCE": manifest["session"], "TARGET_FINGERPRINT": receipt["target_sha256"],
        "EVIDENCE_SNAPSHOT": receipt["manifest_sha256"], "CRITERIA_MATRIX": manifest["criteria"],
        "CRITERION_TOTALS": receipt["criterion_totals"],
        "FINDINGS": receipt["problems"], "INDEPENDENT_CHECKS": manifest["checks"],
        "EVIDENCE": [{"check": c["id"], "artifacts": c["artifact_ids"]} for c in manifest["checks"]],
        "ARTIFACTS": manifest["artifacts"],
        "SKIPPED_OR_INCONCLUSIVE": [c for c in manifest["checks"] if c["status"] == "blocked"],
        "RISK": manifest["risks"], "RISKS": manifest["risks"],
        "INVALIDATION_TRIGGERS": "Any target, base, environment, configuration, evidence, criteria or tool/session change; expiry.",
        "PUBLICATION": receipt["publication"],
        "RECOMMENDATION": receipt["meaning"],
    }
    return "# Crosscheck QA report\n\n" + "\n\n".join(
        f"{key}: {value if isinstance(value, str) else json.dumps(value, sort_keys=True)}" for key, value in fields.items()) + "\n"


def bind_report(manifest, receipt):
    """Report excludes its own digest: render first, then bind exact UTF-8 bytes.

    Reapply after publication changes. Persist report bytes before the receipt;
    mixed generations fail consumption, including after an interrupted write.
    """
    result = copy.deepcopy(receipt)
    result["report_sha256"] = hashlib.sha256(report(manifest, result).encode("utf-8")).hexdigest()
    return result


def validate_report(manifest, receipt, report_bytes):
    if not isinstance(report_bytes, bytes):
        raise ValueError("persisted report bytes are required")
    current = report(manifest, receipt).encode("utf-8")
    # Unreleased Final Boss receipts retain their exact original heading/hash.
    # Accept only that known render variant, never normalize the supplied bytes.
    legacy = current.replace(b"# Crosscheck QA report\n", b"# Final Boss QA report\n", 1)
    if (hashlib.sha256(report_bytes).hexdigest() != receipt["report_sha256"]
            or report_bytes not in (current, legacy)):
        raise ValueError("report does not match the completion receipt")
