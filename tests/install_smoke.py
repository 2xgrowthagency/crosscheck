#!/usr/bin/env python3
"""Exercise legacy skill copy and actual runtime installation; never touch a user install."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = ("crosscheck", "final-boss", "independent-verification", "independent-qa-agent", "qa-agent", "workboard-qa-agent")


def digest_tree(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file()}


def run(args, expected=0, cwd=None):
    # A neutral cwd and no PYTHONPATH prove installed package behavior.
    env = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    result = subprocess.run([str(a) for a in args], text=True, capture_output=True, cwd=cwd, env=env)
    if result.returncode != expected:
        raise AssertionError(f"install command failed: {result.stdout} {result.stderr}")
    return result


def exercise_installed_cli(env, root):
    evidence = root / "evidence"
    shutil.copytree(ROOT / "examples/evidence", evidence)
    manifest = json.loads((evidence / "evidence-manifest.json").read_text())
    now = datetime.now(timezone.utc)
    manifest["session"].update(started_at=(now-timedelta(seconds=20)).isoformat(),
                               finished_at=(now-timedelta(seconds=1)).isoformat())
    for artifact in manifest["artifacts"]:
        artifact["captured_at"] = (now-timedelta(seconds=10)).isoformat()
    target = root / "product"; target.mkdir()
    (target / "sentinel").write_text("untouched")
    common = ["--manifest", evidence / "evidence-manifest.json", "--evidence-root", evidence,
              "--current-target", evidence / "current-target.json", "--target-root", target]
    for verdict, code in (("pass", 0), ("fail", 1), ("blocked", 2)):
        manifest["checks"][0]["status"] = verdict
        (evidence / "evidence-manifest.json").write_text(json.dumps(manifest))
        for name in ("crosscheck", "final-boss"):
            output = root / (verdict + "-" + name)
            evaluated = run([env / "bin" / name, "evaluate", *common, "--output", output], code, cwd=root)
            assert evaluated.stdout.startswith(verdict.upper() + ":")
            receipt = output / (name + "-receipt.json")
            assert {p.name for p in output.iterdir()} == {receipt.name, "qa-report.md", "evidence-manifest.json"}
            report = output / "qa-report.md"
            receipt_data = json.loads(receipt.read_text())
            assert receipt_data["report_sha256"] == hashlib.sha256(report.read_bytes()).hexdigest()
            assert report.read_text().startswith("# Crosscheck QA report\n")
            # Either executable can consume either receipt filename explicitly.
            consumer = "final-boss" if name == "crosscheck" else "crosscheck"
            verified = run([env / "bin" / consumer, "verify-receipt", *common, "--receipt", receipt], code, cwd=root)
            assert verified.stdout.startswith(verdict.upper() + ":")
            report.write_text(report.read_text() + "tampered report\n")
            run([env / "bin" / consumer, "verify-receipt", *common, "--receipt", receipt], 2, cwd=root)
    assert (target / "sentinel").read_text() == "untouched"


def main():
    with tempfile.TemporaryDirectory(dir=ROOT / ".work" if (ROOT / ".work").exists() else None) as tmp:
        root = Path(tmp)
        project = root / "project with spaces"; project.mkdir()
        run([ROOT / "scripts/install-claude-skill.sh", project])
        source = ROOT / "plugins/qa-agent/skills/independent-verification"
        installed = project / ".claude/skills/independent-verification"
        assert digest_tree(source) == digest_tree(installed)
        (installed / "user-note.md").write_text("preserve me")
        before = digest_tree(installed)
        run([ROOT / "scripts/install-claude-skill.sh", project], expected=1)
        assert before == digest_tree(installed)
        run([ROOT / "scripts/install-claude-skill.sh", project, "crosscheck"])
        canonical = project / ".claude/skills/crosscheck"
        assert digest_tree(ROOT / "plugins/crosscheck/skills/crosscheck") == digest_tree(canonical)
        (canonical / "user-note.md").write_text("preserve canonical notes")
        canonical_before = digest_tree(canonical)
        run([ROOT / "scripts/install-claude-skill.sh", project, "crosscheck"], expected=1)
        assert canonical_before == digest_tree(canonical)
        assert before == digest_tree(installed)
        for alias in ALIASES:
            env = root / alias
            run([ROOT / "scripts/install-runtime.sh", env, alias])
            run([env / "bin/crosscheck", "--help"], cwd=root)
            run([env / "bin/final-boss", "--help"], cwd=root)
            run([env / "bin/python", "-c", "import crosscheck, final_boss; from importlib.metadata import version; from crosscheck.gate import PROFILES; assert version('crosscheck-verifier') == '0.3.0rc1'; assert len(PROFILES) == 8; assert crosscheck.evaluate is final_boss.evaluate"], cwd=root)
            if alias == "crosscheck":
                exercise_installed_cli(env, root)
            run([ROOT / "scripts/install-runtime.sh", env, alias], expected=1)
    print("PASS: six runtime migration names; installed Crosscheck/final-boss verdicts, receipt interchange and report tamper rejection; canonical and legacy Claude byte equality/overwrite refusal")
    print("Instruction discovery/invocation requires the separate actual harness check; these are installation checks.")


if __name__ == "__main__": main()
