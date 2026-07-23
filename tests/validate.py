#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "qa-agent"
SKILL = PLUGIN / "skills" / "independent-verification" / "SKILL.md"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

errors = []

for path in (SKILL, MANIFEST, MARKETPLACE, ROOT / "README.md", ROOT / "LICENSE"):
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if MANIFEST.is_file():
    manifest = json.loads(MANIFEST.read_text())
    if manifest.get("name") != "qa-agent":
        errors.append("plugin name must be qa-agent")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin skills path must be ./skills/")

if MARKETPLACE.is_file():
    marketplace = json.loads(MARKETPLACE.read_text())
    if marketplace.get("name") != "independent-qa-agent":
        errors.append("marketplace name must be independent-qa-agent")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1 or entries[0].get("name") != "qa-agent":
        errors.append("marketplace must expose exactly one qa-agent plugin")

if SKILL.is_file():
    skill = SKILL.read_text()
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
    if not frontmatter:
        errors.append("skill must start with YAML frontmatter")
    else:
        meta = frontmatter.group(1)
        if "name: independent-verification" not in meta:
            errors.append("skill name must be independent-verification")
        if "description:" not in meta:
            errors.append("skill description is required")
    for required in ("PASS", "FAIL", "BLOCKED", "Treat builder summaries", "read-only"):
        if required not in skill:
            errors.append(f"skill is missing required contract text: {required}")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    forbidden_patterns = (
        "/" + "Users/",
        r"\b" + "Work" + "board" + r"\b",
        "workboard" + "-qa-result",
        "gho_" + r"[A-Za-z0-9]+",
    )
    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            errors.append(f"private or non-portable text in {path.relative_to(ROOT)}: {pattern}")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: repository structure and portability checks passed")
