# Independent QA Agent

An evidence-first QA skill for Codex and Claude Code. It independently checks completed work and returns exactly `PASS`, `FAIL`, or `BLOCKED`.

The agent is deliberately read-only: it verifies the builder's claims from raw evidence, records durable proof, and recommends the next lane without quietly fixing the product.

## What it verifies

- code diffs, tests, builds, and immutable delivery state;
- browser and UI behavior at named URLs and viewports;
- rendered documents and PDFs;
- data schemas, formulas, transformations, and reconciliation totals;
- operational state through read surfaces, dry runs, logs, and identifiers.

## Install in Codex

```bash
codex plugin marketplace add 2xgrowthagency/independent-qa-agent
codex plugin add qa-agent@independent-qa-agent
```

Start a new Codex task so the installed skill is loaded, then ask:

```text
Use $independent-verification to QA this completed work using qa-packet.md.
```

## Install in Claude Code

Clone this repository, then copy the same Agent Skill into a target project:

```bash
./scripts/install-claude-skill.sh /path/to/target-project
```

This creates:

```text
/path/to/target-project/.claude/skills/independent-verification/
```

Commit that directory if the whole team should inherit the skill. Claude Code discovers the `SKILL.md` metadata and loads the full instructions when the skill becomes relevant.

## Add it to a workflow

1. Give the QA agent a complete packet using [examples/qa-packet.md](examples/qa-packet.md).
2. Run QA in a separate agent/task from the builder.
3. Keep the tested target immutable: pin a commit, artifact hash, or exact URL and deployment identity.
4. Route `PASS` to review, `FAIL` to bounded rework, and `BLOCKED` to the owner of the missing input or capability.

The QA agent never inherits permission to fix, merge, deploy, or publish. Those actions need separate authorization.

## Repository layout

```text
.agents/plugins/marketplace.json        Codex marketplace
plugins/qa-agent/                       Codex plugin
  skills/independent-verification/      Shared Agent Skill
scripts/install-claude-skill.sh         Project-scoped Claude installer
examples/qa-packet.md                    Portable task contract
tests/validate.py                        Dependency-free structural checks
```

## Development

```bash
python3 tests/validate.py
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/qa-agent
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing verdict semantics or safety boundaries.

## License

MIT
