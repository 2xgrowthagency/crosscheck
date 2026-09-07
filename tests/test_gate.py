import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import timedelta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/final-boss/runtime"))
from final_boss.gate import evaluate, validate_receipt, validate, instant, utc_now, fingerprint, PROFILES
from final_boss.publication import publish, summary
from final_boss.report import report
from jsonschema.exceptions import ValidationError


class GateFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".work" if (ROOT / ".work").is_dir() else None)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evidence = self.root / "evidence"
        shutil.copytree(ROOT / "examples/evidence", self.evidence)
        self.m = json.loads((self.evidence / "evidence-manifest.json").read_text())
        self.target = copy.deepcopy(self.m["target"])
        self.now = instant(self.m["session"]["finished_at"]) + timedelta(seconds=1)

    def evaluate(self):
        return evaluate(self.m, self.evidence, self.target, now=self.now)


class GateTests(GateFixture, unittest.TestCase):
    def test_behavior_corpus(self):
        original = copy.deepcopy(self.m)
        for case in json.loads((ROOT / "tests/fixtures/cases.json").read_text()):
            with self.subTest(case=case["name"]):
                self.m = copy.deepcopy(original)
                self.target = copy.deepcopy(self.m["target"])
                self.now = instant(self.m["session"]["finished_at"]) + timedelta(seconds=1)
                mutation = case["mutation"]
                if mutation == "fail": self.m["checks"][0]["status"] = "fail"
                if mutation == "missing": self.m["checks"][0]["artifact_ids"] = []
                if mutation == "stale": self.target["revision"] = "changed"
                if mutation == "producer":
                    for a in self.m["artifacts"]: a["origin"] = "producer"
                if mutation == "stills": self.m["checks"][0]["artifact_ids"] = ["screen"]
                if mutation == "unreviewed": self.m["artifacts"][0]["review"]["status"] = "unreviewed"
                if mutation == "redaction":
                    self.m["artifacts"][0]["sharing"] = "redacted"
                    self.m["artifacts"][0]["review"]["sha256"] = "f" * 64
                if mutation == "self": self.m["session"]["verifier_id"] = self.m["session"]["producer_id"]
                if mutation == "inherited": self.m["session"]["inherited_context"] = True
                if mutation == "expired": self.now += timedelta(hours=2)
                if mutation == "viewport": self.m["criteria"][0]["viewports"][0]["width"] = 320
                if mutation == "screenshot": self.m["artifacts"][0]["media"]["revision"] = "old"
                r = self.evaluate()
                self.assertEqual(case["verdict"], r["verdict"])
                self.assertEqual(case["verdict"] == "PASS", r["gate_cleared"])
                if r["verdict"] != "PASS":
                    self.assertTrue(all(p["owner"] and p["action"] for p in r["problems"]))

    def test_all_profiles_require_their_evidence(self):
        for profile, policy in PROFILES.items():
            with self.subTest(profile=profile):
                self.m["criteria"][0].update(profile=profile, visual=False, sequence=False)
                self.m["checks"][0]["artifact_ids"] = ["screen"]
                self.m["artifacts"][0]["kind"] = policy["evidence_any"][0]
                self.assertEqual("PASS", self.evaluate()["verdict"])
                self.m["artifacts"][0]["kind"] = "log"
                self.assertEqual("BLOCKED", self.evaluate()["verdict"])

    def test_fail_is_not_hidden_by_other_missing_checks(self):
        self.m["checks"][0]["status"] = "fail"
        other = copy.deepcopy(self.m["criteria"][0]); other["id"] = "missing"
        self.m["criteria"].append(other)
        self.assertEqual("FAIL", self.evaluate()["verdict"])
        self.target["base"] = "changed-base"
        self.assertEqual("BLOCKED", self.evaluate()["verdict"])

    def test_advisory_and_required_are_distinct(self):
        advisory = copy.deepcopy(self.m["criteria"][0]); advisory.update(id="advice", required=False)
        self.m["criteria"].append(advisory)
        self.assertEqual("PASS", self.evaluate()["verdict"])
        self.m["criteria"][0]["required"] = False
        with self.assertRaises(ValueError): self.evaluate()

    def test_schema_and_reference_failures(self):
        for mutate in [lambda m: m.update(schema_version="2.0"),
                       lambda m: m["target"].update(unexpected=True),
                       lambda m: m["session"].update(started_at="yesterday")]:
            invalid = copy.deepcopy(self.m); mutate(invalid)
            with self.assertRaises(ValidationError): evaluate(invalid, self.evidence, self.target, now=self.now)
        self.m["checks"][0]["artifact_ids"] = ["unknown"]
        with self.assertRaises(ValueError): self.evaluate()

    def test_duplicate_ids_and_destinations(self):
        self.m["checks"].append(copy.deepcopy(self.m["checks"][0]))
        with self.assertRaises(ValueError): self.evaluate()
        self.m["checks"].pop()
        same = copy.deepcopy(self.m["destinations"][0]); same["id"] = "other"
        self.m["destinations"].append(same)
        with self.assertRaises(ValueError): self.evaluate()

    def test_artifact_bytes_and_symlinks(self):
        p = self.evidence / self.m["artifacts"][0]["path"]
        p.write_bytes(b"changed")
        self.assertEqual("BLOCKED", self.evaluate()["verdict"])
        p.unlink(); p.symlink_to(ROOT / "LICENSE")
        self.assertEqual("BLOCKED", self.evaluate()["verdict"])
        self.m["artifacts"][0]["path"] = "artifacts/../../LICENSE"
        self.assertEqual("BLOCKED", self.evaluate()["verdict"])

    def test_receipt_rechecks_target_manifest_bytes_and_expiry(self):
        receipt = self.evaluate()
        self.assertTrue(validate_receipt(receipt, self.m, self.evidence, self.target, now=self.now))
        for field in ("revision", "base", "environment", "configuration_sha256"):
            target = copy.deepcopy(self.target); target[field] = "f" * 64
            with self.assertRaises(ValueError): validate_receipt(receipt, self.m, self.evidence, target, now=self.now)
        with self.assertRaises(ValueError):
            validate_receipt(receipt, self.m, self.evidence, self.target, now=self.now + timedelta(hours=2))
        self.m["intent"] += " New criteria."
        with self.assertRaises(ValueError): validate_receipt(receipt, self.m, self.evidence, self.target, now=self.now)

    def test_forged_gate_boolean_rejected(self):
        receipt = self.evaluate(); receipt["verdict"] = "FAIL"
        with self.assertRaises(ValidationError): validate(receipt, "final-boss-receipt")

    def test_local_only_media_can_prove_without_upload(self):
        for a in self.m["artifacts"]:
            a["sharing"] = "local-only"; a["review"]["status"] = "unreviewed"
        self.assertEqual("PASS", self.evaluate()["verdict"])

    def test_cli_writes_three_contracts_and_preserves_target(self):
        now = utc_now()
        self.m["session"].update(started_at=(now - timedelta(seconds=20)).isoformat(), finished_at=(now-timedelta(seconds=1)).isoformat())
        for a in self.m["artifacts"]: a["captured_at"] = (now-timedelta(seconds=10)).isoformat()
        mp = self.evidence / "evidence-manifest.json"; mp.write_text(json.dumps(self.m))
        tp = self.evidence / "current-target.json"; tp.write_text(json.dumps(self.target))
        target_root = self.root / "product"; target_root.mkdir(); (target_root / "sentinel").write_text("untouched")
        output = self.root / "reports"
        args = [sys.executable, "-m", "final_boss", "evaluate", "--manifest", str(mp), "--evidence-root", str(self.evidence),
                "--current-target", str(tp), "--target-root", str(target_root), "--output", str(output)]
        env = {**os.environ, "PYTHONPATH": str(ROOT / "plugins/final-boss/runtime")}
        done = subprocess.run(args, env=env, text=True, capture_output=True)
        self.assertEqual(0, done.returncode, done.stderr)
        self.assertEqual({"qa-report.md", "evidence-manifest.json", "final-boss-receipt.json"}, {p.name for p in output.iterdir()})
        self.assertEqual("untouched", (target_root / "sentinel").read_text())
        self.assertEqual(2, subprocess.run(args, env=env, capture_output=True).returncode)
        args[-1] = str(target_root / "reports")
        self.assertEqual(2, subprocess.run(args, env=env, capture_output=True).returncode)
        self.assertFalse((target_root / "reports").exists())
        receipt = json.loads((output / "final-boss-receipt.json").read_text())
        self.assertTrue(validate_receipt(receipt, self.m, self.evidence, self.target))

    def test_report_legacy_field_contract(self):
        result = report(self.m, self.evaluate())
        fields = dict(line.split(": ", 1) for line in result.splitlines() if ": " in line)
        self.assertEqual("PASS", fields["RESULT"])
        self.assertEqual("deliverable", fields["MODE"])
        for key in ("INDEPENDENCE", "TARGET_FINGERPRINT", "CRITERIA_MATRIX", "FINDINGS", "PUBLICATION", "RECOMMENDATION"):
            self.assertIn(key, fields)


