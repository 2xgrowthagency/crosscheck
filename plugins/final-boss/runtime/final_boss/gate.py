"""Validate evidence bytes and derive a fail-closed, exact-target verdict."""
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
PROFILES = json.loads((ROOT / "profiles.json").read_text())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def fingerprint(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def validate(value, name):
    schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps require a timezone")
    return parsed.astimezone(timezone.utc)


def utc_now():
    return datetime.now(timezone.utc)


def unique(items, key="id"):
    result = {item[key]: item for item in items}
    if len(result) != len(items):
        raise ValueError(f"duplicate {key}")
    return result


def evidence_bytes(root, artifact):
    """Never traverse out of the bundle or follow evidence symlinks."""
    root = Path(root).resolve()
    path = root / artifact["path"]
    relative = path.relative_to(root)
    if ".." in relative.parts or any((root.joinpath(*relative.parts[:i])).is_symlink()
                                     for i in range(1, len(relative.parts) + 1)):
        raise ValueError("unsafe evidence path")
    if not path.resolve().is_relative_to(root):
        raise ValueError("evidence escapes bundle")
    return path.read_bytes()


def evaluate(manifest, evidence_root, current_target, *, now=None):
    """Consume independently collected observations, never run producer commands.

    Session attestations and current_target must come from a trusted fresh verifier
    adapter. JSON and hashes alone cannot establish truthful collection or sandboxing.
    """
    validate(manifest, "evidence-manifest")
    validate(current_target, "target")
    now = now or utc_now()
    if now.tzinfo is None:
        raise ValueError("clock requires a timezone")
    session = manifest["session"]
    criteria = unique(manifest["criteria"])
    if not any(c["required"] for c in criteria.values()):
        raise ValueError("at least one required criterion is necessary")
    artifacts = unique(manifest["artifacts"])
    unique(manifest["checks"])
    unique(manifest["destinations"])
    if len({(d["kind"], d["locator"]) for d in manifest["destinations"]}) != len(manifest["destinations"]):
        raise ValueError("duplicate publication destination")
    for check in manifest["checks"]:
        if check["criterion_id"] not in criteria or any(a not in artifacts for a in check["artifact_ids"]):
            raise ValueError("check refers to unknown criterion or artifact")
    target_hash = fingerprint(manifest["target"])
    start, finish = instant(session["started_at"]), instant(session["finished_at"])
    expiry = finish + timedelta(seconds=manifest["freshness_seconds"])
    problems, failures, gaps = [], [], []

    def problem(code, criterion_id=None, owner="verification owner", action=None, observation=None, artifact_ids=None):
        return dict(code=code, criterion_id=criterion_id, owner=owner, severity="error",
                    disposition="rework" if code == "required-defect" else "ask-owner",
                    observation=observation or code.replace("-", " "), artifact_ids=artifact_ids or [],
                    impact="The required criterion failed." if code == "required-defect" else "Verification cannot safely clear this target.",
                    action=action or "Start a fresh read-only verifier with a newly bound target and evidence.")

    if current_target != manifest["target"]:
        problems.append(problem("stale-target"))
    if not (start <= finish <= now <= expiry):
        problems.append(problem("stale-session"))
    if (session["producer_id"] == session["verifier_id"] or not session["ephemeral"]
            or session["inherited_context"] or session["target_write_owned"] or session["target_written"]):
        problems.append(problem("independence-unproven"))
    valid = set()
    for aid, artifact in artifacts.items():
        try:
            data = evidence_bytes(evidence_root, artifact)
            if len(data) != artifact["size"] or hashlib.sha256(data).hexdigest() != artifact["sha256"]:
                raise ValueError("artifact bytes changed")
        except (OSError, ValueError):
            problems.append(problem("artifact-integrity", action=f"Recapture and bind artifact {aid} in a fresh run."))
            continue
        if artifact["target_sha256"] != target_hash or not start <= instant(artifact["captured_at"]) <= finish:
            problems.append(problem("stale-evidence", action=f"Recapture current artifact {aid} in the bound session."))
            continue
        review = artifact["review"]
        if artifact["sharing"] != "local-only" and (
                review["status"] != "approved" or review["sha256"] != artifact["sha256"]):
            problems.append(problem("privacy-review", action=f"Keep {aid} local or review the exact sanitized bytes before sharing."))
            continue
        if artifact["origin"] == "verifier" and artifact["session_id"] == session["verifier_id"]:
            valid.add(aid)

    for cid, criterion in criteria.items():
        checks = [c for c in manifest["checks"] if c["criterion_id"] == cid]
        if not criterion["required"]:
            continue
        if not checks:
            gaps.append(problem("missing-check", cid, action=f"Run an independent check for {cid}."))
        for check in checks:
            usable = [artifacts[a] for a in check["artifact_ids"] if a in valid]
            if not usable or check["status"] == "blocked":
                gaps.append(problem("inconclusive-check", cid, check["owner"], check["action"],
                                    check["observation"], check["artifact_ids"]))
                continue
            if check["status"] == "fail":
                failures.append(problem("required-defect", cid, check["owner"], check["action"],
                                    check["observation"], check["artifact_ids"]))
                continue
            kinds = {a["kind"] for a in usable}
            if not kinds.intersection(PROFILES[criterion["profile"]]["evidence_any"]):
                gaps.append(problem("missing-profile-evidence", cid, action=f"Collect {criterion['profile']} evidence for {cid}."))
            if criterion["visual"] or criterion["profile"] == "ui":
                screenshots = [a for a in usable if a["kind"] == "screenshot"
                               and a["media"]["url"] == manifest["target"]["locator"]
                               and a["media"]["revision"] == manifest["target"]["revision"]]
                if not criterion["viewports"] or not all(
                        any(a["media"]["viewport"] == viewport for a in screenshots)
                        for viewport in criterion["viewports"]):
                    gaps.append(problem("missing-current-screenshot", cid, action=f"Capture the bound URL/revision and required viewport for {cid}."))
            if criterion["sequence"] and not any(
                    a["kind"] in ("video", "trace") and a["media"]["sequence_proven"]
                    and a["media"]["revision"] == manifest["target"]["revision"]
                    and a["media"]["url"] == manifest["target"]["locator"] for a in usable):
                gaps.append(problem("missing-interaction-media", cid,
                                    action=f"Provide a safe ordered trace or reviewed recording for {cid}; do not record private material."))
    # Invalid target/session/integrity defeats even conclusive observations.
    verdict = "BLOCKED" if problems else "FAIL" if failures else "BLOCKED" if gaps else "PASS"
    all_problems = problems + failures + gaps
    meaning = {"PASS": PROFILES[manifest["target"]["kind"]]["pass_permits"] + "; no merge, closure, deployment or mutation authority.",
               "FAIL": "A required criterion failed. The named producer owns bounded rework, followed by fresh verification.",
               "BLOCKED": "The target is not cleared. The named owner must perform the exact unblock action before fresh verification."}[verdict]
    receipt = dict(schema_version="1.0", packet_id=manifest["packet_id"], target_sha256=target_hash,
                   manifest_sha256=fingerprint(manifest), verifier_id=session["verifier_id"],
                   evaluated_at=now.isoformat(), expires_at=expiry.isoformat(), verdict=verdict,
                   gate_cleared=verdict == "PASS", meaning=meaning, problems=all_problems,
                   publication=[dict(destination_id=d["id"], status="pending" if d["authorized"] else "not-authorized",
                                     comment_locator=None, reason=None) for d in manifest["destinations"]])
    validate(receipt, "final-boss-receipt")
    return receipt


def validate_receipt(receipt, manifest, evidence_root, current_target, *, now=None):
    """A stored PASS is never consumed by trusting its boolean alone."""
    validate(receipt, "final-boss-receipt")
    expected = evaluate(manifest, evidence_root, current_target, now=now)
    for key in ("packet_id", "target_sha256", "manifest_sha256", "verifier_id", "verdict", "gate_cleared", "meaning", "problems", "expires_at"):
        if receipt[key] != expected[key]:
            raise ValueError(f"receipt no longer valid: {key}")
    if not instant(manifest["session"]["finished_at"]) <= instant(receipt["evaluated_at"]) <= (now or utc_now()):
        raise ValueError("invalid receipt evaluation time")
    expected_destinations = {p["destination_id"] for p in expected["publication"]}
    if set(unique(receipt["publication"], "destination_id")) != expected_destinations:
        raise ValueError("receipt publication destinations differ")
    return expected["gate_cleared"]
