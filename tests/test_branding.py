"""Crosscheck naming must preserve receipt and comment compatibility."""
import copy
import hashlib
import importlib
import json
import subprocess
import unittest

from test_gate import GateFixture, MemoryTransport, ROOT


class BrandingTests(GateFixture, unittest.TestCase):
    def test_canonical_runtime_and_legacy_imports_share_the_gate(self):
        canonical = importlib.import_module("crosscheck")
        legacy = importlib.import_module("final_boss")
        self.assertIs(canonical.evaluate, legacy.evaluate)
        for module, name in (("gate", "validate_receipt"), ("report", "report"),
                             ("publication", "publish"), ("github", "GitHubTransport")):
            self.assertIs(getattr(importlib.import_module("crosscheck." + module), name),
                          getattr(importlib.import_module("final_boss." + module), name))

    def test_crosscheck_report_preserves_strict_legacy_receipt_consumption(self):
        from crosscheck.gate import evaluate, validate_receipt, validate
        from crosscheck.report import report
        receipt = evaluate(self.m, self.evidence, self.target, now=self.now)
        current = report(self.m, receipt).encode()
        self.assertTrue(current.startswith(b"# Crosscheck QA report\n"))
        legacy = current.replace(b"# Crosscheck QA report\n", b"# Final Boss QA report\n", 1)
        old_receipt = copy.deepcopy(receipt)
        old_receipt["report_sha256"] = hashlib.sha256(legacy).hexdigest()
        validate(old_receipt, "final-boss-receipt")
        validate(old_receipt, "crosscheck-receipt")
        self.assertTrue(validate_receipt(old_receipt, self.m, self.evidence, self.target,
            report_bytes=legacy, now=self.now))
        for bad in (current, legacy + b"Changed scope\n"):
            with self.assertRaises(ValueError):
                validate_receipt(old_receipt, self.m, self.evidence, self.target,
                    report_bytes=bad, now=self.now)
        changed = {**self.target, "revision": "changed"}
        with self.assertRaises(ValueError):
            validate_receipt(old_receipt, self.m, self.evidence, changed,
                report_bytes=legacy, now=self.now)

    def test_old_comment_markers_are_updated_in_place_and_retry_is_idempotent(self):
        from crosscheck.publication import publish, summary
        from crosscheck.report import report
        self.m["destinations"] = [dict(id="worker", kind="worker-thread",
            locator="synthetic-producer", authorized=True)]
        receipt = self.evaluate()
        body = summary(self.m, receipt, purpose="Demo", checked="Two steps",
                       next_action="Owner review", human_action="None")
        self.assertTrue(body.startswith("<!-- crosscheck-result:"))
        self.assertIn("\nCrosscheck: PASS", body)
        approval = dict(reviewed=True, body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                        destinations=copy.deepcopy(self.m["destinations"]))
        for prefix in ("final-boss-result", "independent-qa-result", "workboard-qa-result"):
            with self.subTest(prefix=prefix):
                transport = MemoryTransport(copy.deepcopy(self.target))
                transport.comments["worker"] = body.replace("crosscheck-result", prefix, 1)
                lookup = transport.find_owned
                def find_owned(destination, markers):
                    existing = lookup(destination, markers)
                    return existing if existing and existing["body"].splitlines()[0] in markers else None
                transport.find_owned = find_owned
                put = transport.put
                def update(destination, existing, body, key):
                    self.assertIsNotNone(existing, "renamed publisher must find the original comment")
                    return put(destination, existing, body, key)
                transport.put = update
                result = publish(self.m, receipt, self.evidence, transport, body, approval,
                    report_bytes=report(self.m, receipt).encode(), clock=lambda: self.now)
                self.assertEqual("published", result["publication"][0]["status"])
                again = publish(self.m, result, self.evidence, transport, body, approval,
                    report_bytes=report(self.m, result).encode(), clock=lambda: self.now)
                self.assertEqual("published", again["publication"][0]["status"])
                self.assertEqual(1, transport.writes)

    def test_previously_approved_final_boss_body_can_retry_without_losing_binding(self):
        from crosscheck.publication import publish, summary
        from crosscheck.report import report
        self.m["destinations"] = [dict(id="worker", kind="worker-thread",
            locator="synthetic-producer", authorized=True)]
        receipt = self.evaluate()
        body = summary(self.m, receipt, purpose="Demo", checked="Two steps",
                       next_action="Owner review", human_action="None")
        body = body.replace("crosscheck-result:", "final-boss-result:", 1).replace("Crosscheck: PASS", "Final Boss: PASS", 1)
        approval = dict(reviewed=True, body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                        destinations=copy.deepcopy(self.m["destinations"]))
        transport = MemoryTransport(copy.deepcopy(self.target))
        result = publish(self.m, receipt, self.evidence, transport, body, approval,
            report_bytes=report(self.m, receipt).encode(), clock=lambda: self.now)
        self.assertEqual("published", result["publication"][0]["status"])
        self.assertEqual(body, transport.comments["worker"])
        wrong = body.replace(receipt["target_sha256"], "f" * 64, 1)
        wrong_approval = {**approval, "body_sha256": hashlib.sha256(wrong.encode()).hexdigest()}
        with self.assertRaises(ValueError):
            publish(self.m, receipt, self.evidence, transport, wrong, wrong_approval,
                report_bytes=report(self.m, receipt).encode(), clock=lambda: self.now)
        self.assertEqual(1, transport.writes)

    def test_canonical_claude_install_refuses_missing_managed_source_without_writes(self):
        project = self.root / "isolated project"
        project.mkdir()
        done = subprocess.run([ROOT / "scripts/install-claude-skill.sh", project, "crosscheck"],
                              text=True, capture_output=True)
        self.assertEqual(2, done.returncode)
        self.assertIn("managed Crosscheck skill source", done.stderr)
        self.assertEqual([], list(project.iterdir()))


if __name__ == "__main__":
    unittest.main()
