# Crosscheck

Crosscheck is the 2x-maintained, open-source verification gate for completed work.
Its deterministic runtime binds evidence to an exact target and returns `PASS`,
`FAIL`, or `BLOCKED`. Only PASS clears that target. A later change or expired
result requires fresh verification. PASS grants no merge, closure, deployment,
or account-change authority.

**Release candidate: 0.3.0-rc.1.** The runtime, schemas, tests and migration
installers are available for review. The canonical `$crosscheck` skill remains
pending integration through the existing Skill Workshop proposal. The Crosscheck
marketplace entry is deliberately unavailable until that integration and fresh
independent QA pass. The existing `qa-agent` plugin and `$independent-verification`
skill remain unchanged and usable; they do not automatically enforce the new runtime.

## Install the runtime

Requires Python 3.11 or later. From this repository checkout:

```bash
./scripts/install-runtime.sh .venv-crosscheck
.venv-crosscheck/bin/crosscheck --help
```

The installer creates a new isolated environment and refuses to overwrite an
existing one. This repository is the canonical source:
`2xgrowthagency/crosscheck`, renamed from `2xgrowthagency/independent-qa-agent`.
The Python distribution is `crosscheck-verifier`; no package registry release
has been published. Install the reviewed checkout, not an assumed registry package.

## Codex compatibility install

The existing published install path remains:

```bash
codex plugin marketplace add 2xgrowthagency/crosscheck
codex plugin add qa-agent@independent-qa-agent
```

Start a fresh task to load `$independent-verification`. The marketplace retains
its machine name `independent-qa-agent` to preserve installed references; its
visible name is Crosscheck. The staged future plugin name is
`crosscheck@independent-qa-agent`. Do not install it as a working skill until the
pending source integration is complete. Review checkout/runtime installation
is separate from the main-branch Codex plugin installation above.

## Claude Code compatibility install

```bash
./scripts/install-claude-skill.sh /path/to/target-project
```

This copies the unchanged skill into
`.claude/skills/independent-verification/` and refuses to overwrite an existing
installation. Runtime installation is independent and uses the first command
above. The explicit canonical path is:

```bash
./scripts/install-claude-skill.sh /path/to/isolated-project crosscheck
```

It currently returns **BLOCKED** without creating an installation because the
managed source is not integrated. After the owner supplies the managed skill and
its four references, it copies that package into `.claude/skills/crosscheck/`.
Actual Codex/Claude instruction discovery and invocation are separate acceptance
checks; Python imports, CLI success and a filesystem copy do not prove them.

## Runtime usage

A trusted fresh verifier collects observations and a current target readback.
The runtime checks those inputs; it does not launch an agent, execute producer
commands, enforce an operating-system sandbox, or prove that an attestation is true.
The harness must provide execution separation and a read-only target.

```bash
crosscheck evaluate \
  --manifest /path/to/evidence/evidence-manifest.json \
  --evidence-root /path/to/evidence \
  --current-target /path/to/current-target.json \
  --target-root /path/to/read-only-product \
  --output /path/to/new-private-report-directory
```

The output contains `qa-report.md`, `evidence-manifest.json`, and
`crosscheck-receipt.json`. Keep the original artifact bundle alongside the reports;
manifest artifact paths resolve against `--evidence-root`. A missing receipt means
an incomplete run. Exit codes are 0 for PASS, 1 for FAIL, and 2 for BLOCKED or an
invalid/unavailable contract. A malformed contract cannot issue a valid receipt.

Before consuming a stored result, run `crosscheck verify-receipt` with the same
inputs and `--receipt /path/to/crosscheck-receipt.json`, omitting `--output`.
It reads `qa-report.md` beside the receipt, or the exact file specified by
`--report`. Missing or changed report bytes fail closed. Validated PASS, FAIL and
BLOCKED receipts retain exit codes 0, 1 and 2, respectively; invalid or stale
inputs return BLOCKED with exit 2. Receipt schema 1.1 requires report hashes and
criterion totals; pre-release 1.0 receipts cannot clear this revised gate.
The current-target file must be freshly read by the trusted harness each time.
Never use a comment, old target snapshot or `gate_cleared` boolean as approval.

The unreleased `final-boss` CLI remains an alias and still writes
`final-boss-receipt.json`; Python `final_boss` imports share the Crosscheck runtime.
Stored Final Boss report/receipt pairs remain readable only when their exact
original bytes, bound target and freshness still validate. New reports and
comments use Crosscheck; exact legacy comment markers are reconciled in place.
See the migration matrix for installed legacy skill identities, which remain unchanged.

## Supported targets and evidence

The [profile policy](plugins/crosscheck/runtime/crosscheck/profiles.json) defines
inputs, checks, evidence, failure modes, stop conditions and PASS meaning for
code/PR, UI, interactive workflows, documents, data, operations, decisions and
QA processes. Multiple criteria can use different profiles in one bound target.

See the [contract reference](docs/contracts.md),
[synthetic screenshot and interaction bundle](examples/evidence),
[PASS/FAIL/BLOCKED comment examples](examples/comments),
[integration interfaces](docs/integrations.md), and
[migration matrix](docs/migration.md).

## Development

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tests/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tests/install_smoke.py
git diff --check
```

CI checks Python 3.11, 3.12 and 3.14. Optional screenshot recapture uses Playwright
1.58.0 and `scripts/capture-demo.py`; normal tests replay fixed synthetic bytes
and never launch a browser, access credentials, or call a model.
See [contribution and release requirements](CONTRIBUTING.md).

[MIT license](LICENSE). Migration behavior derives from John Chan’s public v0.2.1
implementation; private company instructions are not included.