class MemoryTransport:
    def __init__(self, target):
        self.target = target; self.comments = {}; self.writes = 0; self.fail = set(); self.timeout_once = False
    def current_target(self): return self.target
    def verify_destination(self, destination, target): return self.target == target
    def find_owned(self, destination, markers):
        body = self.comments.get(destination["id"])
        return {"body": body, "locator": "https://example.test/comments/" + destination["id"]} if body else None
    def put(self, destination, existing, body, key):
        if destination["id"] in self.fail: raise OSError("private transport detail")
        if not existing or existing["body"] != body:
            self.comments[destination["id"]] = body; self.writes += 1
        if self.timeout_once:
            self.timeout_once = False; raise TimeoutError("write succeeded but response lost")
        return "https://example.test/comments/" + destination["id"]


class PublicationTests(GateFixture, unittest.TestCase):
    def publish_setup(self):
        for d in self.m["destinations"]: d["authorized"] = True
        receipt = self.evaluate()
        body = summary(self.m, receipt, purpose="Verify the two-step demo", checked="Two clicks and the resulting screen",
                       next_action="Reviewer inspects the result", human_action="Nothing needed from you")
        approval = dict(reviewed=True, body_sha256=hashlib.sha256(body.encode()).hexdigest(), destinations=copy.deepcopy(self.m["destinations"]))
        return receipt, body, approval, MemoryTransport(self.target)

    def test_all_destinations_idempotent_and_retry_after_timeout(self):
        receipt, body, approval, t = self.publish_setup(); t.timeout_once = True
        result = publish(self.m, receipt, self.evidence, t, body, approval, now=self.now)
        self.assertEqual("PASS", result["verdict"])
        self.assertEqual("failed", result["publication"][0]["status"])
        result = publish(self.m, result, self.evidence, t, body, approval, now=self.now)
        self.assertEqual(3, t.writes)
        self.assertTrue(all(p["status"] == "published" for p in result["publication"]))

    def test_publication_failure_does_not_change_verdict(self):
        receipt, body, approval, t = self.publish_setup(); t.fail = {"issue"}
        result = publish(self.m, receipt, self.evidence, t, body, approval, now=self.now)
        self.assertEqual("PASS", result["verdict"]); self.assertTrue(result["gate_cleared"])
        self.assertEqual(["published", "failed", "published"], [p["status"] for p in result["publication"]])
        self.assertNotIn("private transport detail", json.dumps(result))

    def test_no_authority_inferred_from_association(self):
        receipt, body, approval, t = self.publish_setup()
        self.m["destinations"][1]["authorized"] = False; receipt = self.evaluate()
        result = publish(self.m, receipt, self.evidence, t, body, approval, now=self.now)
        self.assertNotIn("issue", t.comments)
        self.assertEqual("not-authorized", result["publication"][1]["status"])

    def test_unreviewed_summary_is_never_sent(self):
        receipt, body, approval, t = self.publish_setup()
        with self.assertRaises(ValueError): publish(self.m, receipt, self.evidence, t, body + "unreviewed", approval, now=self.now)
        self.assertEqual({}, t.comments)

    def test_target_changed_before_comment_invalidates_pass(self):
        receipt, body, approval, t = self.publish_setup(); t.target = {**self.target, "revision": "new"}
        result = publish(self.m, receipt, self.evidence, t, body, approval, now=self.now)
        self.assertEqual("BLOCKED", result["verdict"]); self.assertFalse(result["gate_cleared"])
        self.assertEqual({}, t.comments)


if __name__ == "__main__": unittest.main()
