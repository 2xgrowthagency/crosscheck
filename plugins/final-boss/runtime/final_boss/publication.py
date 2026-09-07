"""Optional result-comment transport; no product mutation or media upload API."""
import copy
import hashlib
from typing import Protocol

from .gate import evaluate, validate, validate_receipt, fingerprint, utc_now
from .report import bind_report, validate_report


class CommentTransport(Protocol):
    """One trusted single writer per packet and target.

    verify_destination must confirm exact repository/PR head or issue binding,
    and original worker identity. find_owned searches all pages and returns only
    comments authored by this adapter identity with an exact marker match.
    put must upsert with the supplied key, including after timeout/restart.
    A worker transport without readback/idempotency must refuse publication.
    No transport may treat a worker result notice as a repair command.
    """
    def current_target(self): ...
    def verify_destination(self, destination, target): ...
    def find_owned(self, destination, markers): ...
    def put(self, destination, existing, body, key): ...


def summary(manifest, receipt, *, purpose, checked, next_action, human_action):
    """Build a candidate; apply active communication guidance before approval."""
    marker = f"<!-- final-boss-result:{manifest['packet_id']}:{receipt['target_sha256']} -->"
    return (f"{marker}\nFinal Boss: {receipt['verdict']} — {receipt['meaning']}\n\n"
            f"Purpose: {purpose}\n\nChecked: {checked}\n\n"
            f"Next: {next_action}\n\nHuman action: {human_action}\n\n"
            "Full report retained locally. This result does not authorize product changes.\n")


def publish(manifest, receipt, evidence_root, transport, body, approval, *, report_bytes, clock=utc_now):
    """Publish a reviewed summary to EVERY explicitly authorized destination.

    approval is supplied by the trusted caller after privacy and communication
    review, never inferred from association, a producer packet, or elapsed time.
    Only body is sent; artifacts, raw reports, exception text and paths stay local.
    """
    result = copy.deepcopy(receipt)
    validate(result, "final-boss-receipt")
    validate_report(manifest, result, report_bytes)
    statuses = {p["destination_id"]: p for p in result["publication"]}

    def changed(fresh):
        stale_codes = {"stale-target", "stale-session", "stale-evidence", "artifact-integrity"}
        return (fresh["verdict"] != result["verdict"] or fresh["problems"] != result["problems"]
                or any(p["code"] in stale_codes for p in fresh["problems"]))

    def invalidate(fresh):
        # Preserve remote locations for reconciliation, including a just-written
        # comment. Never label a known-stale posted/reused PASS as current success.
        for state in statuses.values():
            if state["status"] != "not-authorized":
                state.update(status="stale", reason="Result is stale. Reconcile any prior comment and request a fresh verifier.")
        fresh["publication"] = list(statuses.values())
        return bind_report(manifest, fresh)

    def refresh(destination=None):
        # Destination lookup is also remote work. Read the live target and clock
        # AFTER it; no frozen invocation timestamp may outlive remote pagination.
        admitted = destination is None or transport.verify_destination(destination, manifest["target"])
        current = transport.current_target()
        fresh = evaluate(manifest, evidence_root, current, now=clock())
        if changed(fresh):
            return invalidate(fresh)
        if not admitted:
            raise ValueError("destination binding could not be confirmed")
        return None

    current = transport.current_target()
    now = clock()
    fresh = evaluate(manifest, evidence_root, current, now=now)
    if changed(fresh):
        return invalidate(fresh)
    validate_receipt(result, manifest, evidence_root, current, report_bytes=report_bytes, now=now)
    marker = f"<!-- final-boss-result:{manifest['packet_id']}:{fingerprint(manifest['target'])} -->"
    if not body.startswith(marker + "\n") or f"Final Boss: {result['verdict']}" not in body:
        raise ValueError("summary verdict/binding differs from receipt")
    if approval.get("body_sha256") != hashlib.sha256(body.encode()).hexdigest() or approval.get("reviewed") is not True:
        raise ValueError("the exact comment body needs explicit privacy and communication review")
    approved = approval.get("destinations", [])
    legacy = [f"<!-- {prefix}:{manifest['packet_id']}:{result['target_sha256']} -->"
              for prefix in ("independent-qa-result", "workboard-qa-result")]
    for destination in manifest["destinations"]:
        state = statuses[destination["id"]]
        if not destination["authorized"]:
            state.update(status="not-authorized", comment_locator=None, reason="No explicit comment authorization.")
            continue
        if destination not in approved:
            state.update(status="failed", comment_locator=None, reason="Exact destination was not approved for this summary.")
            continue
        try:
            stale = refresh(destination)
            if stale is not None:
                return stale
            existing = transport.find_owned(destination, [marker] + legacy)
            if existing and isinstance(existing.get("locator"), str):
                state["comment_locator"] = existing["locator"]
            stale = refresh(destination)
            if stale is not None:
                return stale
            if existing and existing.get("body") == body:
                location = existing["locator"]
            else:
                location = transport.put(destination, existing, body, marker)
            if not isinstance(location, str) or not location.strip():
                raise ValueError("publication has no durable readback")
            state["comment_locator"] = location
            stale = refresh(destination)
            if stale is not None:
                return stale
            state.update(status="published", comment_locator=location, reason=None)
        except Exception:
            # API exceptions may contain auth headers or private content. Never echo them.
            state.update(status="failed",
                         reason="Comment delivery or readback failed; reconcile this destination before retrying.")
    try:
        stale = refresh()
    except Exception:
        # A failed final freshness read cannot confirm delivery/closeout. Keep
        # the product verdict and remote locations, without exposing API text.
        for state in statuses.values():
            if state["status"] == "published":
                state.update(status="failed",
                             reason="Final freshness readback failed; reconcile this destination before retrying.")
        return bind_report(manifest, result)
    return stale if stale is not None else bind_report(manifest, result)
