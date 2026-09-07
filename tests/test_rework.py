"""Accepted source-review regressions: observable publication and CLI behavior."""
import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from datetime import timedelta

from test_gate import GateFixture, MemoryTransport, ROOT
from crosscheck.gate import utc_now
from crosscheck.publication import publish, summary
from crosscheck.report import report, bind_report
from crosscheck.gate import validate_receipt, instant


class ReworkTests(GateFixture, unittest.TestCase):
    def publication_inputs(self):
        self.m["destinations"] = [dict(id="worker", kind="worker-thread",
            locator="synthetic-producer", authorized=True)]
        receipt = self.evaluate()
        body = summary(self.m, receipt, purpose="Check the demo", checked="Both steps",
                       next_action="Owner review", human_action="None")
        approval = dict(reviewed=True, body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                        destinations=copy.deepcopy(self.m["destinations"]))
        return receipt, body, approval

    def test_single_destination_changes_during_lookup(self):
        receipt, body, approval = self.publication_inputs()
        transport = MemoryTransport(copy.deepcopy(self.target))
        def lookup(destination, markers):
            transport.target["revision"] = "changed-during-pagination"
            return None
        transport.find_owned = lookup
        result = publish(self.m, receipt, self.evidence, transport, body, approval, report_bytes=report(self.m, receipt).encode(), clock=lambda: self.now)
        self.assertEqual("BLOCKED", result["verdict"])
        self.assertFalse(result["gate_cleared"])
        self.assertEqual(0, transport.writes)

    def send(self, receipt, body, approval, transport):
        return publish(self.m, receipt, self.evidence, transport, body, approval,
                       report_bytes=report(self.m, receipt).encode(), clock=lambda: self.now)

    def test_reused_comment_is_not_current_after_lookup_change(self):
        receipt, body, approval = self.publication_inputs()
        transport = MemoryTransport(copy.deepcopy(self.target))
        def lookup(destination, markers):
            transport.target["revision"] = "changed"
            return dict(body=body, locator="https://example.test/prior-comment")
        transport.find_owned = lookup
        result = self.send(receipt, body, approval, transport)
        self.assertEqual("BLOCKED", result["verdict"])
        self.assertEqual("stale", result["publication"][0]["status"])
        self.assertEqual("https://example.test/prior-comment", result["publication"][0]["comment_locator"])
        self.assertEqual(0, transport.writes)

    def test_post_write_change_preserves_locator_for_reconciliation(self):
        receipt, body, approval = self.publication_inputs()
        transport = MemoryTransport(copy.deepcopy(self.target))
        original = transport.put
        def put(*args):
            locator = original(*args)
            transport.target["revision"] = "changed-after-write"
            return locator
        transport.put = put
        result = self.send(receipt, body, approval, transport)
        self.assertEqual("BLOCKED", result["verdict"])
        self.assertFalse(result["gate_cleared"])
        self.assertEqual("stale", result["publication"][0]["status"])
        self.assertTrue(result["publication"][0]["comment_locator"])
        self.assertEqual(1, transport.writes)
        # Replaying a known-stale receipt cannot turn it into current publication.
        again = self.send(result, body, approval, transport)
        self.assertEqual("stale", again["publication"][0]["status"])
        self.assertEqual(1, transport.writes)

    def test_expiry_during_lookup_prevents_write_or_reuse(self):
        for reuse in (False, True):
            with self.subTest(reuse=reuse):
                self.now = instant(self.m["session"]["finished_at"]) + timedelta(seconds=1)
                receipt, body, approval = self.publication_inputs()
                transport = MemoryTransport(copy.deepcopy(self.target))
                def lookup(destination, markers):
                    self.now += timedelta(seconds=self.m["freshness_seconds"])
                    return dict(body=body, locator="https://example.test/prior") if reuse else None
                transport.find_owned = lookup
                result = self.send(receipt, body, approval, transport)
                self.assertEqual("BLOCKED", result["verdict"])
                self.assertEqual("stale", result["publication"][0]["status"])
                self.assertEqual(0, transport.writes)

    def test_destination_rechecked_after_lookup_and_readback(self):
        for phase in ("lookup", "write"):
            with self.subTest(phase=phase):
                receipt, body, approval = self.publication_inputs()
                transport = MemoryTransport(copy.deepcopy(self.target))
                transport.admitted = True
                transport.verify_destination = lambda *args: transport.admitted
                if phase == "lookup":
                    def lookup(*args):
                        transport.admitted = False
                        return None
                    transport.find_owned = lookup
                else:
                    original = transport.put
                    def put(*args):
                        location = original(*args)
                        transport.admitted = False
                        return location
                    transport.put = put
                result = self.send(receipt, body, approval, transport)
                self.assertEqual("PASS", result["verdict"])
                self.assertEqual("failed", result["publication"][0]["status"])
                self.assertEqual(0 if phase == "lookup" else 1, transport.writes)

    def test_publication_regeneration_renews_report_binding(self):
        receipt, body, approval = self.publication_inputs()
        transport = MemoryTransport(copy.deepcopy(self.target))
        old_report = report(self.m, receipt).encode()
        result = self.send(receipt, body, approval, transport)
        self.assertEqual("published", result["publication"][0]["status"])
        self.assertNotEqual(receipt["report_sha256"], result["report_sha256"])
        with self.assertRaises(ValueError):
            validate_receipt(result, self.m, self.evidence, self.target, report_bytes=old_report, now=self.now)
        self.assertTrue(validate_receipt(result, self.m, self.evidence, self.target,
            report_bytes=report(self.m, result).encode(), now=self.now))
        self.send(result, body, approval, transport)
        self.assertEqual(1, transport.writes)

    def test_final_read_timeout_retains_written_or_discovered_location_and_retries(self):
        for verdict in ("pass", "fail", "blocked"):
            for reuse in (False, True):
                with self.subTest(verdict=verdict, reuse=reuse):
                    self.m["checks"][0]["status"] = verdict
                    receipt, body, approval = self.publication_inputs()
                    transport = MemoryTransport(copy.deepcopy(self.target))
                    if reuse:
                        transport.comments["worker"] = body
                    original = transport.current_target
                    reads = 0
                    def current_target():
                        nonlocal reads
                        reads += 1
                        if reads == 5:
                            raise TimeoutError("synthetic private readback diagnostic")
                        return original()
                    transport.current_target = current_target
                    result = self.send(receipt, body, approval, transport)
                    self.assertEqual(5, reads)
                    self.assertEqual(receipt["verdict"], result["verdict"])
                    self.assertEqual(receipt["gate_cleared"], result["gate_cleared"])
                    state = result["publication"][0]
                    self.assertEqual("failed", state["status"])
                    self.assertEqual("https://example.test/comments/worker", state["comment_locator"])
                    self.assertIn("freshness", state["reason"])
                    regenerated = report(self.m, result).encode()
                    self.assertNotIn("synthetic private readback diagnostic", json.dumps(result))
                    self.assertNotIn(b"synthetic private readback diagnostic", regenerated)
                    self.assertEqual(hashlib.sha256(regenerated).hexdigest(), result["report_sha256"])
                    self.assertEqual(verdict == "pass", validate_receipt(result, self.m, self.evidence,
                        self.target, report_bytes=regenerated, now=self.now))
                    with self.assertRaises(ValueError):
                        validate_receipt(result, self.m, self.evidence, self.target,
                            report_bytes=report(self.m, receipt).encode(), now=self.now)
                    # A fresh retry reconciles the already delivered body without duplication.
                    again = self.send(result, body, approval, transport)
                    self.assertEqual("published", again["publication"][0]["status"])
                    self.assertEqual(state["comment_locator"], again["publication"][0]["comment_locator"])
                    self.assertEqual(0 if reuse else 1, transport.writes)

    def test_final_read_timeout_marks_all_deliveries_uncertain_and_stale_retry_blocks(self):
        self.publication_inputs()
        self.m["destinations"].extend([
            dict(id="second", kind="worker-thread", locator="synthetic-second", authorized=True),
            dict(id="private", kind="worker-thread", locator="synthetic-private", authorized=False),
        ])
        receipt = self.evaluate()
        body = summary(self.m, receipt, purpose="Demo", checked="Both steps",
                       next_action="Owner review", human_action="None")
        approval = dict(reviewed=True, body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                        destinations=copy.deepcopy(self.m["destinations"]))
        transport = MemoryTransport(copy.deepcopy(self.target))
        original = transport.current_target
        reads = 0
        def current_target():
            nonlocal reads
            reads += 1
            if reads == 8:
                raise TimeoutError("synthetic private readback diagnostic")
            return original()
        transport.current_target = current_target
        result = self.send(receipt, body, approval, transport)
        self.assertEqual(2, transport.writes)
        self.assertEqual(["failed", "failed", "not-authorized"],
                         [state["status"] for state in result["publication"]])
        locations = [state["comment_locator"] for state in result["publication"]]
        self.assertEqual(["https://example.test/comments/worker",
                          "https://example.test/comments/second", None], locations)
        transport.target["revision"] = "changed-before-retry"
        again = self.send(result, body, approval, transport)
        self.assertEqual("BLOCKED", again["verdict"])
        self.assertFalse(again["gate_cleared"])
        self.assertEqual(["stale", "stale", "not-authorized"],
                         [state["status"] for state in again["publication"]])
        self.assertEqual(locations, [state["comment_locator"] for state in again["publication"]])
        self.assertEqual(2, transport.writes)

    def test_criterion_totals_count_criteria_not_check_rows(self):
        advisory = copy.deepcopy(self.m["criteria"][0])
        advisory.update(id="advisory", required=False)
        self.m["criteria"].append(advisory)
        second = copy.deepcopy(self.m["checks"][0])
        second.update(id="second-observation")
        self.m["checks"].append(second)
        receipt = self.evaluate()
        self.assertEqual(dict(total=1, passed=1, failed=0, blocked=0), receipt["criterion_totals"]["required"])
        self.assertEqual(dict(total=1, passed=0, failed=0, blocked=1), receipt["criterion_totals"]["advisory"])
        fields = dict(line.split(": ", 1) for line in report(self.m, receipt).splitlines() if ": " in line)
        self.assertEqual(self.m["risks"], json.loads(fields["RISK"]))
        # Rebinding the rendered report cannot legitimize fabricated totals.
        receipt["criterion_totals"]["required"]["passed"] = 2
        receipt = bind_report(self.m, receipt)
        with self.assertRaises(ValueError):
            validate_receipt(receipt, self.m, self.evidence, self.target,
                             report_bytes=report(self.m, receipt).encode(), now=self.now)

    def cli_inputs(self, status):
        now = utc_now()
        self.m["session"].update(started_at=(now-timedelta(seconds=20)).isoformat(),
                                 finished_at=(now-timedelta(seconds=1)).isoformat())
        for artifact in self.m["artifacts"]:
            artifact["captured_at"] = (now-timedelta(seconds=10)).isoformat()
        self.m["checks"][0]["status"] = status
        if status == "blocked":
            self.m["checks"][0]["artifact_ids"] = []
        manifest = self.root / (status + "-manifest.json")
        manifest.write_text(json.dumps(self.m))
        target = self.root / "target.json"
        target.write_text(json.dumps(self.target))
        output = self.root / status
        common = ["--manifest", str(manifest), "--evidence-root", str(self.evidence),
                  "--current-target", str(target), "--target-root", str(self.root / "product")]
        self.env = {**os.environ, "PYTHONPATH": str(ROOT / "plugins/crosscheck/runtime")}
        evaluated = self.cli("evaluate", *common, "--output", str(output))
        return evaluated, output, common

    def cli(self, *args):
        return subprocess.run([sys.executable, "-m", "crosscheck", *args],
                              env=self.env, text=True, capture_output=True)

    def test_modified_report_cannot_clear_receipt(self):
        evaluated, output, common = self.cli_inputs("pass")
        self.assertEqual(0, evaluated.returncode, evaluated.stderr)
        (output / "qa-report.md").write_text("RESULT: PASS\nSCOPE: different untested work\n")
        verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"))
        self.assertEqual(2, verified.returncode)

    def test_valid_blocked_receipt_keeps_exit_two(self):
        evaluated, output, common = self.cli_inputs("blocked")
        self.assertEqual(2, evaluated.returncode, evaluated.stderr)
        verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"))
        self.assertEqual(2, verified.returncode)
        self.assertTrue(verified.stdout.startswith("BLOCKED:"))

    def test_cli_all_valid_verdicts(self):
        for verdict, code in (("pass", 0), ("fail", 1), ("blocked", 2)):
            with self.subTest(verdict=verdict):
                evaluated, output, common = self.cli_inputs(verdict)
                self.assertEqual(code, evaluated.returncode, evaluated.stderr)
                verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"))
                self.assertEqual(code, verified.returncode, verified.stderr)
                self.assertTrue(verified.stdout.startswith(verdict.upper() + ":"))

    def test_missing_or_swapped_report_is_blocked(self):
        _, output, common = self.cli_inputs("pass")
        _, other, _ = self.cli_inputs("fail")
        for path in (self.root / "missing.md", other / "qa-report.md"):
            with self.subTest(path=path.name):
                verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"),
                                    "--report", str(path))
                self.assertEqual(2, verified.returncode)
                self.assertTrue(verified.stderr.startswith("BLOCKED:"))
        (output / "qa-report.md").unlink()
        verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"))
        self.assertEqual(2, verified.returncode)

    def test_cli_stale_target_is_blocked(self):
        _, output, common = self.cli_inputs("pass")
        self.target["revision"] = "changed-after-evaluation"
        (self.root / "target.json").write_text(json.dumps(self.target))
        verified = self.cli("verify-receipt", *common, "--receipt", str(output / "crosscheck-receipt.json"))
        self.assertEqual(2, verified.returncode)
        self.assertTrue(verified.stderr.startswith("BLOCKED:"))


if __name__ == "__main__":
    unittest.main()
