#!/usr/bin/env python3
"""Exercise legacy skill copy and actual runtime installation; never touch a user install."""
import hashlib
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = ("final-boss", "independent-verification", "qa-agent", "workboard-qa-agent")


def digest_tree(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file()}


def run(args, expected=0):
    result = subprocess.run([str(a) for a in args], text=True, capture_output=True)
    if result.returncode != expected:
        raise AssertionError(f"install command failed: {result.stdout} {result.stderr}")
    return result


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
        for alias in ALIASES:
            env = root / alias
            run([ROOT / "scripts/install-runtime.sh", env, alias])
            run([env / "bin/final-boss", "--help"])
            run([env / "bin/python", "-c", "import final_boss; from final_boss.gate import PROFILES; assert len(PROFILES) == 8"])
            run([ROOT / "scripts/install-runtime.sh", env, alias], expected=1)
    print("PASS: four runtime migration names; isolated installed CLI/schema package; legacy Claude skill byte equality and overwrite refusal")


if __name__ == "__main__": main()
