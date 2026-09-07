#!/usr/bin/env python3
"""Validate consumed metadata and schema/example contracts, not prompt wording."""
import json
import sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/final-boss/runtime"))
from final_boss.gate import evaluate, instant, validate, validate_receipt


def main():
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    assert marketplace["name"] == "independent-qa-agent", "preserve installed marketplace identity"
    assert marketplace["interface"]["displayName"] == "Final Boss"
    assert {p["name"] for p in marketplace["plugins"]} == {"qa-agent", "final-boss"}
    for entry in marketplace["plugins"]:
        plugin = ROOT / entry["source"]["path"]
        metadata = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
        assert metadata["name"] == plugin.name == entry["name"]
        assert metadata["author"]["name"] == "2x Growth Agency"
        assert entry["policy"]["installation"] == ("NOT_AVAILABLE" if entry["name"] == "final-boss" else "AVAILABLE")
        assert entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}
        for field in ("composerIcon", "logo", "logoDark"):
            if field in metadata["interface"]:
                assert (plugin / metadata["interface"][field]).is_file()
        if "skills" in metadata:
            assert (plugin / metadata["skills"]).is_dir()
            for skill in (plugin / metadata["skills"]).glob("*/SKILL.md"):
                _, frontmatter, _ = skill.read_text().split("---", 2)
                parsed = yaml.safe_load(frontmatter)
                assert parsed["name"] == skill.parent.name
                assert isinstance(parsed["description"], str) and parsed["description"]
    for path in (ROOT / "plugins/final-boss/runtime/final_boss/schemas").glob("*.json"):
        Draft202012Validator.check_schema(json.loads(path.read_text()))
    bundle = ROOT / "examples/evidence"
    manifest = json.loads((bundle / "evidence-manifest.json").read_text())
    receipt = json.loads((bundle / "final-boss-receipt.json").read_text())
    validate_receipt(receipt, manifest, bundle, manifest["target"], now=instant(receipt["evaluated_at"]))
    for path in (ROOT / "examples/comments").glob("*.json"):
        validate(json.loads(path.read_text()), "final-boss-receipt")
    workflow = yaml.safe_load((ROOT / ".github/workflows/validate.yml").read_text())
    events = workflow.get("on", workflow.get(True))  # YAML 1.1 treats on as a boolean.
    assert "pull_request" in events and "main" in events["push"]["branches"]
    assert workflow["permissions"] == {"contents": "read"}
    print("PASS: package metadata, legacy skill metadata, schemas, example receipts and CI contract")


if __name__ == "__main__":
    main()
